import { useState, useEffect } from "react"
import { 
  ArrowLeft, 
  MapPin, 
  Plus, 
  Search, 
  Filter, 
  Globe, 
  CreditCard, 
  DollarSign,
  Smartphone,
  ShoppingCart,
  Pill,
  Building2,
  Bus,
  Dumbbell,
  BookOpen,
  UtensilsCrossed,
  List,
  Grid3x3,
  CheckCircle2,
  Clock,
  Navigation
} from "lucide-react"
import { Button } from "@/shared/components/ui/button"
import { Input } from "@/shared/components/ui/input"
import { Card } from "@/shared/components/ui/card"
import { Spinner } from "@/shared/components/ui/spinner"
import { cn } from "@/lib/utils"
import { useCurrentUser } from "@/features/user/hooks/useCurrentUser"
import { placeService } from "../services/placeService"

// Map category names to icons
const categoryIconMap = {
  "SIM/eSIM": Smartphone,
  "Groceries": ShoppingCart,
  "Pharmacy": Pill,
  "ATM/Banks": Building2,
  "Transport": Bus,
  "Gyms": Dumbbell,
  "Study Spaces": BookOpen,
  "Eateries": UtensilsCrossed,
}

const categoryColorMap = {
  "SIM/eSIM": "text-blue-600",
  "Groceries": "text-gray-600",
  "Pharmacy": "text-red-600",
  "ATM/Banks": "text-green-600",
  "Transport": "text-blue-600",
  "Gyms": "text-yellow-600",
  "Study Spaces": "text-green-600",
  "Eateries": "text-purple-600",
}

function formatDate(dateString) {
  if (!dateString) return "Never"
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return "Today"
  if (diffDays === 1) return "1 day ago"
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 14) return "1 week ago"
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  if (diffDays < 60) return "1 month ago"
  return `${Math.floor(diffDays / 30)} months ago`
}

