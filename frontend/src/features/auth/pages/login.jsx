import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { Button } from "@/shared/components/ui/button"
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

  .login-container.transition-argentina {
    background: linear-gradient(135deg, #6d70bd 0%, #8b6fc3 100%) !important;
    background-image: url('/ba.jpg') !important;
    background-size: cover !important;
    background-position: center;
    background-blend-mode: overlay;
  }

  .login-container.transition-india {
    background: linear-gradient(135deg, #ff9933 0%, #ffcc33 100%) !important;
    background-image: url('/hyd.jpg') !important;
    background-size: cover !important;
    background-position: center;
    background-blend-mode: overlay;
  }

  .login-container.transition-germany {
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
    background-color: rgba(217, 163, 0, 0.65) !important;
  }

  .overlay.transition-india {
    background-color: rgba(255, 153, 51, 0.62) !important;
  }

  .overlay.transition-germany {
    background-color: rgba(122, 179, 232, 0.65) !important;
  }
`

export default function LoginPage() {
  const [isWaitingForOtp, setIsWaitingForOtp] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(0)
  const [currentLocale, setCurrentLocale] = useState('usa')
  const [pressed, setPressed] = useState({ main: false, verify: false, resend: false, back: false })
  const login = useLogin()
  const verification = useLoginVerification(login.email)

  useEffect(() => {
    if (isWaitingForOtp) return
    const locales = ['usa', 'china', 'korea', 'argentina', 'india', 'germany']
    let index = 0

    const timer = setInterval(() => {
      index = (index + 1) % locales.length
      setCurrentLocale(locales[index])
    }, 5000)

    return () => clearInterval(timer)
  }, [isWaitingForOtp])

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
      korea: 'transition-korea',
      argentina: 'transition-argentina',
      india: 'transition-india',
      germany: 'transition-germany'
    }
    return classMap[currentLocale] || 'show-photo'
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

  const buttonStyle = (isPressed) => ({
    background: isPressed ? getLocaleColor() : '#fff',
    color: isPressed ? '#fff' : getLocaleColor()
  })

  const shouldSplitLetters = () => {
    return currentLocale !== 'india'
  }

  return (
    <>
      <style>{animationStyles}</style>
      <div className={`login-container min-h-screen w-full relative flex items-center justify-center ${getLocaleClass()}`}>
        <div className={`overlay absolute inset-0 ${getLocaleClass()}`}></div>

        <div className="relative z-10 flex flex-col items-center justify-center w-full px-6 sm:px-12">
          <h1 className="text-white text-6xl sm:text-8xl md:text-9xl font-extrabold leading-tight" style={{fontFamily: 'Fraunces, serif', letterSpacing: '0.01em'}}>
            {shouldSplitLetters() ? (
              getLocaleText().split('').map((letter, index) => (
                <span key={index} className={`letter letter-${index}`}>
                  {letter}
                </span>
              ))
            ) : (
              <span className="letter letter-0" style={{fontFeatureSettings: '"liga" on, "kern" on'}}>{getLocaleText()}</span>
            )}
          </h1>

          {login.errors.submit && (
            <div className="mt-4 text-sm text-white">{login.errors.submit}</div>
          )}
          
          {!isWaitingForOtp ? (
            <form onSubmit={handleLogin} className="fade-in mt-8 w-full max-w-2xl flex flex-col items-center gap-4">
              <Input
                id="email"
                type="email"
                placeholder="your.email@example.com"
                value={login.email}
                onChange={(e) => login.handleChange(e.target.value)}
                disabled={login.isLoading}
                required
                className="w-full bg-white rounded-full px-8 py-3 text-gray-800 text-lg text-center shadow-lg"
                autoComplete="email"
              />
              {login.errors.email && (
                <div className="mt-2 text-sm text-white">{login.errors.email}</div>
              )}
              <div className="flex items-center justify-between w-full gap-4 mt-2">
                <div className="text-white text-sm font-medium whitespace-nowrap">
                  Don't have an account? <Link to="/signup" className="underline hover:opacity-80 transition">Sign up</Link>
                </div>
                <Button
                  type="submit"
                  className="rounded-full px-8 py-3 font-semibold shadow-lg whitespace-nowrap"
                  style={buttonStyle(pressed.main)}
                  onMouseDown={() => setPressed(p => ({ ...p, main: true }))}
                  onMouseUp={() => setPressed(p => ({ ...p, main: false }))}
                  onMouseLeave={() => setPressed(p => ({ ...p, main: false }))}
                  disabled={login.isLoading}
                >
                  {login.isLoading ? <Spinner className="mr-2" /> : 'Sign In'}
                </Button>
              </div>
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
              {verification.errors.submit && (
                <div className="mt-2 text-sm text-white">{verification.errors.submit}</div>
              )}
              <div className="mt-4 w-full flex flex-col space-y-3">
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
                    <Button
                      type="button"
                      variant="ghost"
                      className="flex-1 rounded-full text-sm font-semibold"
                      style={buttonStyle(pressed.resend)}
                      onMouseDown={() => setPressed(p => ({ ...p, resend: true }))}
                      onMouseUp={() => setPressed(p => ({ ...p, resend: false }))}
                      onMouseLeave={() => setPressed(p => ({ ...p, resend: false }))}
                      onClick={handleResendWithCooldown}
                      disabled={verification.isResending || verification.isLoading || resendCooldown > 0}
                    >
                    {verification.isResending ? <Spinner className="mr-2" /> : (resendCooldown > 0 ? `Resend in ${resendCooldown}s` : 'Resend code')}
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    className="flex-1 rounded-full text-sm font-semibold"
                    style={buttonStyle(pressed.back)}
                    onMouseDown={() => setPressed(p => ({ ...p, back: true }))}
                    onMouseUp={() => setPressed(p => ({ ...p, back: false }))}
                    onMouseLeave={() => setPressed(p => ({ ...p, back: false }))}
                    onClick={handleBackToLogin}
                    disabled={verification.isLoading}
                  >
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