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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/shared/components/ui/select"
import { Spinner } from "@/shared/components/ui/spinner"

import { getCurrentUser, updateUserProfile } from "@/api/user"
import { getCities } from "@/api/cities"
import { getUserItems } from "@/api/item"

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

  // Profile picture
  const [profilePicture, setProfilePicture] = useState(null)
  const [profilePreview, setProfilePreview] = useState(null)

  // Contributions
  const [items, setItems] = useState([])
  const [itemsLoading, setItemsLoading] = useState(true)

  // Image compression helper
  const compressImageToDataUrl = (file) =>
    new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => {
        const img = new Image()
        img.onload = () => {
          const maxSize = 512
          const scale = Math.min(maxSize / img.width, maxSize / img.height, 1)

          const canvas = document.createElement("canvas")
          canvas.width = img.width * scale
          canvas.height = img.height * scale

          const ctx = canvas.getContext("2d")
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height)

          resolve(canvas.toDataURL("image/jpeg", 0.82))
        }
        img.onerror = reject
        img.src = reader.result
      }
      reader.onerror = reject
      reader.readAsDataURL(file)
    })

  const handleProfilePictureChange = async (e) => {
    const file = e.target.files?.[0]
    if (!file || !file.type.startsWith("image/")) return

    try {
      const dataUrl = await compressImageToDataUrl(file)
      setProfilePicture(dataUrl)
      setProfilePreview(dataUrl)
    } catch {
      setErrorMessage("Failed to process image.")
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
        setRotationCityId(
          userData?.rotation_city?.city_id
            ? String(userData.rotation_city.city_id)
            : ""
        )
        setCities(citiesData)

        if (userData.profile_picture) {
          setProfilePreview(userData.profile_picture)
        }
      } catch (err) {
        console.error(err)
        setErrorMessage("Failed to load profile data")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // Fetch user items
  useEffect(() => {
    if (!user?.user_id) return

    async function fetchItems() {
      try {
        const data = await getUserItems(user.user_id)
        setItems(data)
      } catch (err) {
        console.error("Failed to load user items", err)
      } finally {
        setItemsLoading(false)
      }
    }

    fetchItems()
  }, [user])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setMessage("")
    setErrorMessage("")

    try {
      const payload = {
        first_name: firstName,
        last_name: lastName,
        rotation_city_id: Number(rotationCityId),
      }

      if (profilePicture) {
        payload.profile_picture = profilePicture
      }

      await updateUserProfile(payload)
      setMessage("Profile updated successfully!")

      if (profilePicture) {
        setProfilePicture(null)
      }
    } catch {
      setErrorMessage("Failed to update profile")
    } finally {
      setSaving(false)
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
    <div className="flex min-h-screen flex-col items-center bg-slate-900 p-6">
      {/* PROFILE CARD */}
      <Card className="w-full max-w-xl bg-slate-800 border-slate-700 shadow-xl">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl text-white">My Profile</CardTitle>
          <CardDescription className="text-slate-300">
            Update your personal information and rotation city.
          </CardDescription>
        </CardHeader>

        <div className="flex flex-col items-center gap-3 pb-4">
          <div className="w-28 h-28 rounded-full overflow-hidden bg-slate-700 border">
            {profilePreview ? (
              <img
                src={profilePreview}
                alt="Profile"
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="flex items-center justify-center h-full text-slate-400">
                No Photo
              </div>
            )}
          </div>

          <label className="cursor-pointer text-blue-400 text-sm hover:underline">
            Upload profile picture
            <input
              type="file"
              accept="image/*"
              className="hidden"
              onChange={handleProfilePictureChange}
            />
          </label>
        </div>

        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-5">
            <Field>
              <FieldLabel>Email</FieldLabel>
              <Input disabled value={user.email} />
            </Field>

            <Field>
              <FieldLabel>First Name</FieldLabel>
              <Input value={firstName} onChange={(e) => setFirstName(e.target.value)} />
            </Field>

            <Field>
              <FieldLabel>Last Name</FieldLabel>
              <Input value={lastName} onChange={(e) => setLastName(e.target.value)} />
            </Field>

            <Field>
              <FieldLabel>Rotation City</FieldLabel>
              <Select value={rotationCityId} onValueChange={setRotationCityId}>
                <SelectTrigger>
                  <SelectValue placeholder="Choose a city" />
                </SelectTrigger>
                <SelectContent>
                  {cities.map((c) => (
                    <SelectItem key={c.city_id} value={String(c.city_id)}>
                      {c.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Field>

            {errorMessage && <FieldError errors={[{ message: errorMessage }]} />}
            {message && <p className="text-green-400 text-sm">{message}</p>}
          </CardContent>

          <CardFooter>
            <Button type="submit" disabled={saving} className="w-full">
              {saving && <Spinner className="mr-2" />}
              Save Changes
            </Button>
          </CardFooter>
        </form>
      </Card>

      {/* MY CONTRIBUTIONS */}
      <Card className="mt-8 w-full max-w-4xl bg-slate-800 border-slate-700 shadow-xl">
        <CardHeader>
          <CardTitle className="text-xl text-white">
            My Contributions ({items.length})
          </CardTitle>
        </CardHeader>

        <CardContent>
          {itemsLoading ? (
            <div className="flex justify-center py-8">
              <Spinner />
            </div>
          ) : items.length === 0 ? (
            <div className="text-center text-slate-400 py-10">
              <p>No items yet.</p>
              <Button
                className="mt-4"
                onClick={() => (window.location.href = "/add-item")}
              >
                Add your first item
              </Button>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 gap-6">
              {items.map((item, i) => (
                <div
                  key={i}
                  className="p-4 rounded-lg bg-slate-900 border border-slate-700 space-y-3"
                >
                  <div>
                    <h3 className="text-lg text-white font-semibold">
                      {item.name}
                    </h3>
                    <p className="text-sm text-slate-400">{item.location}</p>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {item.categories.map((c) => (
                      <span
                        key={c.category_id}
                        className="text-xs px-2 py-1 rounded bg-slate-700 text-white"
                      >
                        {c.name}
                      </span>
                    ))}
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {item.tags.map((t) => (
                      <span
                        key={t.tag_id}
                        className="text-xs px-2 py-1 rounded bg-blue-600/20 text-blue-300"
                      >
                        {t.name}: {t.value}
                      </span>
                    ))}
                  </div>

                  <p className="text-sm text-slate-400">
                    ✔ {item.number_of_verifications} verifications
                  </p>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}