export default function HomePage() {
  const { user, isLoading: isLoadingUser } = useCurrentUser()
  const [searchQuery, setSearchQuery] = useState("")
  const [activeFilters, setActiveFilters] = useState([])
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [viewMode, setViewMode] = useState("list")
  const [categories, setCategories] = useState([])
  const [places, setPlaces] = useState([])
  const [isLoadingPlaces, setIsLoadingPlaces] = useState(true)
  const [isLoadingCategories, setIsLoadingCategories] = useState(true)

  // Fetch categories
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const cats = await placeService.getCategories()
        setCategories(cats)
      } catch (error) {
        console.error("Failed to fetch categories:", error)
      } finally {
        setIsLoadingCategories(false)
      }
    }
    fetchCategories()
  }, [])

  // Fetch places
  useEffect(() => {
    const fetchPlaces = async () => {
      setIsLoadingPlaces(true)
      try {
        const items = await placeService.getPlaces(
          selectedCategory,
          searchQuery || null
        )
        setPlaces(items)
      } catch (error) {
        console.error("Failed to fetch places:", error)
        setPlaces([])
      } finally {
        setIsLoadingPlaces(false)
      }
    }
    fetchPlaces()
  }, [selectedCategory, searchQuery])

  const toggleFilter = (filter) => {
    setActiveFilters(prev => 
      prev.includes(filter) 
        ? prev.filter(f => f !== filter)
        : [...prev, filter]
    )
  }

  if (isLoadingUser) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Spinner className="h-8 w-8" />
      </div>
    )
  }

  const rotationCityName = user?.rotation_city?.name || "Loading..."

  const getTagColor = (tagName) => {
    if (tagName === "English") return "bg-purple-100 text-purple-700"
    if (tagName === "Foreign Cards") return "bg-green-100 text-green-700"
    return "bg-gray-100 text-gray-700"
  }

  // Filter places by active filters
  const filteredPlaces = places.filter(place => {
    if (activeFilters.length === 0) return true
    
    const placeTags = place.tags.map(t => t.tag_name)
    const hasEnglish = placeTags.includes("English") && place.tags.find(t => t.tag_name === "English")?.boolean_value
    const hasForeignCards = placeTags.includes("Foreign Cards") && place.tags.find(t => t.tag_name === "Foreign Cards")?.boolean_value
    const hasBudget = placeTags.includes("Budget")
    
    if (activeFilters.includes("english") && !hasEnglish) return false
    if (activeFilters.includes("cards") && !hasForeignCards) return false
    if (activeFilters.includes("budget") && !hasBudget) return false
    
    return true
  })

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="sticky top-0 z-10 bg-white border-b border-gray-200 px-4 py-3">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="icon" className="h-8 w-8">
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div className="flex items-center gap-2">
              <MapPin className="h-5 w-5 text-purple-600" />
              <div>
                <h1 className="text-lg font-bold text-gray-900">{rotationCityName}</h1>
                <p className="text-xs text-gray-600">Student guide</p>
              </div>
            </div>
          </div>
          <Button className="bg-orange-500 hover:bg-orange-600 text-white h-9 px-4">
            <Plus className="h-4 w-4 mr-2" />
            Add Place
          </Button>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
        {/* Search Bar */}
        <div className="flex items-center gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <Input
              type="text"
              placeholder="Search places..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 h-11 rounded-lg border-gray-300"
            />
          </div>
          <Button variant="outline" size="icon" className="h-11 w-11 rounded-lg border-gray-300">
            <Filter className="h-5 w-5 text-gray-600" />
          </Button>
        </div>

        {/* Filter Buttons */}
        <div className="flex gap-2 flex-wrap">
          <Button
            variant={activeFilters.includes("english") ? "default" : "outline"}
            size="sm"
            onClick={() => toggleFilter("english")}
            className={cn(
              "rounded-lg border-gray-300 h-9",
              activeFilters.includes("english") && "bg-purple-600 hover:bg-purple-700 text-white border-purple-600"
            )}
          >
            <Globe className="h-4 w-4 mr-2" />
            English-Friendly
          </Button>
          <Button
            variant={activeFilters.includes("cards") ? "default" : "outline"}
            size="sm"
            onClick={() => toggleFilter("cards")}
            className={cn(
              "rounded-lg border-gray-300 h-9",
              activeFilters.includes("cards") && "bg-green-600 hover:bg-green-700 text-white border-green-600"
            )}
          >
            <CreditCard className="h-4 w-4 mr-2" />
            Foreign Cards
          </Button>
          <Button
            variant={activeFilters.includes("budget") ? "default" : "outline"}
            size="sm"
            onClick={() => toggleFilter("budget")}
            className={cn(
              "rounded-lg border-gray-300 h-9",
              activeFilters.includes("budget") && "bg-yellow-500 hover:bg-yellow-600 text-white border-yellow-500"
            )}
          >
            <DollarSign className="h-4 w-4 mr-2" />
            $ Budget
          </Button>
        </div>

        {/* Categories Section */}
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-4">Categories</h2>
          {isLoadingCategories ? (
            <div className="flex justify-center py-8">
              <Spinner className="h-6 w-6" />
            </div>
          ) : (
            <div className="grid grid-cols-4 gap-3">
              {categories.map((category) => {
                const Icon = categoryIconMap[category.name] || ShoppingCart
                const color = categoryColorMap[category.name] || "text-gray-600"
                return (
                  <Card
                    key={category.category_id}
                    onClick={() => setSelectedCategory(selectedCategory === category.category_id ? null : category.category_id)}
                    className={cn(
                      "p-4 cursor-pointer hover:shadow-md transition-shadow border-gray-200",
                      selectedCategory === category.category_id && "ring-2 ring-purple-600"
                    )}
                  >
                    <div className="flex flex-col items-center gap-2">
                      <div className={cn("p-2 rounded-lg bg-gray-50", color)}>
                        <Icon className="h-6 w-6" />
                      </div>
                      <div className="text-center">
                        <p className="text-sm font-medium text-gray-900">{category.name}</p>
                        <p className="text-xs text-gray-500">{category.count}</p>
                      </div>
                    </div>
                  </Card>
                )
              })}
            </div>
          )}
        </section>

        {/* All Places Section */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900">
              All Places ({filteredPlaces.length})
            </h2>
            <div className="flex gap-2">
              <Button
                variant={viewMode === "list" ? "default" : "outline"}
                size="icon"
                onClick={() => setViewMode("list")}
                className={cn(
                  "h-9 w-9",
                  viewMode === "list" && "bg-purple-600 hover:bg-purple-700 text-white"
                )}
              >
                <List className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === "grid" ? "default" : "outline"}
                size="icon"
                onClick={() => setViewMode("grid")}
                className={cn(
                  "h-9 w-9",
                  viewMode === "grid" && "bg-purple-600 hover:bg-purple-700 text-white"
                )}
              >
                <Grid3x3 className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {isLoadingPlaces ? (
            <div className="flex justify-center py-12">
              <Spinner className="h-8 w-8" />
            </div>
          ) : filteredPlaces.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              No places found. Try adjusting your filters or search.
            </div>
          ) : (
            <div className={cn(
              "space-y-4",
              viewMode === "grid" && "grid grid-cols-1 md:grid-cols-2 gap-4"
            )}>
              {filteredPlaces.map((place) => {
                const budgetTag = place.tags.find(t => t.tag_name === "Budget")
                const price = budgetTag?.value || ""
                const englishTag = place.tags.find(t => t.tag_name === "English" && t.boolean_value)
                const foreignCardsTag = place.tags.find(t => t.tag_name === "Foreign Cards" && t.boolean_value)
                
                const displayTags = []
                if (englishTag) displayTags.push("English")
                if (foreignCardsTag) displayTags.push("Foreign Cards")
                
                return (
                  <Card key={place.item_id} className="p-4 border-gray-200 hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 mb-1">{place.name}</h3>
                        <div className="flex items-center gap-1 text-sm text-gray-600 mb-2">
                          <MapPin className="h-4 w-4" />
                          <span>{place.location}</span>
                          {place.walking_distance && (
                            <>
                              <span className="text-gray-400">•</span>
                              <span>{place.walking_distance.toFixed(1)} km away</span>
                            </>
                          )}
                        </div>
                        {displayTags.length > 0 && (
                          <div className="flex flex-wrap gap-2 mb-3">
                            {displayTags.map((tag, idx) => (
                              <span
                                key={idx}
                                className={cn(
                                  "px-2 py-1 text-xs rounded-md font-medium",
                                  getTagColor(tag)
                                )}
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        )}
                        <div className="flex items-center gap-4 text-sm text-gray-600">
                          <div className="flex items-center gap-1">
                            <CheckCircle2 className="h-4 w-4 text-green-600" />
                            <span>{place.number_of_verifications} verified</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <Clock className="h-4 w-4" />
                            <span>{formatDate(place.last_verified_date)}</span>
                          </div>
                        </div>
                      </div>
                      {price && (
                        <div className="text-right">
                          <p className="text-lg font-semibold text-gray-900 mb-4">{price}</p>
                        </div>
                      )}
                    </div>
                    <div className="flex gap-2">
                      <Button className="flex-1 bg-purple-600 hover:bg-purple-700 text-white">
                        View Details
                      </Button>
                      <Button variant="outline" className="flex-1 border-gray-300">
                        <Navigation className="h-4 w-4 mr-2" />
                        Directions
                      </Button>
                    </div>
                  </Card>
                )
              })}
            </div>
          )}
        </section>
      </div>
    </div>
  )
}
