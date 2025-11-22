import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import SignupPage from './features/auth/pages/signup'
import LoginPage from './features/auth/pages/login'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/login" element={<LoginPage />} />
        {/* Add a default route if needed, e.g., redirect to /login */}
      </Routes>
    </Router>
  )
}

export default App