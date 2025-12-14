import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import SignupPage from './features/auth/pages/signup'
import LoginPage from './features/auth/pages/login'
import ProfilePage from './features/profile/ProfilePage';
import HomePage from './features/home/HomePage';
import { getAccessToken } from './features/auth/services/authservice'

function ProtectedRoute({ element }) {
  const token = getAccessToken()
  
  if (!token) {
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
      </Routes>
    </Router>
  )
}

export default App
