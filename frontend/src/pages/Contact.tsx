import { useState } from "react"
import { useTranslation } from "react-i18next"
import { Helmet } from "react-helmet-async"
import { Button } from "../components/ui/button"
import { Input } from "../components/ui/input"
import { Label } from "../components/ui/label"
import { Textarea } from "../components/ui/textarea"
import { toast } from "@/components/ui/use-toast"

export default function Contact() {
  const { t } = useTranslation()
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  })
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/contact`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        toast({
          title: t('contact.success'),
          description: t('contact.successMessage'),
        })
        setFormData({ name: "", email: "", subject: "", message: "" })
      } else {
        throw new Error("Failed to send message")
      }
    } catch {
      toast({
        title: t('contact.error'),
        description: t('contact.errorMessage'),
        variant: "destructive",
      })
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <Helmet>
          <title>{t('nav.contactUs')} | Cemelin Travel</title>
          <meta name="description" content={t('contact.metaDescription')} />
          <meta property="og:title" content={`${t('nav.contactUs')} | Cemelin Travel`} />
          <meta property="og:description" content={t('contact.metaDescription')} />
          <meta property="og:type" content="website" />
        </Helmet>
        <h1 className="text-3xl font-bold mb-8">{t('nav.contactUs')}</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="name">{t('contact.name')}</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">{t('contact.email')}</Label>
            <Input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="subject">{t('contact.subject')}</Label>
            <Input
              id="subject"
              value={formData.subject}
              onChange={(e) =>
                setFormData({ ...formData, subject: e.target.value })
              }
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="message">{t('contact.message')}</Label>
            <Textarea
              id="message"
              value={formData.message}
              onChange={(e) =>
                setFormData({ ...formData, message: e.target.value })
              }
              required
              className="min-h-[200px]"
            />
          </div>
          <Button type="submit" className="w-full">
            {t('contact.send')}
          </Button>
        </form>
      </div>
    </div>
  )
}
