import { useNavigate, useLocation } from "react-router-dom"
import { clearTokens } from "@/features/auth/services/authservice.js"
import { useEffect, useMemo, useState } from "react"
import { getCurrentUser } from "@/api/user"

// Locale-based colors matching HomePage
const localeColors = {
  usa: "#cc0000",
  china: "#2c6e49",
  korea: "#da627d",
  argentina: "#d9a300",
  india: "#ff9505",
  germany: "#007ea7",
}

function hexToRgb(hex) {
  const h = (hex || "").replace("#", "")
  if (h.length !== 6) return { r: 59, g: 130, b: 246 } // fallback blue
  const n = parseInt(h, 16)
  return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 }
}

export default function NavBar() {
  const navigate = useNavigate()
  const location = useLocation()
  const [themeColor, setThemeColor] = useState("#3b82f6") // default blue

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
    
    // Listen for city change events
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

  const { r, g, b } = hexToRgb(themeColor)

  return (
    <aside
      className="rg-sidebar"
      style={{
        "--accent": themeColor,
        "--accent-rgb": `${r}, ${g}, ${b}`,
        "--w": "200px", // change to 220px if you want slightly wider
      }}
    >
      <style>{`
        .rg-sidebar{
          width: var(--w);
          min-height: 100vh;
          position: fixed;
          left: 0; top: 0;
          z-index: 100;
          display: flex;
          flex-direction: column;
          background: linear-gradient(180deg, var(--accent) 0%, rgba(var(--accent-rgb), 0.85) 100%);
          border-right: 1px solid rgba(255, 255, 255, 0.2);
          box-shadow: 4px 0 32px rgba(0,0,0,0.15);
        }

        .rg-brand{
          padding: 24px 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        .rg-brandTitle{
          font-size: 24px;
          font-weight: 700;
          letter-spacing: 0.5px;
          color: white;
          font-family: 'Fraunces', serif;
          text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .rg-nav{
          padding: 20px 16px;
          display: flex;
          flex-direction: column;
          gap: 10px;
          flex: 1;
        }

        .rg-item{
          position: relative;
          width: 100%;
          border: 0;
          background: rgba(255, 255, 255, 0.25);
          color: white;
          padding: 14px 18px;
          border-radius: 50px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 12px;
          text-align: left;
          transition: all 250ms cubic-bezier(0.4, 0, 0.2, 1);
          backdrop-filter: blur(8px);
          border: 1px solid rgba(255, 255, 255, 0.15);
        }
        .rg-item:hover{
          background: rgba(255, 255, 255, 0.4);
          transform: translateX(4px);
          box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }
        .rg-item:focus-visible{
          outline: none;
          box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.4);
        }

        .rg-item[data-active="true"]{
          background: white;
          color: var(--accent);
          transform: translateX(4px);
          box-shadow: 0 6px 20px rgba(0,0,0,0.2);
          border: 1px solid rgba(255, 255, 255, 0.9);
        }

        .rg-icon{
          width: 36px;
          height: 36px;
          border-radius: 50%;
          display: grid;
          place-items: center;
          background: rgba(255,255,255,0.3);
          font-size: 18px;
          transition: all 250ms ease;
        }
        .rg-item[data-active="true"] .rg-icon{
          background: rgba(var(--accent-rgb), 0.15);
        }

        .rg-label{
          font-size: 14px;
          font-weight: 600;
          letter-spacing: 0.2px;
        }

        .rg-bottom{
          padding: 16px;
          border-top: 1px solid rgba(255, 255, 255, 0.2);
        }
      `}</style>

      {/* Brand */}
      <div className="rg-brand" onClick={() => navigate("/home")}>
        <div className="rg-brandTitle">Rotation Guide</div>
      </div>

      {/* Nav */}
      <nav className="rg-nav" aria-label="Sidebar navigation">
        {navItems.map((item) => (
          <button
            key={item.path}
            type="button"
            className="rg-item"
            data-active={isActive(item.path)}
            onClick={() => navigate(item.path)}
          >
            <span className="rg-icon">{item.icon}</span>
            <span className="rg-label">{item.label}</span>
          </button>
        ))}
      </nav>

      {/* Logout */}
      <div className="rg-bottom">
        <button type="button" className="rg-item" onClick={handleLogout}>
          <span className="rg-icon">🚪</span>
          <span className="rg-label">Logout</span>
        </button>
      </div>
    </aside>
  )
}
