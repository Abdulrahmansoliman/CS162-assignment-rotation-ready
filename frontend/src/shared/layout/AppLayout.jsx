import { useState } from "react"
import { Link, useLocation, useNavigate } from "react-router-dom"
import { authService, clearTokens } from "@/features/auth/services/authservice"

const navLinks = [
  { to: "/home", label: "Home" },
  { to: "/profile", label: "Profile" },
  { to: "/add-item", label: "Contribute" },
]

const linkBase = "px-3 py-2 rounded-md text-sm font-medium transition-colors"

export default function AppLayout({ children }) {
  const location = useLocation()
  const navigate = useNavigate()
  const [isLoggingOut, setIsLoggingOut] = useState(false)

  const handleLogout = async () => {
    setIsLoggingOut(true)
    clearTokens()
    setIsLoggingOut(false)
    navigate("/login", { replace: true })
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <header className="bg-slate-900/80 backdrop-blur border-b border-slate-800 sticky top-0 z-20">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <Link to="/home" className="text-lg font-semibold tracking-tight text-white">
            Rotation Portal
          </Link>

          <nav className="flex items-center gap-1">
            {navLinks.map((link) => {
              const isActive = location.pathname.startsWith(link.to)
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  className={`${linkBase} ${
                    isActive
                      ? "bg-blue-600/80 text-white"
                      : "text-slate-300 hover:bg-slate-800/80 hover:text-white"
                  }`}
                >
                  {link.label}
                </Link>
              )
            })}
          </nav>

          <button
            onClick={handleLogout}
            disabled={isLoggingOut}
            className="rounded-md border border-slate-700 px-4 py-2 text-sm font-medium text-slate-200 hover:bg-slate-800 disabled:opacity-50"
          >
            {isLoggingOut ? "Signing out…" : "Logout"}
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
    </div>
  )
}
