import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { authService } from "../services/authservice"

export function useLoginVerification(email) {
  const navigate = useNavigate()
  const [verificationCode, setVerificationCode] = useState("")
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const [isResending, setIsResending] = useState(false)
  const [resendMessage, setResendMessage] = useState("")

  const handleVerificationCodeChange = (value) => {
    const sanitized = value.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 6)
    setVerificationCode(sanitized)
    if (errors.verification) {
      setErrors(prev => ({ ...prev, verification: null }))
    }
  }

  const handleSubmit = async () => {
    setErrors({})
    setIsLoading(true)

    try {
      await authService.verifyLogin({
        email,
        verificationCode,
      })

      navigate("/")
      return { success: true }
    } catch (error) {
      setErrors({ submit: error.message })
      return { success: false }
    } finally {
      setIsLoading(false)
    }
  }

  const handleResendCode = async () => {
    setErrors({})
    setResendMessage("")
    setIsResending(true)

    try {
      await authService.login({ email })
      setResendMessage("Verification code resent successfully. Please check your email.")
    } catch (error) {
      setErrors({ submit: error.message })
    } finally {
      setIsResending(false)
    }
  }

  const reset = () => {
    setVerificationCode("")
    setErrors({})
    setResendMessage("")
  }

  return {
    verificationCode,
    errors,
    isLoading,
    isResending,
    resendMessage,
    handleVerificationCodeChange,
    handleSubmit,
    handleResendCode,
    reset,
  }
}