import { useState } from "react"
import { authService } from "../services/authservice"

const EMAIL_REGEX = /^[^\s@]+@(uni\.minerva\.edu|minerva\.edu)$/

export function validateEmail(email) {
  if (!EMAIL_REGEX.test(email)) {
    return "Email must be from @uni.minerva.edu or @minerva.edu"
  }
  return null
}

export function useSignup() {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    cityId: "1", // default to first rotation city
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }))
    }
  }

  const handleSubmit = async () => {
    setErrors({})
    
    const emailError = validateEmail(formData.email)
    if (emailError) {
      setErrors({ email: emailError })
      return { success: false }
    }

    if (!formData.cityId) {
      setErrors({ cityId: "Rotation city is required" })
      return { success: false }
    }

    setIsLoading(true)

    try {
      await authService.register({
        email: formData.email,
        cityId: formData.cityId,
        firstName: formData.firstName,
        lastName: formData.lastName,
      })
      return { success: true }
    } catch (error) {
      setErrors({ submit: error.message })
      return { success: false }
    } finally {
      setIsLoading(false)
    }
  }

  return {
    formData,
    errors,
    isLoading,
    handleChange,
    handleSubmit,
  }
}
