import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { Button } from "@/shared/components/ui/button"
import { Field, FieldContent, FieldDescription, FieldError, FieldLabel } from "@/shared/components/ui/field"
import { Input } from "@/shared/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/shared/components/ui/select"
import { Spinner } from "@/shared/components/ui/spinner"
import { useSignup } from "../hooks/useSignup"
import { useVerification } from "../hooks/useVerification"
import { getCities } from "@/api/cities"

const animationStyles = `
  @keyframes letterFlyIn {
    from {
      opacity: 0;
      transform: translateX(-60px) translateY(-40px) rotateZ(-15deg);
    }
    to {
      opacity: 1;
      transform: translateX(0) translateY(0) rotateZ(0deg);
    }
  }

  @keyframes fadeInSlideUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .letter {
    display: inline-block;
  }

  .fade-in {
    animation: fadeInSlideUp 0.8s ease-out 1.2s forwards;
    opacity: 0;
  }

  .signup-container {
    background: linear-gradient(135deg, #cc0000 0%, #ff4444 100%);
    background-size: cover;
    background-position: center;
    transition: background-image 0.8s ease-out, background 0.8s ease-out;
  }

  .signup-container.show-photo {
    background-image: url('/sf.jpg');
    background-size: cover;
    background-position: center;
    background-blend-mode: overlay;
  }

  .signup-container.transition-green {
    background: linear-gradient(135deg, #1d9a5c 0%, #2fb872 100%) !important;
    background-image: url('/tp.jpg') !important;
    background-size: 120% !important;
    background-repeat: no-repeat !important;
    background-position: center;
    background-blend-mode: overlay;
  }

  .signup-container.transition-korea {
    background: linear-gradient(135deg, #c60c30 0%, #e91e63 100%) !important;
    background-image: url('/sl.jpg') !important;
    background-size: cover !important;
    background-position: center;
    background-blend-mode: overlay;
  }

  .signup-container.transition-argentina {
    background: linear-gradient(135deg, #6d70bd 0%, #8b6fc3 100%) !important;
    background-image: url('/ba.jpg') !important;
    background-size: cover !important;
    background-position: center;
    background-blend-mode: overlay;
  }

  .signup-container.transition-india {
    background: linear-gradient(135deg, #ff9933 0%, #ffcc33 100%) !important;
    background-image: url('/hyd.jpg') !important;
    background-size: cover !important;
    background-position: center;
    background-blend-mode: overlay;
  }

  .signup-container.transition-germany {
    background: linear-gradient(135deg, #4a90e2 0%, #7bb3e8 100%) !important;
    background-image: url('/br.jpg') !important;
    background-size: cover !important;
    background-position: center;
    background-blend-mode: overlay;
  }

  .overlay {
    background-color: rgba(204, 0, 0, 0.8);
    transition: background-color 0.8s ease-out;
  }

  .overlay.show-photo {
    background-color: rgba(204, 0, 0, 0.5);
  }

  .overlay.transition-green {
    background-color: rgba(29, 154, 92, 0.7) !important;
  }

  .overlay.transition-korea {
    background-color: rgba(198, 12, 48, 0.6) !important;
  }

  .overlay.transition-argentina {
    background-color: rgba(233, 174, 66, 0.62) !important;
  }

  .overlay.transition-india {
    background-color: rgba(255, 153, 51, 0.62) !important;
  }

  .overlay.transition-germany {
    background-color: rgba(122, 179, 232, 0.65) !important;
  }
`

const ROTATION_CITIES = [] // This line is no longer needed, cities will be fetched

