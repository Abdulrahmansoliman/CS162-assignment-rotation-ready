import { useNavigate, useLocation } from "react-router-dom"
import { clearTokens } from "@/features/auth/services/authservice.js"
import { useEffect, useMemo, useState } from "react"
import { getCurrentUser } from "@/api/user"

const localeColors = {
  usa: "#cc0000",
  china: "#2c6e49",
  korea: "#da627d",
  argentina: "#d9a300",
  india: "#ff9505",
  germany: "#007ea7",
}

export default function NavBar() {
  const navigate = useNavigate()
  const location = useLocation()
  const [themeColor, setThemeColor] = useState("#3b82f6")

  useEffect(() => {
    let mounted = true

    async function loadUserTheme() {
      try {
        const user = await getCurrentUser()
        const cityName = user.rotation_city?.name?.toLowerCase() || ""

        const localeMap = {
          "san francisco": "usa",
          taipei: "china",
          seoul: "korea",
          "buenos aires": "argentina",
          hyderabad: "india",
          berlin: "germany",
        }

        const locale = localeMap[cityName] || "usa"
        if (mounted) setThemeColor(localeColors[locale])
      } catch (err) {
        console.error("Failed to load user theme:", err)
      }
    }

    loadUserTheme()
    
    const handleCityChange = () => {
      loadUserTheme()
    }
    
    window.addEventListener('cityChanged', handleCityChange)
    
    return () => {
      mounted = false
      window.removeEventListener('cityChanged', handleCityChange)
    }
  }, [])

  const handleLogout = () => {
    clearTokens()
    navigate("/login", { replace: true })
  }

  const isActive = (path) => location.pathname === path

  const navItems = useMemo(
    () => [
      { path: "/home", label: "Home", icon: "🏠" },
      { path: "/profile", label: "Profile", icon: "👤" },
      { path: "/add-item", label: "Contribute", icon: "➕" },
    ],
    []
  )

  return (
    <aside className="nav-sidebar" style={{ "--accent": themeColor }}>
      <style>{`
        .nav-sidebar {
          width: 200px;
          min-height: 100vh;
          background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
          position: fixed;
          left: 0;
          top: 0;
          z-index: 100;
          display: flex;
          flex-direction: column;
          border-right: 1px solid rgba(255, 255, 255, 0.1);
          box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3);
        }

        .nav-brand {
          padding: 24px 20px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          cursor: pointer;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 8px;
        }

        .nav-brand-logo {
          font-size: 32px;
        }

        .nav-brand-title {
          font-size: 18px;
          font-weight: 700;
          color: white;
          font-family: 'Fraunces', serif;
          letter-spacing: 0.5px;
          white-space: nowrap;
        }

        .nav-brand-subtitle {
          font-size: 10px;
          color: rgba(255, 255, 255, 0.5);
          letter-spacing: 1px;
          text-transform: lowercase;
        }

        .nav-menu {
          padding: 24px 16px;
          display: flex;
          flex-direction: column;
          gap: 8px;
          flex: 1;
        }

        .nav-item {
          width: 100%;
          border: none;
          background: rgba(255, 255, 255, 0.05);
          color: rgba(255, 255, 255, 0.7);
          padding: 12px 16px;
          border-radius: 12px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 12px;
          text-align: left;
          transition: all 200ms ease;
          font-size: 14px;
          font-weight: 500;
        }

        .nav-item:hover {
          background: rgba(255, 255, 255, 0.1);
          color: white;
          transform: translateX(2px);
        }

        .nav-item[data-active="true"] {
          background: var(--accent);
          color: white;
          border: 1px solid var(--accent);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }

        .nav-icon {
          font-size: 18px;
          width: 24px;
          text-align: center;
        }

        .nav-bottom {
          padding: 16px;
          border-top: 1px solid rgba(255, 255, 255, 0.1);
        }

        .nav-logout {
          background: rgba(255, 255, 255, 0.05);
          color: rgba(255, 255, 255, 0.7);
          border: none;
        }

        .nav-logout:hover {
          background: var(--accent);
          color: white;
          transform: translateX(2px);
        }
      `}</style>

      {/* Brand */}
      <div className="nav-brand" onClick={() => navigate("/home")}>
        <span className="nav-brand-logo">🗺️</span>
        <div className="nav-brand-title">Rotation Ready</div>
        <div className="nav-brand-subtitle">explore · rotate · repeat</div>
      </div>

      {/* Navigation */}
      <nav className="nav-menu" aria-label="Main navigation">
        {navItems.map((item) => (
          <button
            key={item.path}
            type="button"
            className="nav-item"
            data-active={isActive(item.path)}
            onClick={() => navigate(item.path)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      {/* Logout */}
      <div className="nav-bottom">
        <button type="button" className="nav-item nav-logout" onClick={handleLogout}>
          <span className="nav-icon">🚪</span>
          <span>Logout</span>
        </button>
      </div>
    </aside>
  )
}
