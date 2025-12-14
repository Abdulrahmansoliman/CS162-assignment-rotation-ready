import { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { apiFetch } from "@/api"
import { Spinner } from "@/shared/components/ui/spinner"
import { Button } from "@/shared/components/ui/button"

export default function ItemDetailsPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [item, setItem] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function fetchItem() {
      try {
        const data = await apiFetch(`/item/${id}`)
        setItem(data)
      } catch (err) {
        setError("Unable to load item details")
      } finally {
        setLoading(false)
      }
    }
    fetchItem()
  }, [id])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
        <Spinner className="w-10 h-10" />
      </div>
    )
  }

  if (error || !item) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-900 text-white gap-4 px-6">
        <p className="text-lg font-semibold">{error || "Item not found"}</p>
        <Button onClick={() => navigate(-1)} className="bg-white text-slate-900 hover:bg-slate-100">Go Back</Button>
      </div>
    )
  }

  const priceLevel = item.price_level || 1
  const verifiedCount = item.verified_count || 0
  const lastVerified = item.last_verified || "N/A"
  const tags = item.tags || []

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-8 py-10">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight">{item.name}</h1>
          <Button onClick={() => navigate(-1)} className="bg-white text-slate-900 hover:bg-slate-100">Back</Button>
        </div>

        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 shadow-xl border border-white/10">
          <div className="space-y-3">
            <div className="text-lg font-semibold">{item.location}</div>
            {item.walking_distance && (
              <div className="text-slate-200 text-sm">{(item.walking_distance / 1000).toFixed(1)} km away</div>
            )}
          </div>

          <div className="mt-6 flex flex-wrap gap-2">
            {tags.length > 0 ? tags.map((tag, idx) => (
              <span key={idx} className="px-3 py-1 rounded-full bg-white/15 border border-white/10 text-sm font-semibold">
                {tag.name}: {tag.value}
              </span>
            )) : (
              <span className="text-sm text-slate-200">No tags provided</span>
            )}
          </div>

          <div className="mt-6 flex items-center gap-4 text-sm text-slate-100">
            <div className="flex items-center gap-2">
              <span className="font-semibold">Price:</span>
              <span className="text-lg font-bold">{"$".repeat(priceLevel)}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="font-semibold">Verified:</span>
              <span>{verifiedCount} checks</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="font-semibold">Last verified:</span>
              <span>{lastVerified}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
