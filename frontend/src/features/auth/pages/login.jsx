import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/shared/components/ui/card"
import { Button } from "@/shared/components/ui/button"
import { Field, FieldContent, FieldDescription, FieldError, FieldLabel } from "@/shared/components/ui/field"
import { Input } from "@/shared/components/ui/input"
import { Spinner } from "@/shared/components/ui/spinner"
import { useLogin } from "../hooks/useLogin"
import { useLoginVerification } from "../hooks/useLoginVerification"

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

  .letter-0 { }
  .letter-1 { }
  .letter-2 { }
  .letter-3 { }
  .letter-4 { }
  .letter-5 { }
  .letter-6 { }

  .chinese-letter {
    display: inline-block;
  }

  .chinese-letter-0 { }
  .chinese-letter-1 { }

  .fade-in {
    animation: fadeInSlideUp 0.8s ease-out 1.2s forwards;
    opacity: 0;
  }

  .login-container {
    background: linear-gradient(135deg, #cc0000 0%, #ff4444 100%);
    background-size: cover;
    background-position: center;
    transition: background-image 0.8s ease-out, background 0.8s ease-out;
  }

  .login-container.show-photo {
    background-image: url('/sf.jpg');
    background-size: cover;
    background-position: center;
    background-blend-mode: overlay;
  }

  .login-container.transition-green {
    background: linear-gradient(135deg, #1d9a5c 0%, #2fb872 100%) !important;
    background-image: url('/tp.jpg') !important;
    background-size: 120% !important;
    background-repeat: no-repeat !important;
    background-position: center;
    background-blend-mode: overlay;
  }

  .login-container.transition-korea {
    background: linear-gradient(135deg, #c60c30 0%, #e91e63 100%) !important;
    background-image: url('/sl.jpg') !important;
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
`

export default function LoginPage() {
  const [isWaitingForOtp, setIsWaitingForOtp] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(0)
  const [showPhoto, setShowPhoto] = useState(true)
  const [currentLocale, setCurrentLocale] = useState('usa') // usa, china, korea, argentina, india, germany
  const login = useLogin()
  const verification = useLoginVerification(login.email)

  useEffect(() => {
    const locales = ['usa', 'china', 'korea']
    let index = 0
    
    const cycleLocales = () => {
      index = (index + 1) % locales.length
      setCurrentLocale(locales[index])
      setTimeout(cycleLocales, 5000)
    }
    
    const timer = setTimeout(cycleLocales, 5000)
    return () => clearTimeout(timer)
  }, [])

  const handleLogin = async (e) => {
    e.preventDefault()
    const result = await login.handleSubmit()
    if (result.success) {
      setIsWaitingForOtp(true)
    }
  }

  const handleVerify = async (e) => {
    e.preventDefault()
    await verification.handleSubmit()
  }

  const handleBackToLogin = () => {
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
      korea: 'transition-korea'
    }
    return classMap[currentLocale] || 'show-photo'
  }

  const getLocaleText = () => {
    const textMap = {
      usa: 'Welcome',
      china: '欢迎',
      korea: '어서 오세요'
    }
    return textMap[currentLocale] || 'Welcome'
  }

  return (
    <>
      <style>{animationStyles}</style>
      <div className={`login-container min-h-screen w-full relative flex items-center justify-center ${getLocaleClass()}`}>
        <div className={`overlay absolute inset-0 ${getLocaleClass()}`}></div>

        <div className="relative z-10 flex flex-col items-center justify-center w-full px-6 sm:px-12">
          <h1 className="text-white text-6xl sm:text-8xl md:text-9xl font-extrabold leading-tight drop-shadow-md" style={{fontFamily: 'Georgia, serif', letterSpacing: '0.05em'}}>
            {getLocaleText().split('').map((letter, index) => (
              <span key={index} className={`letter letter-${index}`}>
                {letter}
              </span>
            ))}
          </h1>

          {!isWaitingForOtp ? (
          <form onSubmit={handleLogin} className="fade-in mt-8 w-full max-w-2xl flex flex-col items-center">
            <div className="w-full">
              <Input
                id="email"
                type="email"
                placeholder="email..."
                value={login.email}
                onChange={(e) => login.handleChange(e.target.value)}
                disabled={login.isLoading}
                required
                className="mx-auto block w-full max-w-3xl bg-white rounded-full px-8 py-4 text-gray-800 text-lg sm:text-xl placeholder-gray-400 shadow-lg"
              />
            </div>

            <div className="mt-6 w-full max-w-3xl flex items-center justify-between">
              <div className="text-sm text-white/90">
                Don't have an account? <Link to="/signup" className="underline font-medium">Sign up</Link>
              </div>
              <Button type="submit" className="ml-4 rounded-full px-6 py-3 bg-white text-red-700 font-semibold shadow-lg" disabled={login.isLoading}>
                {login.isLoading ? <Spinner className="mr-2" /> : 'Sign in'}
              </Button>
            </div>
            {login.errors.submit && (
              <div className="mt-4 text-sm text-yellow-200">{login.errors.submit}</div>
            )}
          </form>
        ) : (
          <form onSubmit={handleVerify} className="fade-in mt-8 w-full max-w-md flex flex-col items-center">
            <Input
              id="verification-code"
              type="text"
              placeholder="ABC123"
              value={verification.verificationCode}
              onChange={(e) => verification.handleVerificationCodeChange(e.target.value)}
              disabled={verification.isLoading}
              required
              maxLength={6}
              className="mx-auto block w-full bg-white rounded-full px-8 py-4 text-gray-800 text-lg tracking-widest text-center font-mono uppercase shadow-lg"
              autoComplete="off"
            />

            <div className="mt-4 w-full flex flex-col space-y-3">
              <Button type="submit" className="rounded-full px-6 py-3 bg-white text-red-700 font-semibold shadow-lg" disabled={verification.isLoading || verification.verificationCode.length !== 6}>
                {verification.isLoading ? <Spinner className="mr-2" /> : 'Verify'}
              </Button>
              <div className="flex gap-3">
                <Button type="button" variant="ghost" className="flex-1 rounded-full bg-white/90 text-sm" onClick={handleResendWithCooldown} disabled={verification.isResending || verification.isLoading || resendCooldown > 0}>
                  {verification.isResending ? <Spinner className="mr-2" /> : (resendCooldown > 0 ? `Resend in ${resendCooldown}s` : 'Resend code')}
                </Button>
                <Button type="button" variant="outline" className="flex-1 rounded-full bg-transparent border border-white/60 text-white text-sm" onClick={handleBackToLogin} disabled={verification.isLoading}>
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
