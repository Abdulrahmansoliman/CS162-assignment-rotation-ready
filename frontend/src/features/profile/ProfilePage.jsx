import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/shared/components/ui/card"
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
  const [user, setUser] = useState(null)

  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [rotationCityId, setRotationCityId] = useState("")

  const [message, setMessage] = useState("")
  const [errorMessage, setErrorMessage] = useState("")

  // Fetch user + cities
  useEffect(() => {
    async function fetchData() {
      try {
        const [userData, citiesData] = await Promise.all([
          getCurrentUser(),
          getCities(),
        ])

        setUser(userData)
        setFirstName(userData.first_name)
        setLastName(userData.last_name)
        setRotationCityId(String(userData.rotation_city.city_id))
        setCities(citiesData)

      } catch (err) {
        console.error(err)
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
      await updateUserProfile({
        first_name: firstName,
        last_name: lastName,
        rotation_city_id: Number(rotationCityId),
      })

      setMessage("Profile updated successfully!")
    } catch (err) {
      console.error(err)
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

        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-6 sm:space-y-7">

            {/* Email (cannot change) */}
            <Field>
              <FieldContent>
                <FieldLabel className="text-slate-200">Email</FieldLabel>
                <Input
                  type="email"
                  value={user.email}
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
                        {c.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </FieldContent>
            </Field>

            {errorMessage && (
              <FieldError errors={[{ message: errorMessage }]} />
            )}

            {message && (
              <p className="text-green-400 mt-2 text-sm">{message}</p>
            )}

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

