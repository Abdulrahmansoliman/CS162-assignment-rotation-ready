import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import SignupPage from './features/auth/pages/signup'
import LoginPage from './features/auth/pages/login'
import ProfilePage from './features/profile/ProfilePage';
import ViewUserProfilePage from "./features/userProfile/ViewUserProfilePage";
import ItemDetailPage from './features/item/pages/item';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/user/:id" element={<ViewUserProfilePage />} />
        <Route path="/item/:id" element={<ItemDetailPage />} />
      </Routes>
    </Router>
  )
}

export default App