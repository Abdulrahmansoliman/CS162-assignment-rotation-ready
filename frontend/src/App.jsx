import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import SignupPage from './features/auth/pages/signup'
import LoginPage from './features/auth/pages/login'
import ProfilePage from './features/profile/ProfilePage';
import HomePage from './features/home/HomePage';
import { getAccessToken } from './features/auth/services/authservice'
import AddItemPage from './features/addItem/AddItemPage';
import ViewUserProfilePage from "./features/userProfile/ViewUserProfilePage";
import ItemDetailPage from './features/item/pages/item';


function ProtectedRoute({ element, requiresProfile }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check if user has token
    const token = getAccessToken()
    setIsAuthenticated(!!token)
    setIsLoading(false)
  }, [])

  if (isLoading) {
    return <div className="flex min-h-screen items-center justify-center bg-slate-900">Loading...</div>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return element
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to={getAccessToken() ? "/home" : "/login"} replace />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/home" element={<ProtectedRoute element={<HomePage />} />} />
        <Route path="/profile" element={<ProtectedRoute element={<ProfilePage />} />} />
        <Route path="/user/:id" element={<ProtectedRoute element={<ViewUserProfilePage />} />} />
        <Route path="/add-item" element={<ProtectedRoute element={<AddItemPage />} />} />
        <Route path="/item/:id" element={<ProtectedRoute element={<ItemDetailPage />} />}} />
      </Routes>
    </Router>
  )
}

export default App