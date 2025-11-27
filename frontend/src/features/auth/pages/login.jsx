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
    verification.reset()
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-black p-4 sm:p-6 md:p-12">
      <Card className="w-full max-w-md sm:max-w-lg lg:max-w-xl bg-muted-50 dark:bg-muted-900 shadow-lg">
        <CardHeader className="space-y-1 text-center">
          <CardTitle className="text-lg sm:text-2xl font-bold text-white">
            {isWaitingForOtp ? "Verify your email" : "Welcome back!"}
          </CardTitle>
          <CardDescription className="text-sm sm:text-base">
            {isWaitingForOtp
              ? "Enter the 6-character code sent to your email"
              : "Enter your email to sign in"}
          </CardDescription>
        </CardHeader>

        {!isWaitingForOtp ? (
          <form onSubmit={handleLogin}>
            <CardContent className="space-y-4 sm:space-y-5">
              <Field>
                <FieldContent>
                  <FieldLabel htmlFor="email">Email</FieldLabel>
                  <Input
                    id="email"
                    type="email"
                    placeholder="john@uni.minerva.edu"
                    value={login.email}
                    onChange={(e) => login.handleChange(e.target.value)}
                    disabled={login.isLoading}
                    required
                    className="w-full text-sm sm:text-base"
                  />
                  <FieldError errors={login.errors.email ? [{ message: login.errors.email }] : null} />
                </FieldContent>
              </Field>

              {login.errors.submit && (
                <FieldError errors={[{ message: login.errors.submit }]} />
              )}
            </CardContent>
            <CardFooter className="flex flex-col space-y-4 sm:flex-row sm:items-center sm:justify-between sm:space-y-0 sm:space-x-4">
              <Button type="submit" className="w-full sm:w-auto" disabled={login.isLoading}>
                {login.isLoading && <Spinner className="mr-2" />}
                Sign in
              </Button>
              <p className="text-sm text-muted-foreground text-center sm:text-left">
                Don't have an account?{" "}
                <Link to="/signup" className="text-primary hover:underline font-medium text-white">
                  Sign up
                </Link>
              </p>
            </CardFooter>
          </form>
        ) : (
          <form onSubmit={handleVerify}>
            <CardContent className="space-y-4 sm:space-y-5">
              <Field>
                <FieldContent>
                  <FieldLabel htmlFor="verification-code">Verification Code</FieldLabel>
                  <Input
                    id="verification-code"
                    type="text"
                    placeholder="ABC123"
                    value={verification.verificationCode}
                    onChange={(e) => verification.handleVerificationCodeChange(e.target.value)}
                    disabled={verification.isLoading}
                    required
                    maxLength={6}
                    className="w-full text-sm sm:text-base font-mono tracking-widest text-center uppercase"
                    autoComplete="off"
                  />
                  <FieldDescription className="text-xs sm:text-sm">
                    Enter the 6-character code sent to {login.email}
                  </FieldDescription>
                  <FieldError errors={verification.errors.verification ? [{ message: verification.errors.verification }] : null} />
                </FieldContent>
              </Field>

              {verification.resendMessage && (
                <div className="text-sm text-green-600 dark:text-green-400">
                  {verification.resendMessage}
                </div>
              )}

              {verification.errors.submit && (
                <FieldError errors={[{ message: verification.errors.submit }]} />
              )}
            </CardContent>
            <CardFooter className="flex flex-col space-y-4">
              <Button type="submit" className="w-full bg-black-200 text-white" disabled={verification.isLoading || verification.verificationCode.length !== 6}>
                {verification.isLoading && <Spinner className="mr-2" />}
                Verify
              </Button>
              <Button
                type="button"
                variant="ghost"
                className="w-full bg-gray-300 dark:bg-gray-800"
                onClick={verification.handleResendCode}
                disabled={verification.isResending || verification.isLoading}
              >
                {verification.isResending && <Spinner className="mr-2" />}
                Resend code
              </Button>
              <Button
                type="button"
                variant="outline"
                className="w-full bg-black-200 text-white"
                onClick={handleBackToLogin}
                disabled={verification.isLoading}
              >
                Back to login
              </Button>
            </CardFooter>
          </form>
        )}
      </Card>
    </div>
  )
}
