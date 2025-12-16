// frontend/src/features/userProfile/ViewUserProfilePage.jsx

import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"

import { getUserById } from "@/api/otherUser"
import { getUserItems } from "@/api/item"
import '@/shared/styles/locale-theme.css'

export default function ViewUserProfilePage() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [user, setUser] = useState(null)
  const [items, setItems] = useState([])
  const [loadingItems, setLoadingItems] = useState(true)
  const [error, setError] = useState(null)
  const [userLocale, setUserLocale] = useState('usa')

  const localeMap = {
    'san francisco': 'usa',
    'taipei': 'china',
    'seoul': 'korea',
    'buenos aires': 'argentina',
    'hyderabad': 'india',
    'berlin': 'germany'
  }

  const getLocaleClass = () => {
    const classMap = {
      usa: 'show-photo',
      china: 'transition-green',
      korea: 'transition-korea',
      argentina: 'transition-argentina',
      india: 'transition-india',
      germany: 'transition-germany'
    }
    return classMap[userLocale] || 'show-photo'
  }

  const getLocaleColor = () => {
    const colorMap = {
      usa: '#cc0000',
      china: '#2c6e49',
      korea: '#da627d',
      argentina: '#d9a300',
      india: '#ff9505',
      germany: '#007ea7'
    }
    return colorMap[userLocale] || '#cc0000'
  }

  const localeCategoryPalettes = {
    usa: ["#002856", "#A50404", "#B8500C", "#F6DBAF", "#F6DBAF"],        
    china: ["#2c6e49", "#4c956c", "#ffc9b9", "#d68c45"],
    korea: ["#f9dbbd", "#ffa5ab", "#da627d", "#a53860", "#450920"],
    argentina: ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"],
    india: ["#cc5803", "#e2711d", "#ff9505", "#ffb627", "#ffc971"],
    germany: ["#003459", "#007ea7", "#00a8e8"],
  };

  const getCategoryColor = (index) => {
    const palette = localeCategoryPalettes[userLocale] || localeCategoryPalettes['usa'];
    return palette[index % palette.length];
  };

  useEffect(() => {
    async function load() {
      try {
        const userData = await getUserById(id)
        setUser(userData)

        // Set locale from user's rotation city
        if (userData?.rotation_city?.name) {
          const cityName = userData.rotation_city.name.toLowerCase()
          const locale = localeMap[cityName] || 'usa'
          setUserLocale(locale)
        }

        // fetch items contributed by this user
        const userItems = await getUserItems(userData.user_id)
        setItems(userItems || [])
      } catch (err) {
        console.error(err)
        setError(err.message)
      } finally {
        setLoadingItems(false)
      }
    }
    load()
  }, [id])

  // Error UI
  if (error) {
    return (
      <div className="text-red-400 p-10 text-center">
        {error.includes("404")
          ? "User not found."
          : "Failed to load user profile."}
      </div>
    )
  }

  // Loading UI
  if (!user) {
    return (
      <div className="flex justify-center p-10 text-white">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-white" />
      </div>
    )
  }

  return (
    <div className={`locale-container min-h-screen w-full relative flex items-center justify-center ${getLocaleClass()} p-4`}>
      <div className={`locale-overlay absolute inset-0 ${getLocaleClass()}`}></div>
      
      <div className="relative z-10 flex flex-col items-center justify-center w-full max-w-4xl">
        {/* Header Section */}
        <div className="flex flex-col items-center gap-3 mb-8">
          {user?.profile_picture && (
            <div className="w-24 h-24 rounded-full border-3 border-white overflow-hidden flex items-center justify-center">
              <img 
                src={user.profile_picture} 
                alt="Profile" 
                className="w-full h-full object-cover"
              />
            </div>
          )}
          {!user?.profile_picture && (
            <div className="w-24 h-24 rounded-full border-3 border-white bg-white/20 flex items-center justify-center text-white text-3xl">
              👤
            </div>
          )}
          
          <h1 className="text-white text-4xl font-extrabold text-center drop-shadow-md" style={{fontFamily: 'Fraunces, serif'}}>
            {user?.first_name || 'User'}'s Profile
          </h1>
          
          {user?.rotation_city && (
            <span style={{ fontSize: "0.95rem", opacity: 0.95, background: "rgba(255, 255, 255, 0.2)", borderRadius: "20px", padding: "0.5rem 1rem", backdropFilter: "blur(10px)", color: "white", marginTop: "0.5rem" }}>
              {user.rotation_city.name}
            </span>
          )}
        </div>

        {/* Contributions Section */}
        <div className="w-full bg-white/95 rounded-xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3">
            Contributions
            <span className="text-white border-none rounded-lg px-6 py-2 text-base font-semibold" style={{backgroundColor: getLocaleColor()}}>
              {items.length}
            </span>
          </h2>

          {loadingItems ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[1, 2, 3].map(i => (
                <div key={i} className="bg-gray-100 rounded-lg p-4 animate-pulse">
                  <div className="h-5 bg-gray-200 rounded w-3/4 mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/2 mb-3"></div>
                  <div className="flex gap-2">
                    <div className="h-6 bg-gray-200 rounded w-16"></div>
                    <div className="h-6 bg-gray-200 rounded w-16"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : items.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p className="text-lg mb-2">No contributions yet</p>
              <p className="text-sm">{user?.first_name} hasn't added any items to the community</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {items.map((item) => (
                <div
                  key={item.item_id}
                  onClick={() => navigate(`/item/${item.item_id}`)}
                  className="bg-gray-50 border border-gray-200 rounded-lg p-5 cursor-pointer hover:shadow-md hover:border-gray-300 transition-all"
                >
                  <h3 className="font-semibold text-lg text-gray-900 mb-2">
                    {item.name}
                  </h3>

                  <p className="text-gray-600 text-sm mb-3">
                    {item.location}
                  </p>

                  {/* Categories */}
                  {item.categories?.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-3">
                      {item.categories.map((c) => (
                        <span
                          key={c.category_id}
                          className="px-3 py-1 text-xs text-white rounded-lg font-semibold"
                          style={{backgroundColor: getCategoryColor(c.category_id)}}
                        >
                          {c.name}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Tags */}
                  {item.tags?.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-3">
                      {item.tags.map((t) => (
                        <span
                          key={t.tag_id}
                          className="px-2 py-1 text-xs bg-gray-200 text-gray-700 rounded-full"
                        >
                          {t.name}: {t.value}
                        </span>
                      ))}
                    </div>
                  )}

                  <p className="text-xs text-gray-500">
                    ✓ {item.number_of_verifications || 0} verifications
                    {item.created_at && (
                      <> • Added {new Date(item.created_at).toLocaleDateString()}</>
                    )}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}



