import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import SignupPage from './features/auth/pages/signup'
import LoginPage from './features/auth/pages/login'
import ProfilePage from './features/profile/ProfilePage';
import { getAccessToken } from './features/auth/services/authservice'

function App() {
  return (
    <Router>
      <Routes>
<<<<<<< HEAD
        <Route path="/" element={<LoginPage />} />
=======
        <Route path="/" element={<Navigate to={getAccessToken() ? "/profile" : "/login"} replace />} />
>>>>>>> 9f73737c27ab8e09dbdc43ba0109785d2cf616d1
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
    </Router>
  )
}

export default App