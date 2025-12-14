import { useEffect, useMemo, useState } from "react"
import { useNavigate } from "react-router-dom"
import { Button } from "@/shared/components/ui/button"
import { Field, FieldContent, FieldError, FieldLabel } from "@/shared/components/ui/field"
import { Input } from "@/shared/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/shared/components/ui/select"
import { Spinner } from "@/shared/components/ui/spinner"

import { getCurrentUser, updateUserProfile } from "@/api/user"
import { getCities } from "@/api/cities"

export default function ProfilePage() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [pressed, setPressed] = useState(false)

  const [cities, setCities] = useState([])
  const [user, setUser] = useState(null)

  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [rotationCityId, setRotationCityId] = useState("")
  const [currentLocale, setCurrentLocale] = useState("usa")

  const [message, setMessage] = useState("")
  const [errorMessage, setErrorMessage] = useState("")

  const cityToLocaleMap = useMemo(() => ({
    1: "usa",
    2: "china",
    3: "korea",
    4: "argentina",
    5: "india",
    6: "germany",
  }), [])

  const getLocaleClass = () => {
    const classMap = {
      usa: "show-photo",
      china: "transition-green",
      korea: "transition-korea",
      argentina: "transition-argentina",
      india: "transition-india",
      germany: "transition-germany",
    }
    return classMap[currentLocale] || "show-photo"
  }

  const getLocaleColor = () => {
    const colorMap = {
      usa: "#cc0000",
      china: "#6fbec7",
      korea: "#d67ab1",
      argentina: "#e9ae42",
      india: "#cc5803",
      germany: "#42481c",
    }
    return colorMap[currentLocale] || "#cc0000"
  }

  const buttonStyle = (isPressed) => ({
    background: isPressed ? getLocaleColor() : "#fff",
    color: isPressed ? "#fff" : getLocaleColor(),
  })

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
        setCurrentLocale(cityToLocaleMap[userData.rotation_city.city_id] || "usa")

      } catch (err) {
        console.error(err)
        setErrorMessage("Failed to load profile data")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [cityToLocaleMap])

  useEffect(() => {
    if (!rotationCityId) return
    const locale = cityToLocaleMap[Number(rotationCityId)] || "usa"
    setCurrentLocale(locale)
  }, [rotationCityId, cityToLocaleMap])

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
      navigate("/")
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
    <>
      <style>{`
        .profile-container {
          background: linear-gradient(135deg, #cc0000 0%, #ff4444 100%);
          background-size: cover;
          background-position: center;
          transition: background-image 0.8s ease-out, background 0.8s ease-out;
        }

        .profile-container.show-photo {
          background-image: url('/sf.jpg');
          background-size: cover;
          background-position: center;
          background-blend-mode: overlay;
        }

        .profile-container.transition-green {
          background: linear-gradient(135deg, #1d9a5c 0%, #2fb872 100%) !important;
          background-image: url('/tp.jpg') !important;
          background-size: 120% !important;
          background-repeat: no-repeat !important;
          background-position: center;
          background-blend-mode: overlay;
        }

        .profile-container.transition-korea {
          background: linear-gradient(135deg, #c60c30 0%, #e91e63 100%) !important;
          background-image: url('/sl.jpg') !important;
          background-size: cover !important;
          background-position: center;
          background-blend-mode: overlay;
        }

        .profile-container.transition-argentina {
          background: linear-gradient(135deg, #6d70bd 0%, #8b6fc3 100%) !important;
          background-image: url('/ba.jpg') !important;
          background-size: cover !important;
          background-position: center;
          background-blend-mode: overlay;
        }

        .profile-container.transition-india {
          background: linear-gradient(135deg, #ff9933 0%, #ffcc33 100%) !important;
          background-image: url('/hyd.jpg') !important;
          background-size: cover !important;
          background-position: center;
          background-blend-mode: overlay;
        }

        .profile-container.transition-germany {
          background: linear-gradient(135deg, #4a90e2 0%, #7bb3e8 100%) !important;
          background-image: url('/br.jpg') !important;
          background-size: cover !important;
          background-position: center;
          background-blend-mode: overlay;
        }

        .profile-overlay {
          background-color: rgba(204, 0, 0, 0.8);
          transition: background-color 0.8s ease-out;
        }

        .profile-overlay.show-photo {
          background-color: rgba(204, 0, 0, 0.5);
        }

        .profile-overlay.transition-green {
          background-color: rgba(29, 154, 92, 0.7) !important;
        }

        .profile-overlay.transition-korea {
          background-color: rgba(198, 12, 48, 0.6) !important;
        }

        .profile-overlay.transition-argentina {
          background-color: rgba(233, 174, 66, 0.62) !important;
        }

        .profile-overlay.transition-india {
          background-color: rgba(255, 153, 51, 0.62) !important;
        }

        .profile-overlay.transition-germany {
          background-color: rgba(122, 179, 232, 0.65) !important;
        }
      `}</style>

      <div className={`profile-container min-h-screen w-full relative flex items-center justify-center ${getLocaleClass()}`}>
        <div className={`profile-overlay absolute inset-0 ${getLocaleClass()}`}></div>

        <div className="relative z-10 flex flex-col items-center justify-center w-full px-6 sm:px-12 max-w-3xl">
          <h1 className="text-white text-4xl sm:text-6xl font-extrabold leading-tight drop-shadow-md text-center mb-6" style={{ fontFamily: "Georgia, serif" }}>
            My Profile
          </h1>
          <p className="text-white/90 text-center text-xs sm:text-sm mb-6 max-w-2xl">
            Update your personal information and rotation city. Changes update instantly without leaving this page.
          </p>

          <form onSubmit={handleSubmit} className="w-full flex flex-col items-center">
            <div className="w-full max-w-2xl space-y-6">

              {/* Email (cannot change) */}
              <Field>
                <FieldContent>
                  <FieldLabel className="text-lg font-semibold text-white">Email</FieldLabel>
                  <Input
                    type="email"
                    value={user.email}
                    disabled
                    className="bg-white/70 rounded-full px-8 py-4 text-gray-500 text-lg placeholder-gray-400 shadow-lg cursor-not-allowed"
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
                    className="bg-white rounded-full px-8 py-4 text-gray-800 text-lg placeholder-gray-400 shadow-lg"
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
                    className="bg-white rounded-full px-8 py-4 text-gray-800 text-lg placeholder-gray-400 shadow-lg"
                  />
                </FieldContent>
              </Field>

              {/* Rotation City */}
              <Field>
                <FieldContent>
                  <FieldLabel className="text-lg font-semibold text-white">Rotation City</FieldLabel>
                  <Select
                    value={rotationCityId}
                    onValueChange={(v) => setRotationCityId(v)}
                  >
                    <SelectTrigger className="bg-white rounded-full px-8 py-4 text-gray-800 text-lg placeholder-gray-400 shadow-lg">
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
                </FieldContent>
              </Field>

              {errorMessage && (
                <FieldError errors={[{ message: errorMessage }]} />
              )}

              {message && (
                <p className="text-white font-semibold mt-2 text-sm">{message}</p>
              )}

            </div>

            <div className="mt-8 w-full max-w-2xl">
              <Button
                type="submit"
                className="rounded-full px-6 py-3 font-semibold shadow-lg w-full"
                style={buttonStyle(pressed)}
                onMouseDown={() => setPressed(true)}
                onMouseUp={() => setPressed(false)}
                onMouseLeave={() => setPressed(false)}
                disabled={saving}
              >
                {saving ? <Spinner className="mr-2" /> : "Save Changes"}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </>
  )
}

