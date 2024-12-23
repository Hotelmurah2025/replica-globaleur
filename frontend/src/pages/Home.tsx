import { Search } from "lucide-react"
import { Input } from "../components/ui/input"
import { Button } from "../components/ui/button"

const Home = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative h-[600px] bg-gradient-to-r from-blue-600 to-blue-400 flex items-center justify-center">
        <div className="container text-center text-white">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Discover Your Next Adventure
          </h1>
          <p className="text-xl mb-8">
            Find and plan your perfect trip with Cemelin
          </p>
          
          {/* Search Bar */}
          <div className="max-w-2xl mx-auto flex gap-2">
            <div className="flex-1 relative">
              <Input
                type="text"
                placeholder="Search destinations..."
                className="w-full h-12 pl-12 bg-white text-gray-900"
              />
              <Search className="absolute left-4 top-3 h-6 w-6 text-gray-400" />
            </div>
            <Button className="h-12 px-8 bg-blue-700 hover:bg-blue-800">
              Search
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