export default function SignupPage() {
  const [isWaitingForOtp, setIsWaitingForOtp] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(0)
  const [currentLocale, setCurrentLocale] = useState('usa')
  const [pressed, setPressed] = useState({ main: false, verify: false })
  const [rotationCities, setRotationCities] = useState([])
  const [citiesLoading, setCitiesLoading] = useState(true)
  const [citiesError, setCitiesError] = useState("")
  const signup = useSignup()
  const verification = useVerification(signup.formData.email)

  // Map city_id to locale
  const cityToLocaleMap = {
    1: 'usa',
    2: 'china',
    3: 'korea',
    4: 'argentina',
    5: 'india',
    6: 'germany'
  }

  useEffect(() => {
    const loadCities = async () => {
      try {
        const cities = await getCities()
        setRotationCities(cities)
      } catch (error) {
        console.error('Failed to fetch cities:', error)
        setRotationCities([])
        setCitiesError("Failed to load rotation cities from server")
      } finally {
        setCitiesLoading(false)
      }
    }
    loadCities()
  }, [])

  // Update locale when city is selected
  useEffect(() => {
    if (signup.formData.cityId) {
      const selectedLocale = cityToLocaleMap[signup.formData.cityId] || 'usa'
      setCurrentLocale(selectedLocale)
    }
  }, [signup.formData.cityId])

  const handleRegister = async (e) => {
    e.preventDefault()
    const result = await signup.handleSubmit()
    if (result.success) {
      setIsWaitingForOtp(true)
    }
  }

  const handleVerify = async (e) => {
    e.preventDefault()
    await verification.handleSubmit()
  }

  const handleBackToRegistration = () => {
    setIsWaitingForOtp(false)
    setResendCooldown(0)
    verification.reset()
  }

  const handleResendWithCooldown = async () => {
    await verification.handleResendCode()
    setResendCooldown(60)
    
    const interval = setInterval(() => {
      setResendCooldown((prev) => {
        if (prev <= 1) {
          clearInterval(interval)
          return 0
        }
        return prev - 1
      })
    }, 1000)
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
    return classMap[currentLocale] || 'show-photo'
  }

  const getLocaleColor = () => {
    const colorMap = {
      usa: '#cc0000',
      china: '#6fbec7',
      korea: '#d67ab1',
      argentina: '#e9ae42',
      india: '#cc5803',
      germany: '#42481c'
    }
    return colorMap[currentLocale] || '#cc0000'
  }

  const getLocaleText = () => {
    const textMap = {
      usa: 'Welcome',
      china: '欢迎',
      korea: '어서 오세요',
      argentina: 'Bienvenido',
      india: 'స్వాగతం',
      germany: 'Willkommen'
    }
    return textMap[currentLocale] || 'Welcome'
  }

  const shouldSplitLetters = () => {
    return currentLocale !== 'india'
  }

  const buttonStyle = (isPressed) => ({
    background: isPressed ? getLocaleColor() : '#fff',
    color: isPressed ? '#fff' : getLocaleColor()
  })

  return (
    <>
      <style>{animationStyles}</style>
      <div className={`signup-container min-h-screen w-full relative flex items-center justify-center ${getLocaleClass()}`}>
        <div className={`overlay absolute inset-0 ${getLocaleClass()}`}></div>

        <div className="relative z-10 flex flex-col items-center justify-center w-full px-6 sm:px-12 max-w-3xl">
          <h1 className="text-white text-5xl sm:text-7xl font-extrabold leading-tight drop-shadow-md text-center mb-8" style={{fontFamily: 'Georgia, serif'}}>
            {shouldSplitLetters() ? (
              getLocaleText().split('').map((letter, index) => (
                <span key={index} className={`letter letter-${index}`}>
                  {letter}
                </span>
              ))
            ) : (
              <span className="letter letter-0">{getLocaleText()}</span>
            )}
          </h1>

          {signup.errors.submit && (
            <div className="text-sm text-white">{signup.errors.submit}</div>
          )}
          {!isWaitingForOtp ? (
            <form onSubmit={handleRegister} className="fade-in w-full flex flex-col items-center">
              <div className="w-full max-w-2xl space-y-6">
                <Field>
                  <FieldContent>
                    <FieldLabel htmlFor="firstName" className="text-lg font-semibold text-white">First Name</FieldLabel>
                    <Input
                      id="firstName"
                      type="text"
                      placeholder="John"
                      value={signup.formData.firstName}
                      onChange={(e) => signup.handleChange("firstName", e.target.value)}
                      disabled={signup.isLoading}
                      required
                      className="bg-white rounded-full px-8 py-4 text-gray-800 text-lg placeholder-gray-400 shadow-lg"
                    />
                    <FieldError errors={signup.errors.firstName ? [{ message: signup.errors.firstName }] : null} />
                  </FieldContent>
                </Field>

                <Field>
                  <FieldContent>
                    <FieldLabel htmlFor="lastName" className="text-lg font-semibold text-white">Last Name</FieldLabel>
                    <Input
                      id="lastName"
                      type="text"
                      placeholder="Doe"
                      value={signup.formData.lastName}
                      onChange={(e) => signup.handleChange("lastName", e.target.value)}
                      disabled={signup.isLoading}
                      required
                      className="bg-white rounded-full px-8 py-4 text-gray-800 text-lg placeholder-gray-400 shadow-lg"
                    />
                    <FieldError errors={signup.errors.lastName ? [{ message: signup.errors.lastName }] : null} />
                  </FieldContent>
                </Field>

                <Field>
                  <FieldContent>
                    <FieldLabel htmlFor="email" className="text-lg font-semibold text-white">Email</FieldLabel>
                    <Input
                      id="email"
                      type="email"
                      placeholder="john@example.com"
                      value={signup.formData.email}
                      onChange={(e) => signup.handleChange("email", e.target.value)}
                      disabled={signup.isLoading}
                      required
                      className="bg-white rounded-full px-8 py-4 text-gray-800 text-lg placeholder-gray-400 shadow-lg"
                    />
                    <FieldError errors={signup.errors.email ? [{ message: signup.errors.email }] : null} />
                  </FieldContent>
                </Field>

                <Field>
                  <FieldContent>
                    <FieldLabel htmlFor="city" className="text-lg font-semibold text-white">Rotation City</FieldLabel>
                    <Select value={signup.formData.cityId} onValueChange={(value) => signup.handleChange("cityId", value)}>
                      <SelectTrigger className="bg-white rounded-full px-8 py-4 text-gray-800 text-lg placeholder-gray-400 shadow-lg">
                        <SelectValue placeholder={citiesLoading ? "Loading cities..." : (citiesError ? citiesError : "Select a city")} />
                      </SelectTrigger>
                      <SelectContent>
                        {citiesLoading ? (
                          <div className="px-4 py-2 text-gray-500">Loading...</div>
                        ) : (
                          rotationCities.map((city) => (
                            <SelectItem key={city.city_id} value={String(city.city_id)}>
                              {city.name}
                            </SelectItem>
                          ))
                        )}
                      </SelectContent>
                    </Select>
                    {citiesError && (
                      <div className="mt-2 text-sm text-white">{citiesError}</div>
                    )}
                    <FieldError errors={signup.errors.cityId ? [{ message: signup.errors.cityId }] : null} />
                  </FieldContent>
                </Field>
              </div>

              <div className="mt-8 w-full max-w-2xl flex items-center justify-between">
                <div className="text-white text-sm font-medium whitespace-nowrap">
                  Have an account? <Link to="/login" className="underline hover:opacity-80 transition">Sign in</Link>
                </div>
                <Button
                  type="submit"
                  className="rounded-full px-6 py-3 font-semibold shadow-lg whitespace-nowrap"
                  style={buttonStyle(pressed.main)}
                  onMouseDown={() => setPressed(p => ({ ...p, main: true }))}
                  onMouseUp={() => setPressed(p => ({ ...p, main: false }))}
                  onMouseLeave={() => setPressed(p => ({ ...p, main: false }))}
                  disabled={signup.isLoading || citiesLoading || rotationCities.length === 0}
                >
                  {signup.isLoading ? <Spinner className="mr-2" /> : 'Sign up'}
                </Button>
              </div>
            </form>
          ) : (
            <form onSubmit={handleVerify} className="fade-in w-full flex flex-col items-center">
              <div className="w-full max-w-2xl space-y-6">
                <Field>
                  <FieldContent>
                    <FieldLabel htmlFor="verification-code" className="text-lg font-semibold text-white">Verification Code</FieldLabel>
                    <Input
                      id="verification-code"
                      type="text"
                      placeholder="ABC123"
                      value={verification.verificationCode}
                      onChange={(e) => verification.handleVerificationCodeChange(e.target.value)}
                      disabled={verification.isLoading}
                      required
                      maxLength={6}
                      className="bg-white rounded-full px-8 py-4 text-gray-800 text-lg text-center placeholder-gray-400 shadow-lg"
                      autoComplete="off"
                    />
                    <FieldDescription className="text-white/90">
                      Enter the 6-character code sent to {signup.formData.email}
                    </FieldDescription>
                    <FieldError errors={verification.errors.verification ? [{ message: verification.errors.verification }] : null} />
                  </FieldContent>
                </Field>

                {verification.resendMessage && (
                  <div className="text-lg text-green-200 font-medium">
                    {verification.resendMessage}
                  </div>
                )}

                {verification.errors.submit && (
                  <FieldError errors={[{ message: verification.errors.submit }]} />
                )}
              </div>

              <div className="mt-8 w-full max-w-2xl flex flex-col space-y-3">
                <Button
                  type="submit"
                  className="rounded-full px-6 py-3 font-semibold shadow-lg"
                  style={buttonStyle(pressed.verify)}
                  onMouseDown={() => setPressed(p => ({ ...p, verify: true }))}
                  onMouseUp={() => setPressed(p => ({ ...p, verify: false }))}
                  onMouseLeave={() => setPressed(p => ({ ...p, verify: false }))}
                  disabled={verification.isLoading || verification.verificationCode.length !== 6}
                >
                  {verification.isLoading ? <Spinner className="mr-2" /> : 'Verify'}
                </Button>
                <div className="flex gap-3">
                  <Button type="button" variant="ghost" className="flex-1 rounded-full bg-white/90 text-sm font-semibold" style={{color: getLocaleColor()}} onClick={handleResendWithCooldown} disabled={verification.isResending || verification.isLoading || resendCooldown > 0}>
                    {verification.isResending ? <Spinner className="mr-2" /> : (resendCooldown > 0 ? `Resend in ${resendCooldown}s` : 'Resend code')}
                  </Button>
                  <Button type="button" variant="outline" className="flex-1 rounded-full bg-white text-sm font-semibold" style={{color: getLocaleColor()}} onClick={handleBackToRegistration} disabled={verification.isLoading}>
                    Back
                  </Button>
                </div>
              </div>
            </form>
          )}
        </div>
      </div>
    </>
  )
}
