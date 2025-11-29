import { useState, useEffect } from "react"
import { userService } from "../services/userService"

export function useCurrentUser() {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchUser = async () => {
      try {
        setIsLoading(true)
        setError(null)
        const userData = await userService.getCurrentUser()
        setUser(userData)
      } catch (err) {
        setError(err.message)
        setUser(null)
      } finally {
        setIsLoading(false)
      }
    }

    fetchUser()
  }, [])

  return { user, isLoading, error }
}

