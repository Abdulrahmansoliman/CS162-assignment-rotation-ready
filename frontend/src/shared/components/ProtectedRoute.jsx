import { useEffect, useState } from "react"
import { Navigate } from "react-router-dom"
import { getAccessToken } from "@/features/auth/services/authservice"
import { checkAuth } from "@/api/index"
import { Spinner } from "@/shared/components/ui/spinner"

export default function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const verifyAuth = async () => {
      const token = getAccessToken()
      if (!token) {
        setIsAuthenticated(false)
        setIsLoading(false)
        return
      }

      try {
        const authenticated = await checkAuth()
        setIsAuthenticated(authenticated)
      } catch (error) {
        setIsAuthenticated(false)
      } finally {
        setIsLoading(false)
      }
    }

    verifyAuth()
  }, [])

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Spinner className="h-8 w-8" />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}

