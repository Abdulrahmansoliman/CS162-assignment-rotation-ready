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

export default function ProfilePage() {
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

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
    <div className="flex min-h-screen items-center justify-center bg-slate-900 p-4 sm:p-6 md:p-12">
      <Card className="w-full max-w-md sm:max-w-lg lg:max-w-xl bg-slate-800/90 backdrop-blur-sm border-slate-700 shadow-xl">
        <CardHeader className="space-y-3 text-center">
          <CardTitle className="text-3xl font-bold text-white">
            My Profile
          </CardTitle>
          <CardDescription className="text-slate-300 text-sm sm:text-base">
            Update your personal information and rotation city.
          </CardDescription>
        </CardHeader>

        {/* Profile Picture (UI + preview) */}
        <div className="flex flex-col items-center gap-3 px-6 pb-2">
          <div className="w-28 h-28 rounded-full bg-slate-700 overflow-hidden flex items-center justify-center border border-slate-600">
            {profilePreview ? (
              <img
                src={profilePreview}
                alt="Profile"
                className="w-full h-full object-cover"
              />
            ) : (
              <span className="text-slate-300 text-sm">No Photo</span>
            )}
          </div>

          <label className="cursor-pointer text-sm text-blue-400 hover:underline">
            Upload profile picture
            <input
              type="file"
              accept="image/*"
              className="hidden"
              onChange={handleProfilePictureChange}
            />
          </label>

          <p className="text-xs text-slate-400 text-center">
            Tip: Images are automatically resized/compressed before saving.
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-6 sm:space-y-7">
            {/* Email (cannot change) */}
            <Field>
              <FieldContent>
                <FieldLabel className="text-slate-200">Email</FieldLabel>
                <Input
                  type="email"
                  value={user?.email || ""}
                  disabled
                  className="w-full h-12 bg-slate-700/40 border-slate-600 text-slate-400 cursor-not-allowed"
                />
              </FieldContent>
            </Field>

            {/* First Name */}
            <Field>
              <FieldContent>
                <FieldLabel className="text-slate-200">First Name</FieldLabel>
                <Input
                  type="text"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  className="w-full h-12 bg-slate-700/50 border-slate-600 text-white"
                />
              </FieldContent>
            </Field>

            {/* Last Name */}
            <Field>
              <FieldContent>
                <FieldLabel className="text-slate-200">Last Name</FieldLabel>
                <Input
                  type="text"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  className="w-full h-12 bg-slate-700/50 border-slate-600 text-white"
                />
              </FieldContent>
            </Field>

            {/* Rotation City */}
            <Field>
              <FieldContent>
                <FieldLabel className="text-slate-200">Rotation City</FieldLabel>
                {citiesError ? (
                  <div className="space-y-2">
                    <p className="text-red-400 text-sm">{citiesError}</p>
                    <Button
                      type="button"
                      variant="outline"
                      onClick={handleRetryFetchCities}
                      className="w-full bg-slate-700/50 hover:bg-slate-700 text-white border-slate-600"
                    >
                      Retry Loading Cities
                    </Button>
                  </div>
                ) : (
                  <Select
                    value={rotationCityId}
                    onValueChange={(v) => setRotationCityId(v)}
                  >
                    <SelectTrigger className="w-full h-12 bg-slate-700/50 border-slate-600 text-white">
                      <SelectValue placeholder="Choose a city" />
                    </SelectTrigger>

                    <SelectContent className="bg-slate-800 border-slate-700 text-white">
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

            {errorMessage && <FieldError errors={[{ message: errorMessage }]} />}

            {message && <p className="text-green-400 mt-2 text-sm">{message}</p>}
          </CardContent>

          <CardFooter className="pt-4">
            <Button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 h-12 text-white font-semibold"
              disabled={saving}
            >
              {saving && <Spinner className="mr-2" />}
              Save Changes
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}


