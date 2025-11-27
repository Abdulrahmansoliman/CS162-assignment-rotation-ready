import { useState } from "react"
import { Link } from "react-router-dom"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/shared/components/ui/card"
import { Button } from "@/shared/components/ui/button"
import { Field, FieldContent, FieldDescription, FieldError, FieldLabel } from "@/shared/components/ui/field"
import { Input } from "@/shared/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/shared/components/ui/select"
import { Spinner } from "@/shared/components/ui/spinner"
import { useSignup } from "../hooks/useSignup"
import { useVerification } from "../hooks/useVerification"

const ROTATION_CITIES = [
  { value: "1", label: "San Francisco" },
  { value: "2", label: "Taipei" },
  { value: "3", label: "Seoul" },
  { value: "4", label: "Buenos Aires" },
  { value: "5", label: "India" },
  { value: "6", label: "Berlin" },
]

export default function SignupPage() {
  const [isWaitingForOtp, setIsWaitingForOtp] = useState(false)
  const signup = useSignup()
  const verification = useVerification(signup.formData.email)

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
    verification.reset()
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-900 p-4 sm:p-6 md:p-12">
      <Card className="w-full max-w-md sm:max-w-lg lg:max-w-2xl bg-slate-800/90 backdrop-blur-sm border-slate-700 shadow-2xl">
        <CardHeader className="space-y-3 text-center pb-8">
          <CardTitle className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white tracking-tight">
            {isWaitingForOtp ? "Verify your email" : "Let's start the journey!"}
          </CardTitle>
          <CardDescription className="text-base sm:text-lg lg:text-xl text-slate-300">
            {isWaitingForOtp
              ? "Enter the 6-character code sent to your email"
              : "Enter your information to get started with your rotation"}
          </CardDescription>
        </CardHeader>

        {!isWaitingForOtp ? (
          <form onSubmit={handleRegister}>
            <CardContent className="space-y-6 sm:space-y-7">
              <Field>
                <FieldContent>
                  <FieldLabel htmlFor="firstName" className="text-lg sm:text-lg font-semibold text-slate-200">First Name</FieldLabel>
                  <Input
                    id="firstName"
                    type="text"
                    placeholder="John"
                    value={signup.formData.firstName}
                    onChange={(e) => signup.handleChange("firstName", e.target.value)}
                    disabled={signup.isLoading}
                    required
                    className="w-full text-lg sm:text-xl h-12 sm:h-14 font-semibold bg-slate-700/50 border-slate-600"
                  />
                  <FieldError errors={signup.errors.firstName ? [{ message: signup.errors.firstName }] : null} />
                </FieldContent>
              </Field>

              <Field>
                <FieldContent>
                  <FieldLabel htmlFor="lastName" className="text-base sm:text-lg font-semibold text-slate-200">Last Name</FieldLabel>
                  <Input
                    id="lastName"
                    type="text"
                    placeholder="Doe"
                    value={signup.formData.lastName}
                    onChange={(e) => signup.handleChange("lastName", e.target.value)}
                    disabled={signup.isLoading}
                    required
                    className="w-full text-lg sm:text-xl h-12 sm:h-14 bg-slate-700/50 border-slate-600 text-white"
                  />
                  <FieldError errors={signup.errors.lastName ? [{ message: signup.errors.lastName }] : null} />
                </FieldContent>
              </Field>

              <Field>
                <FieldContent>
                  <FieldLabel htmlFor="email" className="text-base sm:text-lg font-semibold text-slate-200">Email</FieldLabel>
                  <Input
                    id="email"
                    type="email"
                    placeholder="john@uni.minerva.edu"
                    value={signup.formData.email}
                    onChange={(e) => signup.handleChange("email", e.target.value)}
                    disabled={signup.isLoading}
                    required
                    className="w-full text-lg sm:text-xl h-12 sm:h-14 bg-slate-700/50 border-slate-600 text-white"
                  />
                  <FieldError errors={signup.errors.email ? [{ message: signup.errors.email }] : null} />
                </FieldContent>
              </Field>

              <Field>
                <FieldContent>
                  <FieldLabel htmlFor="rotation-city" className="text-base sm:text-lg font-semibold text-slate-200">Rotation City</FieldLabel>
                  <Select
                    value={signup.formData.cityId}
                    onValueChange={(value) => signup.handleChange("cityId", value)}
                    disabled={signup.isLoading}
                    required
                  >
                    <SelectTrigger id="rotation-city" className="w-full text-lg sm:text-xl h-10 sm:h-12 bg-slate-700/50 border-slate-600" >
                      <SelectValue placeholder="Select your rotation city" />
                    </SelectTrigger>
                    <SelectContent className="bg-slate-800 border-slate-700">
                      {ROTATION_CITIES.map((city) => (
                        <SelectItem key={city.value} value={city.value} className="text-lg sm:text-xl text-white hover:bg-slate-700">
                          {city.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FieldError errors={signup.errors.cityId ? [{ message: signup.errors.cityId }] : null} />
                </FieldContent>
              </Field>

              {signup.errors.submit && (
                <FieldError errors={[{ message: signup.errors.submit }]} />
              )}
            </CardContent>
            <CardFooter className="flex flex-col space-y-4 sm:flex-row sm:items-center sm:justify-between sm:space-y-0 sm:space-x-4 pt-6">
              <Button type="submit" className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white text-base sm:text-lg font-semibold h-12 sm:h-14 px-8" disabled={signup.isLoading}>
                {signup.isLoading && <Spinner className="mr-2" />}
                Create account
              </Button>
              <p className="text-sm sm:text-base text-slate-300 text-center sm:text-left">
                Already have an account?{" "}
                <Link to="/login" className="text-blue-400 hover:text-blue-300 hover:underline font-semibold">
                  Sign in
                </Link>
              </p>
            </CardFooter>
          </form>
        ) : (
          <form onSubmit={handleVerify}>
            <CardContent className="space-y-6 sm:space-y-7">
              <Field>
                <FieldContent>
                  <FieldLabel htmlFor="verification-code" className="text-base sm:text-lg font-semibold text-slate-200">Verification Code</FieldLabel>
                  <Input
                    id="verification-code"
                    type="text"
                    placeholder="ABC123"
                    value={verification.verificationCode}
                    onChange={(e) => verification.handleVerificationCodeChange(e.target.value)}
                    disabled={verification.isLoading}
                    required
                    maxLength={6}
                    className="w-full text-xl sm:text-2xl h-14 sm:h-16 bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 font-mono tracking-widest text-center uppercase focus:border-blue-500 focus:ring-blue-500"
                    autoComplete="off"
                  />
                  <FieldDescription className="text-sm sm:text-base text-slate-300 mt-2">
                    Enter the 6-character code sent to {signup.formData.email}
                  </FieldDescription>
                  <FieldError errors={verification.errors.verification ? [{ message: verification.errors.verification }] : null} />
                </FieldContent>
              </Field>

              {verification.resendMessage && (
                <div className="text-base sm:text-lg text-green-400 font-medium">
                  {verification.resendMessage}
                </div>
              )}

              {verification.errors.submit && (
                <FieldError errors={[{ message: verification.errors.submit }]} />
              )}
            </CardContent>
            <CardFooter className="flex flex-col space-y-4 pt-6">
              <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white text-base sm:text-lg font-semibold h-12 sm:h-14" disabled={verification.isLoading || verification.verificationCode.length !== 6}>
                {verification.isLoading && <Spinner className="mr-2" />}
                Verify
              </Button>
              <Button
                type="button"
                variant="ghost"
                className="w-full bg-slate-700/50 hover:bg-slate-700 text-white text-base sm:text-lg font-semibold h-12 sm:h-14"
                onClick={verification.handleResendCode}
                disabled={verification.isResending || verification.isLoading}
              >
                {verification.isResending && <Spinner className="mr-2" />}
                Resend code
              </Button>
              <Button
                type="button"
                variant="outline"
                className="w-full bg-transparent border-slate-600 hover:bg-slate-700/50 text-white text-base sm:text-lg font-semibold h-12 sm:h-14"
                onClick={handleBackToRegistration}
                disabled={verification.isLoading}
              >
                Back to registration
              </Button>
            </CardFooter>
          </form>
        )}
      </Card>
    </div>
  )
}
