import { useState } from "react"
import { Menu, Globe, User } from "lucide-react"
import { Button } from "../ui/button"
import { Link } from "react-router-dom"
import { useTranslation } from "react-i18next"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "../ui/dropdown-menu"

const Header = () => {
  const { t, i18n } = useTranslation()
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const languages = [
    { code: 'en', label: 'English' },
    { code: 'id', label: 'Indonesia' },
  ]

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white">
      <div className="container flex h-16 items-center justify-between">
        <Link to="/" className="flex items-center space-x-2">
          <div className="h-8 w-8 bg-blue-600 rounded-md flex items-center justify-center text-white font-bold">C</div>
          <span className="text-2xl font-bold text-blue-600">Cemelin</span>
        </Link>
        
        <nav className="hidden md:flex space-x-6">
          <Link to="/" className="text-gray-600 hover:text-blue-600 transition-colors">
            {t('home')}
          </Link>
          <Link to="/destinations" className="text-gray-600 hover:text-blue-600 transition-colors">
            {t('destinations')}
          </Link>
          <Link to="/plans" className="text-gray-600 hover:text-blue-600 transition-colors">
            {t('plans')}
          </Link>
          <Link to="/contact" className="text-gray-600 hover:text-blue-600 transition-colors">
            {t('contactUs')}
          </Link>
        </nav>

        <div className="hidden md:flex items-center space-x-4">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon">
                <Globe className="h-5 w-5" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              {languages.map((lang) => (
                <DropdownMenuItem
                  key={lang.code}
                  onClick={() => i18n.changeLanguage(lang.code)}
                  className={i18n.language === lang.code ? "bg-blue-50" : ""}
                >
                  {lang.label}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>

          <Button variant="ghost" className="flex items-center space-x-2">
            <User className="h-5 w-5" />
            <span>{t('signIn')}</span>
          </Button>
          <Button>{t('signUp')}</Button>
        </div>

        <Button
          variant="ghost"
          className="md:hidden"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <Menu className="h-6 w-6" />
        </Button>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden border-t">
          <nav className="container py-4 space-y-2">
            <Link to="/" className="block px-4 py-2 text-gray-600 hover:bg-blue-50 rounded-lg">
              {t('home')}
            </Link>
            <Link to="/destinations" className="block px-4 py-2 text-gray-600 hover:bg-blue-50 rounded-lg">
              {t('destinations')}
            </Link>
            <Link to="/plans" className="block px-4 py-2 text-gray-600 hover:bg-blue-50 rounded-lg">
              {t('plans')}
            </Link>
            <Link to="/contact" className="block px-4 py-2 text-gray-600 hover:bg-blue-50 rounded-lg">
              {t('contactUs')}
            </Link>
            <div className="px-4 py-2 space-y-2">
              <Button variant="ghost" className="w-full justify-start">
                <User className="h-5 w-5 mr-2" />
                {t('signIn')}
              </Button>
              <Button className="w-full">{t('signUp')}</Button>
            </div>
          </nav>
        </div>
      )}
    </header>
  )
}

export default Header
