import { Menu } from "lucide-react"
import { Button } from "../ui/button"
import { Link } from "react-router-dom"

const Header = () => {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white">
      <div className="container flex h-16 items-center justify-between">
        <Link to="/" className="text-2xl font-bold text-blue-600">
          Cemelin
        </Link>
        
        <nav className="hidden md:flex space-x-6">
          <Link to="/" className="text-gray-600 hover:text-blue-600">
            Home
          </Link>
          <Link to="/destinations" className="text-gray-600 hover:text-blue-600">
            Destinations
          </Link>
          <Link to="/plans" className="text-gray-600 hover:text-blue-600">
            Plans
          </Link>
          <Link to="/contact" className="text-gray-600 hover:text-blue-600">
            Contact Us
          </Link>
        </nav>

        <Button variant="ghost" className="md:hidden">
          <Menu className="h-6 w-6" />
        </Button>
      </div>
    </header>
  )
}

export default Header
