import { Link } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Star } from 'lucide-react';

interface DestinationCardProps {
  id: string;
  name: string;
  description: string;
  imageUrl: string;
  rating?: number;
  reviewCount?: number;
}

export function DestinationCard({ id, name, description, imageUrl, rating, reviewCount }: DestinationCardProps) {
  return (
    <Card className="overflow-hidden">
      <div className="aspect-video w-full overflow-hidden">
        <img
          src={imageUrl}
          alt={name}
          className="h-full w-full object-cover transition-transform hover:scale-105"
        />
      </div>
      <CardHeader>
        <CardTitle className="text-xl">{name}</CardTitle>
        {rating && (
          <div className="flex items-center space-x-1">
            <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
            <span className="text-sm font-medium">{rating.toFixed(1)}</span>
            {reviewCount && (
              <span className="text-sm text-gray-500">({reviewCount} reviews)</span>
            )}
          </div>
        )}
      </CardHeader>
      <CardContent>
        <CardDescription className="line-clamp-2">{description}</CardDescription>
      </CardContent>
      <CardFooter>
        <Button asChild className="w-full">
          <Link to={`/destinations/${id}`}>View Details</Link>
        </Button>
      </CardFooter>
    </Card>
  );
}
