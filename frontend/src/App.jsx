import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import SignupPage from './features/auth/pages/signup'
import LoginPage from './features/auth/pages/login'
import ProfilePage from './features/profile/ProfilePage'
import AddItemPage from './features/addItem/AddItemPage';
import ViewUserProfilePage from "./features/userProfile/ViewUserProfilePage";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/add-item" element={<AddItemPage />} />
        <Route path="/user/:id" element={<ViewUserProfilePage />} />
      </Routes>
    </Router>
  )
}

export default App