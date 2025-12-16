// Page for displaying the logged-in user's profile information

import { useEffect, useState } from "react"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/shared/components/ui/card"
import { Button } from "@/shared/components/ui/button"
import { Field, FieldContent, FieldError, FieldLabel } from "@/shared/components/ui/field"
import { Input } from "@/shared/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/shared/components/ui/select"
import { Spinner } from "@/shared/components/ui/spinner"

import { getCurrentUser, updateUserProfile } from "@/api/user"
import { getCities } from "@/api/cities"
import "@/shared/styles/locale-theme.css"

export default function ProfilePage() {
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [currentLocale, setCurrentLocale] = useState('usa')

  const [cities, setCities] = useState([])
  const [citiesError, setCitiesError] = useState(null)
  const [user, setUser] = useState(null)

  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [rotationCityId, setRotationCityId] = useState("")

  const [message, setMessage] = useState("")
  const [errorMessage, setErrorMessage] = useState("")

  // Profile picture state:
  // - profilePicture: base64 string ready to send to backend (data:image/...;base64,...)
  // - profilePreview: what we show in the UI immediately
  const [profilePicture, setProfilePicture] = useState(null)
  const [profilePreview, setProfilePreview] = useState(null)

  useEffect(() => {
    const locales = ['usa', 'china', 'korea', 'argentina', 'india', 'germany']
    let index = 0

    const cycleLocales = () => {
      index = (index + 1) % locales.length
      setCurrentLocale(locales[index])
      setTimeout(cycleLocales, 8000)
    }

    const timer = setTimeout(cycleLocales, 8000)
    return () => clearTimeout(timer)
  }, [])

  const getLocaleClass = () => {
    const classMap = {
      usa: 'show-photo',
      china: 'transition-green',
      korea: 'transition-korea',
      argentina: 'transition-argentina',
      india: 'transition-india',
      germany: 'transition-germany'
    }
    return classMap[currentLocale] || 'show-photo'
  }

  const getLocaleColor = () => {
    const colorMap = {
      usa: '#cc0000',
      china: '#1d9a5c',
      korea: '#c60c30',
      argentina: '#2a9d8f',
      india: '#ff9933',
      germany: '#4a90e2'
    }
    return colorMap[currentLocale] || '#cc0000'
  }

  // Helper: compress/resize image to keep payload reasonable
  // Returns a DataURL (base64) string.
  const compressImageToDataUrl = (file, opts = {}) => {
    const {
      maxWidth = 512,
      maxHeight = 512,
      quality = 0.8,
    } = opts

    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onerror = () => reject(new Error("Failed to read image file"))
      reader.onload = () => {
        const img = new Image()
        img.onerror = () => reject(new Error("Invalid image file"))
        img.onload = () => {
          let { width, height } = img

          // Preserve aspect ratio within max bounds
          const widthRatio = maxWidth / width
          const heightRatio = maxHeight / height
          const ratio = Math.min(1, widthRatio, heightRatio)

          const targetW = Math.round(width * ratio)
          const targetH = Math.round(height * ratio)

          const canvas = document.createElement("canvas")
          canvas.width = targetW
          canvas.height = targetH

          const ctx = canvas.getContext("2d")
          if (!ctx) {
            reject(new Error("Failed to process image"))
            return
          }

          ctx.drawImage(img, 0, 0, targetW, targetH)

          // Use jpeg for better compression unless it's png and you want transparency.
          // We'll keep original type if possible, otherwise fallback to jpeg.
          const mime =
            file.type === "image/png" ? "image/png" :
            file.type === "image/webp" ? "image/webp" :
            "image/jpeg"

          const dataUrl = canvas.toDataURL(mime, quality)
          resolve(dataUrl)
        }
        img.src = reader.result
      }
      reader.readAsDataURL(file)
    })
  }

  const handleProfilePictureChange = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    setMessage("")
    setErrorMessage("")

    if (!file.type.startsWith("image/")) {
      setErrorMessage("Please upload a valid image file.")
      return
    }

    try {
      // Compress/rescale to reduce size before sending to backend
      const dataUrl = await compressImageToDataUrl(file, {
        maxWidth: 512,
        maxHeight: 512,
        quality: 0.82,
      })

      setProfilePicture(dataUrl)   // what we will save
      setProfilePreview(dataUrl)   // what we show immediately
    } catch (err) {
      console.error(err)
      setErrorMessage("Failed to process image. Please try another file.")
    }
  }

  // Fetch user + cities
  useEffect(() => {
    async function fetchData() {
      try {
        const [userData, citiesData] = await Promise.all([
          getCurrentUser(),
          getCities(),
        ])

        setUser(userData)
        setFirstName(userData.first_name || "")
        setLastName(userData.last_name || "")

        // Keep your existing behavior, but guard for safety
        setRotationCityId(
          userData?.rotation_city?.city_id != null
            ? String(userData.rotation_city.city_id)
            : ""
        )

        setCities(citiesData)

        // Show existing profile picture if available
        if (userData.profile_picture) {
          setProfilePreview(userData.profile_picture)
          // profilePicture stays null unless the user selects a new one
        }
      } catch (err) {
        console.error(err)
        if (err.message?.includes("cities") || err.message?.includes("rotation_city")) {
          setCitiesError("Failed to load cities")
        }
        setErrorMessage("Failed to load profile data")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setErrorMessage("")
    setMessage("")

    try {
      const payload = {
        first_name: firstName,
        last_name: lastName,
        rotation_city_id: Number(rotationCityId),
      }

      // Only send profile_picture if the user selected a new one in this session
      if (profilePicture) {
        payload.profile_picture = profilePicture
      }

      await updateUserProfile(payload)

      setMessage("Profile updated successfully!")

      // Refresh local preview from what we just saved (so UI stays consistent)
      if (profilePicture) {
        setProfilePreview(profilePicture)
        setProfilePicture(null) // reset "pending" state after save
      }
      
      // Dispatch custom event to notify navbar of city change
      window.dispatchEvent(new CustomEvent('cityChanged'))
    } catch (err) {
      console.error(err)
      setErrorMessage("Failed to update profile")
    } finally {
      setSaving(false)
    }
  }

  const handleRetryFetchCities = async () => {
    setCitiesError(null)
    try {
      const citiesData = await getCities()
      setCities(citiesData)
    } catch (err) {
      console.error(err)
      setCitiesError("Failed to load cities")
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-900">
        <Spinner className="w-10 h-10 text-white" />
      </div>
    )
  }

  return (
    <div className={`locale-container min-h-screen w-full relative flex items-center justify-center ${getLocaleClass()} p-4 sm:p-6 md:p-12`}>
      <div className={`locale-overlay absolute inset-0 ${getLocaleClass()}`}></div>
      
      <div className="relative z-10 flex flex-col items-center justify-center w-full max-w-2xl">
        <h1 className="text-white text-5xl sm:text-6xl font-extrabold leading-tight drop-shadow-md text-center mb-8" style={{fontFamily: 'Fraunces, serif'}}>
          My Profile
        </h1>

        {/* Profile Picture (UI + preview) */}
        <div className="flex flex-col items-center gap-3 mb-8">
          <div className="w-28 h-28 rounded-full bg-white/20 overflow-hidden flex items-center justify-center border-2 border-white">
            {profilePreview ? (
              <img
                src={profilePreview}
                alt="Profile"
                className="w-full h-full object-cover"
              />
            ) : (
              <span className="text-white text-sm">No Photo</span>
            )}
          </div>

          <label className="cursor-pointer text-white font-semibold hover:opacity-80 transition">
            Upload profile picture
            <input
              type="file"
              accept="image/*"
              className="hidden"
              onChange={handleProfilePictureChange}
            />
          </label>

          <p className="text-xs text-white/80 text-center">
            Tip: Images are automatically resized/compressed before saving.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="w-full space-y-6">
          {/* Email (cannot change) */}
          <Field>
            <FieldContent>
              <FieldLabel className="text-lg font-semibold text-white">Email</FieldLabel>
              <Input
                type="email"
                value={user?.email || ""}
                disabled
                className="w-full bg-white/10 rounded-full px-6 py-3 text-white/60 cursor-not-allowed backdrop-blur-sm"
              />
            </FieldContent>
          </Field>

          {/* First Name */}
          <Field>
            <FieldContent>
              <FieldLabel className="text-lg font-semibold text-white">First Name</FieldLabel>
              <Input
                type="text"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                className="w-full bg-white rounded-full px-6 py-3 text-gray-800 text-lg placeholder-gray-400 shadow-lg"
              />
            </FieldContent>
          </Field>

          {/* Last Name */}
          <Field>
            <FieldContent>
              <FieldLabel className="text-lg font-semibold text-white">Last Name</FieldLabel>
              <Input
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                className="w-full bg-white rounded-full px-6 py-3 text-gray-800 text-lg placeholder-gray-400 shadow-lg"
              />
            </FieldContent>
          </Field>

          {/* Rotation City */}
          <Field>
            <FieldContent>
              <FieldLabel className="text-lg font-semibold text-white">Rotation City</FieldLabel>
              {citiesError ? (
                <div className="space-y-2">
                  <p className="text-white text-sm">{citiesError}</p>
                  <Button
                    type="button"
                    onClick={handleRetryFetchCities}
                    className="w-full bg-white/20 hover:bg-white/30 text-white border-white rounded-full"
                  >
                    Retry Loading Cities
                  </Button>
                </div>
              ) : (
                <Select
                  value={rotationCityId}
                  onValueChange={(v) => setRotationCityId(v)}
                >
                  <SelectTrigger className="w-full bg-white rounded-full px-6 py-3 text-gray-800 shadow-lg">
                    <SelectValue placeholder="Choose a city" />
                  </SelectTrigger>

                  <SelectContent className="bg-white border-white text-gray-800">
                    {cities.map((c) => (
                      <SelectItem key={c.city_id} value={String(c.city_id)}>
                        {c.name || "Unknown City"}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            </FieldContent>
          </Field>

          {errorMessage && <p className="text-white text-sm">{errorMessage}</p>}

          {message && <p className="text-green-200 text-sm font-semibold">{message}</p>}

          <Button
            type="submit"
            className="w-full rounded-full px-6 py-3 bg-white font-semibold shadow-lg"
            style={{ color: getLocaleColor() }}
            disabled={saving}
          >
            {saving && <Spinner className="mr-2" />}
            Save Changes
          </Button>
        </form>
      </div>
    </div>
  )
}


