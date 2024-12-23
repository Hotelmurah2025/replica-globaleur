import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Star, Loader2 } from 'lucide-react';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { toast } from '../ui/use-toast';

interface Review {
  id: string;
  user_name: string;
  rating: number;
  content: string;
  created_at: string;
}

interface ReviewListProps {
  destinationId: string;
}

export function ReviewList({ destinationId }: ReviewListProps) {
  const { t } = useTranslation();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [newReview, setNewReview] = useState('');
  const [rating, setRating] = useState(5);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/reviews/${destinationId}`
        );
        if (!response.ok) {
          throw new Error('Failed to fetch reviews');
        }
        const data = await response.json();
        setReviews(data);
      } catch (error) {
        console.error('Error fetching reviews:', error);
        toast({
          title: t('reviews.error'),
          description: t('reviews.fetchError'),
          variant: 'destructive',
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchReviews();
  }, [destinationId, t]);

  const handleSubmitReview = async () => {
    if (!newReview.trim()) {
      toast({
        title: t('reviews.error'),
        description: t('reviews.emptyReview'),
        variant: 'destructive',
      });
      return;
    }

    setIsSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        toast({
          title: t('reviews.error'),
          description: t('reviews.loginRequired'),
          variant: 'destructive',
        });
        return;
      }

      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/reviews/${destinationId}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            content: newReview,
            rating,
          }),
        }
      );

      if (!response.ok) {
        throw new Error('Failed to submit review');
      }

      const newReviewData = await response.json();
      setReviews((prev) => [newReviewData, ...prev]);
      setNewReview('');
      setRating(5);
      toast({
        title: t('reviews.success'),
        description: t('reviews.submitSuccess'),
      });
    } catch (error) {
      console.error('Error submitting review:', error);
      toast({
        title: t('reviews.error'),
        description: t('reviews.submitError'),
        variant: 'destructive',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">{t('reviews.title')}</h2>
      
      <div className="space-y-4">
        <div className="flex space-x-2">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              onClick={() => setRating(star)}
              className="focus:outline-none"
            >
              <Star
                className={`h-6 w-6 ${
                  star <= rating
                    ? 'fill-yellow-400 text-yellow-400'
                    : 'fill-gray-200 text-gray-200'
                }`}
              />
            </button>
          ))}
        </div>
        
        <Textarea
          value={newReview}
          onChange={(e) => setNewReview(e.target.value)}
          placeholder={t('reviews.placeholder')}
          className="min-h-[100px]"
        />
        
        <Button
          onClick={handleSubmitReview}
          disabled={isSubmitting}
          className="w-full"
        >
          {isSubmitting ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            t('reviews.submit')
          )}
        </Button>
      </div>

      <div className="space-y-4">
        {isLoading ? (
          <div className="flex justify-center py-8">
            <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
          </div>
        ) : reviews.length > 0 ? (
          reviews.map((review) => (
            <div key={review.id} className="border-b pb-4">
              <div className="flex items-center justify-between mb-2">
                <div className="font-medium">{review.user_name}</div>
                <div className="flex items-center">
                  <Star className="h-4 w-4 fill-yellow-400 text-yellow-400 mr-1" />
                  <span>{review.rating}</span>
                </div>
              </div>
              <p className="text-gray-600">{review.content}</p>
              <div className="text-sm text-gray-400 mt-2">
                {new Date(review.created_at).toLocaleDateString()}
              </div>
            </div>
          ))
        ) : (
          <p className="text-center text-gray-500 py-4">
            {t('reviews.noReviews')}
          </p>
        )}
      </div>
    </div>
  );
}
