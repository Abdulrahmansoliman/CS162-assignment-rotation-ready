import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import SignupPage from './features/auth/pages/signup'
import LoginPage from './features/auth/pages/login'
import ProfilePage from './features/profile/ProfilePage';
import { getAccessToken } from './features/auth/services/authservice'
import ViewUserProfilePage from "./features/userProfile/ViewUserProfilePage";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to={getAccessToken() ? "/profile" : "/login"} replace />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/user/:id" element={<ViewUserProfilePage />} />
      </Routes>
    </Router>
  )
}

export default App