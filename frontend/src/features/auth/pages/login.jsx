import { useState } from "react"
import { Link } from "react-router-dom"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/shared/components/ui/card"
import { Button } from "@/shared/components/ui/button"
import { Field, FieldContent, FieldDescription, FieldError, FieldLabel } from "@/shared/components/ui/field"
import { Input } from "@/shared/components/ui/input"
import { Spinner } from "@/shared/components/ui/spinner"
import { useLogin } from "../hooks/useLogin"
import { useLoginVerification } from "../hooks/useLoginVerification"

export default function LoginPage() {
  const [isWaitingForOtp, setIsWaitingForOtp] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(0)
  const login = useLogin()
  const verification = useLoginVerification(login.email)

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

  return (
    <div className="min-h-screen w-full relative bg-cover bg-center flex items-center justify-center" style={{backgroundImage: "url('/sf.jpg')"}}>
      <div className="absolute inset-0 bg-red-700 opacity-80"></div>

      <div className="relative z-10 flex flex-col items-center justify-center w-full px-6 sm:px-12">
        <h1 className="text-white text-6xl sm:text-8xl md:text-9xl font-extrabold leading-tight drop-shadow-md" style={{fontFamily: 'Georgia, serif'}}>
          Welcome
        </h1>

        {!isWaitingForOtp ? (
          <form onSubmit={handleLogin} className="mt-8 w-full max-w-2xl flex flex-col items-center">
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
          <form onSubmit={handleVerify} className="mt-8 w-full max-w-md flex flex-col items-center">
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
  )
}
