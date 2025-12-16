// Page for viewing another user's public profile

import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"

import { getUserById } from "@/api/otherUser"
import { getUserItems } from "@/api/item"

export default function ViewUserProfilePage() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [user, setUser] = useState(null)
  const [items, setItems] = useState([])
  const [loadingItems, setLoadingItems] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const userData = await getUserById(id)
        setUser(userData)

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
    <div className="flex justify-center p-10 text-white">
      <div className="w-[700px] bg-gray-900 p-8 rounded-xl shadow-xl">

        {/* Back Button */}
        <button
          onClick={() => navigate(-1)}
          className="text-blue-400 hover:underline mb-6"
        >
          ← Back
        </button>

        {/* User Info */}
        <div className="flex items-center gap-5 mb-8">
          <div className="w-24 h-24 rounded-full bg-gray-700 overflow-hidden flex items-center justify-center">
            {user.profile_picture ? (
              <img
                src={user.profile_picture}
                alt="Profile"
                className="w-full h-full object-cover"
              />
            ) : (
              <span className="text-gray-400 text-sm">No Photo</span>
            )}
          </div>

          <div>
            <h1 className="text-2xl font-bold">
              {user.first_name} {user.last_name}
            </h1>

            <p className="text-gray-400 text-sm mb-1">
              Viewing public profile information
            </p>

            <p className="text-gray-400">{user.email}</p>
            <p className="text-gray-400">
              City: {user.rotation_city?.name || "Unknown"}
            </p>
          </div>
        </div>

        {/* Contributions */}
        <h2 className="text-xl font-semibold mb-4">
          Contributions
          <span className="ml-2 px-2 py-1 text-sm bg-blue-600/20 text-blue-300 rounded">
            {items.length}
          </span>
        </h2>

        {loadingItems ? (
          <div className="grid grid-cols-1 gap-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="bg-gray-800 rounded-lg p-4 animate-pulse">
                <div className="h-5 bg-gray-700 rounded w-3/4 mb-2"></div>
                <div className="h-4 bg-gray-700 rounded w-1/2 mb-3"></div>
                <div className="flex gap-2">
                  <div className="h-6 bg-gray-700 rounded w-16"></div>
                  <div className="h-6 bg-gray-700 rounded w-16"></div>
                </div>
              </div>
            ))}
          </div>
        ) : items.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📦</div>
            <p className="text-gray-400 text-lg mb-2">No contributions yet</p>
            <p className="text-gray-500 text-sm">
              {user.first_name} hasn't added any items to the community
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {items.map((item) => (
              <div
                key={item.item_id}
                onClick={() => navigate(`/item/${item.item_id}`)}
                className="bg-gray-800 border border-gray-700 rounded-lg p-4 cursor-pointer hover:bg-gray-750 hover:border-gray-600 transition-all"
              >
                <h3 className="font-semibold text-lg">
                  {item.name}
                </h3>

                <p className="text-gray-400 text-sm">
                  {item.location}
                </p>

                {/* Categories */}
                {item.categories?.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-3">
                    {item.categories.map((c) => (
                      <span
                        key={c.category_id}
                        className="px-2 py-1 text-xs rounded bg-blue-600/20 text-blue-300"
                      >
                        {c.name}
                      </span>
                    ))}
                  </div>
                )}

                {/* Tags */}
                {item.tags?.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {item.tags.map((t) => (
                      <span
                        key={t.tag_id}
                        className="px-2 py-1 text-xs rounded bg-gray-700 text-gray-300"
                      >
                        {t.name}: {t.value}
                      </span>
                    ))}
                  </div>
                )}

                <p className="text-xs text-gray-400 mt-3">
                  ✔ {item.number_of_verifications || 0} verifications
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
  )
}



