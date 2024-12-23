import { Facebook, Instagram, Twitter, Youtube } from "lucide-react"
import { Link } from "react-router-dom"
import { useTranslation } from "react-i18next"

const Footer = () => {
  const { t } = useTranslation();
  return (
    <footer className="border-t bg-gray-50">
      <div className="container py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">{t('footer.legal')}</h3>
            <div className="space-y-2">
              <Link to="/terms" className="block text-gray-600 hover:text-blue-600">
                {t('footer.terms')}
              </Link>
              <Link to="/privacy" className="block text-gray-600 hover:text-blue-600">
                {t('footer.privacy')}
              </Link>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">{t('footer.company')}</h3>
            <div className="space-y-2">
              <Link to="/about" className="block text-gray-600 hover:text-blue-600">
                {t('footer.about')}
              </Link>
              <Link to="/contact" className="block text-gray-600 hover:text-blue-600">
                {t('footer.contact')}
              </Link>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">{t('footer.support')}</h3>
            <div className="space-y-2">
              <Link to="/faq" className="block text-gray-600 hover:text-blue-600">
                {t('footer.faq')}
              </Link>
              <Link to="/help" className="block text-gray-600 hover:text-blue-600">
                {t('footer.help')}
              </Link>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">{t('footer.followUs')}</h3>
            <div className="flex space-x-4">
              <a
                href="https://facebook.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-[#1877F2] transition-colors"
                aria-label="Facebook"
              >
                <Facebook className="h-6 w-6" />
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-[#1DA1F2] transition-colors"
                aria-label="Twitter"
              >
                <Twitter className="h-6 w-6" />
              </a>
              <a
                href="https://instagram.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-[#E4405F] transition-colors"
                aria-label="Instagram"
              >
                <Instagram className="h-6 w-6" />
              </a>
              <a
                href="https://youtube.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-[#FF0000] transition-colors"
                aria-label="YouTube"
              >
                <Youtube className="h-6 w-6" />
              </a>
            </div>
          </div>
        </div>
        
        <div className="mt-8 border-t pt-8 text-center text-gray-600">
          <p>© {new Date().getFullYear()} Cemelin Travel. {t('footer.rights')}</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
