import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { Button } from "@/shared/components/ui/button"
import { Field, FieldContent, FieldDescription, FieldError, FieldLabel } from "@/shared/components/ui/field"
import { Input } from "@/shared/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/shared/components/ui/select"
import { Spinner } from "@/shared/components/ui/spinner"
import { useSignup } from "../hooks/useSignup"
import { useVerification } from "../hooks/useVerification"

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
    background: linear-gradient(135deg, #4b8dc9 0%, #6ba3d1 100%) !important;
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

const ROTATION_CITIES = [
  { value: "1", label: "San Francisco", icon: "/sf.png" },
  { value: "2", label: "Taipei", icon: "/tp.png" },
  { value: "3", label: "Seoul", icon: "/sl.png" },
  { value: "4", label: "Buenos Aires", icon: "/ba.png" },
  { value: "5", label: "India", icon: "/hy.png" },
  { value: "6", label: "Berlin", icon: "/br.png" },
]

export default function SignupPage() {
  const [isWaitingForOtp, setIsWaitingForOtp] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(0)
  const [currentLocale, setCurrentLocale] = useState('usa')
<<<<<<< HEAD
  const [hoveredCity, setHoveredCity] = useState(null)
  const [selectedCity, setSelectedCity] = useState(null)
=======
>>>>>>> 9f73737c27ab8e09dbdc43ba0109785d2cf616d1
  const signup = useSignup()
  const verification = useVerification(signup.formData.email)

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
<<<<<<< HEAD
    const displayLocale = getDisplayLocale()
=======
>>>>>>> 9f73737c27ab8e09dbdc43ba0109785d2cf616d1
    const classMap = {
      usa: 'show-photo',
      china: 'transition-green',
      korea: 'transition-korea',
      argentina: 'transition-argentina',
      india: 'transition-india',
      germany: 'transition-germany'
    }
<<<<<<< HEAD
    return classMap[displayLocale] || 'show-photo'
  }

  const getLocaleColor = () => {
    const displayLocale = getDisplayLocale()
=======
    return classMap[currentLocale] || 'show-photo'
  }

  const getLocaleColor = () => {
>>>>>>> 9f73737c27ab8e09dbdc43ba0109785d2cf616d1
    const colorMap = {
      usa: '#cc0000',
      china: '#2fb872',
      korea: '#e91e63',
<<<<<<< HEAD
      argentina: '#d9a300',
      india: '#ffcc33',
      germany: '#7bb3e8'
    }
    return colorMap[displayLocale] || '#cc0000'
  }

  const getCityLocale = (cityKey) => {
    const map = { '1': 'usa', '2': 'china', '3': 'korea', '4': 'argentina', '5': 'india', '6': 'germany' }
    return map[cityKey] || 'usa'
  }

  const getLandmarkSvg = (cityKey) => {
    const svgs = {
      '1': (
        <svg viewBox="0 0 100 100" className="w-16 h-16">
          <text x="50" y="50" textAnchor="middle" dy=".3em" className="text-2xl" fill="currentColor">🌉</text>
        </svg>
      ),
      '2': (
        <svg viewBox="0 0 100 100" className="w-16 h-16">
          <text x="50" y="50" textAnchor="middle" dy=".3em" className="text-2xl" fill="currentColor">🏯</text>
        </svg>
      ),
      '3': (
        <svg viewBox="0 0 100 100" className="w-16 h-16">
          <text x="50" y="50" textAnchor="middle" dy=".3em" className="text-2xl" fill="currentColor">🗼</text>
        </svg>
      ),
      '4': (
        <svg viewBox="0 0 100 100" className="w-16 h-16">
          <text x="50" y="50" textAnchor="middle" dy=".3em" className="text-2xl" fill="currentColor">🗽</text>
        </svg>
      ),
      '5': (
        <svg viewBox="0 0 100 100" className="w-16 h-16">
          <text x="50" y="50" textAnchor="middle" dy=".3em" className="text-2xl" fill="currentColor">🕌</text>
        </svg>
      ),
      '6': (
        <svg viewBox="0 0 100 100" className="w-16 h-16">
          <text x="50" y="50" textAnchor="middle" dy=".3em" className="text-2xl" fill="currentColor">🗿</text>
        </svg>
      ),
    }
    return svgs[cityKey]
  }

  const getDisplayLocale = () => {
    if (selectedCity) return getCityLocale(selectedCity)
    if (hoveredCity) return getCityLocale(hoveredCity)
    return currentLocale
  }

  const getLocaleText = () => {
    const displayLocale = getDisplayLocale()
    const textMap = {
      usa: 'Ready for Rotation?',
      china: '准备好轮换了吗？',
      korea: '로테이션 준비되셨나요?',
      argentina: '¿Listo para la rotación?',
      india: 'రోటేషన్‌కు సిద్ధమా?',
      germany: 'Bereit für die Rotation?'
    }
    return textMap[displayLocale] || 'Ready for Rotation?'
  }

  const shouldSplitLetters = () => {
    // Keep full phrases intact (no per-letter split) so spaces and script shaping remain correct
    return false
=======
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
>>>>>>> 9f73737c27ab8e09dbdc43ba0109785d2cf616d1
  }

  return (
    <>
      <style>{animationStyles}</style>
      <div className={`signup-container min-h-screen w-full relative flex items-center justify-center ${getLocaleClass()}`}>
        <div className={`overlay absolute inset-0 ${getLocaleClass()}`}></div>

        <div className="relative z-10 flex flex-col items-center justify-center w-full px-6 sm:px-12 max-w-3xl">
<<<<<<< HEAD
          <h1 className="text-white text-3xl sm:text-4xl md:text-5xl font-extrabold leading-tight text-center mb-8" style={{fontFamily: 'Fraunces, serif', letterSpacing: '0.003em'}}>
=======
          <h1 className="text-white text-5xl sm:text-7xl font-extrabold leading-tight drop-shadow-md text-center mb-8" style={{fontFamily: 'Georgia, serif'}}>
>>>>>>> 9f73737c27ab8e09dbdc43ba0109785d2cf616d1
            {shouldSplitLetters() ? (
              getLocaleText().split('').map((letter, index) => (
                <span key={index} className={`letter letter-${index}`}>
                  {letter}
                </span>
              ))
            ) : (
<<<<<<< HEAD
              <span className="letter letter-0" style={{fontFeatureSettings: '"liga" on, "kern" on'}}>{getLocaleText()}</span>
=======
              <span className="letter letter-0">{getLocaleText()}</span>
>>>>>>> 9f73737c27ab8e09dbdc43ba0109785d2cf616d1
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
<<<<<<< HEAD
                    <div className="flex flex-col gap-2">
                      <div className="flex gap-2 justify-center">
                        {ROTATION_CITIES.map((city) => (
                          <button
                            key={city.value}
                            type="button"
                            onClick={() => {
                              signup.handleChange("cityId", city.value);
                              setSelectedCity(city.value);
                            }}
                            onMouseEnter={() => setHoveredCity(city.value)}
                            onMouseLeave={() => setHoveredCity(null)}
                            className={`transition-all duration-150 rounded-xl ${
                              selectedCity === city.value
                                ? "opacity-100 drop-shadow-2xl scale-120"
                                : hoveredCity === city.value
                                  ? "opacity-100 drop-shadow-lg scale-112"
                                  : "opacity-85 hover:opacity-100"
                            }`}
                          >
                            <img src={city.icon} alt={city.label} className="w-24 h-24 object-cover rounded-xl" />
                          </button>
                        ))}
                      </div>
                      <FieldError errors={signup.errors.cityId ? [{ message: signup.errors.cityId }] : null} />
                    </div>
=======
                    <Select value={signup.formData.city} onValueChange={(value) => signup.handleChange("city", value)}>
                      <SelectTrigger className="bg-white rounded-full px-8 py-4 text-gray-800 text-lg shadow-lg">
                        <SelectValue placeholder="Select a city" />
                      </SelectTrigger>
                      <SelectContent>
                        {ROTATION_CITIES.map((city) => (
                          <SelectItem key={city.value} value={city.value}>
                            {city.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FieldError errors={signup.errors.city ? [{ message: signup.errors.city }] : null} />
>>>>>>> 9f73737c27ab8e09dbdc43ba0109785d2cf616d1
                  </FieldContent>
                </Field>
              </div>

              <div className="mt-8 w-full max-w-2xl flex items-center justify-between">
                <Button type="button" className="rounded-full px-6 py-3 bg-white font-semibold shadow-lg" style={{color: getLocaleColor()}} onClick={() => window.location.href = '/login'}>
                  Sign in
                </Button>
                <Button type="submit" className="ml-4 rounded-full px-6 py-3 bg-white font-semibold shadow-lg" style={{color: getLocaleColor()}} disabled={signup.isLoading}>
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
        </div>
      </div>
    </>
  )
}
