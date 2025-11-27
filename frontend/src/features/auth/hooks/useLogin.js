import { useState } from "react"
import { authService } from "../services/authservice"

const EMAIL_REGEX = /^[^\s@]+@(uni\.minerva\.edu|minerva\.edu)$/

export function useLogin() {
  const [email, setEmail] = useState("")
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  const validateEmail = (email) => {
    if (!EMAIL_REGEX.test(email)) {
      return "Email must be from @uni.minerva.edu or @minerva.edu"
    }
    return null
  }

  const handleChange = (value) => {
    setEmail(value)
    if (errors.email) {
      setErrors(prev => ({ ...prev, email: null }))
    }
  }

  const handleSubmit = async () => {
    setErrors({})
    
    const emailError = validateEmail(email)
    if (emailError) {
      setErrors({ email: emailError })
      return { success: false }
    }

    setIsLoading(true)

    try {
      await authService.login({ email })
      return { success: true }
    } catch (error) {
      setErrors({ submit: error.message })
      return { success: false }
    } finally {
      setIsLoading(false)
    }
  }

  return {
    email,
    errors,
    isLoading,
    handleChange,
    handleSubmit,
  }
}
