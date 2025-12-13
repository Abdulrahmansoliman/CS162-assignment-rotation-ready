import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { Button } from "@/shared/components/ui/button"
import { Field, FieldContent, FieldDescription, FieldError, FieldLabel } from "@/shared/components/ui/field"
import { Input } from "@/shared/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/shared/components/ui/select"
import { Spinner } from "@/shared/components/ui/spinner"
import { useSignup } from "../hooks/useSignup"
import { useVerification } from "../hooks/useVerification"
import { getCities } from "../../../api/cities"
import "../../../shared/styles/localeTransitions.css"

// Map city names to icon paths
const CITY_ICONS = {
  'san francisco': '/sf.png',
  'taipei': '/tp.png',
  'seoul': '/sl.png',
  'buenos aires': '/ba.png',
  'hyderabad': '/hy.png',
  'berlin': '/br.png'
}

export default function SignupPage() {
  const [isWaitingForOtp, setIsWaitingForOtp] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(0)
  const [currentLocale, setCurrentLocale] = useState('usa')
  const [rotationCities, setRotationCities] = useState([])
  const signup = useSignup()
  const verification = useVerification(signup.formData.email)

  // Fetch rotation cities on mount
  useEffect(() => {
    const fetchCities = async () => {
      try {
        const cities = await getCities()
        setRotationCities(cities.map(city => ({
          value: String(city.city_id),
          label: city.name,
          icon: CITY_ICONS[city.name.toLowerCase()] || null
        })))
      } catch (error) {
        console.error("Failed to fetch cities:", error)
      }
    }
    fetchCities()
  }, [])

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
      china: '#2fb872',
      korea: '#e91e63',
      argentina: '#6ba3d1',
      india: '#ffcc33',
      germany: '#7bb3e8'
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

  return (
    <>
      <div className={`locale-container min-h-screen w-full relative flex items-center justify-center ${getLocaleClass()}`}>
        <div className={`locale-overlay absolute inset-0 ${getLocaleClass()}`}></div>

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
                    <Select value={signup.formData.city} onValueChange={(value) => signup.handleChange("city", value)}>
                      <SelectTrigger className="bg-white rounded-full px-8 py-4 text-gray-800 text-lg shadow-lg">
                        <SelectValue placeholder="Select a city" />
                      </SelectTrigger>
                      <SelectContent>
                        {rotationCities.map((city) => (
                          <SelectItem key={city.value} value={city.value}>
                            {city.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FieldError errors={signup.errors.city ? [{ message: signup.errors.city }] : null} />
                  </FieldContent>
                </Field>
              </div>

              <div className="mt-8 w-full max-w-2xl flex items-center justify-center">
                <Button type="submit" className="rounded-full px-6 py-3 bg-white font-semibold shadow-lg" style={{color: getLocaleColor()}} disabled={signup.isLoading}>
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
                <Button type="submit" className="rounded-full px-6 py-3 bg-white font-semibold shadow-lg" style={{color: getLocaleColor()}} disabled={verification.isLoading || verification.verificationCode.length !== 6}>
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
          <div className="mt-6 text-white text-center">
            <p>Already have an account? <Link to="/login" className="font-semibold underline hover:opacity-80 transition">Sign in</Link></p>
          </div>
        </div>
      </div>
    </>
  )
}
