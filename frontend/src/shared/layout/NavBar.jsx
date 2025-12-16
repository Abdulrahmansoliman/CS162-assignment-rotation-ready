import { useNavigate, useLocation } from "react-router-dom"
import { clearTokens } from "@/features/auth/services/authservice.js"
import { useEffect, useMemo, useState } from "react"
import { getCurrentUser } from "@/api/user"

// Locale-based colors matching HomePage
const localeColors = {
  usa: "#cc0000",
  china: "#1d9a5c",
  korea: "#c60c30",
  argentina: "#d9a300",
  india: "#ff9933",
  germany: "#4a90e2",
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
          background: linear-gradient(180deg, #1b1b1b 0%, #121212 60%, #0f0f0f 100%);
          border-right: 1px solid rgba(var(--accent-rgb), 0.18);
          box-shadow: 0 12px 36px rgba(0,0,0,0.35);
        }

        .rg-brand{
          padding: 18px 16px;
          display: flex;
          align-items: center;
          gap: 10px;
          cursor: pointer;
          border-bottom: 1px solid rgba(var(--accent-rgb), 0.22);
          position: relative;
        }
        .rg-brand::after{
          content:"";
          position:absolute;
          inset:0;
          background: radial-gradient(120px 60px at 20% 30%, rgba(var(--accent-rgb),0.25), transparent 70%);
          pointer-events:none;
        }
        .rg-brandTitle{
          font-size: 14px;
          font-weight: 700;
          letter-spacing: 0.3px;
          color: var(--accent);
        }
        .rg-brandSub{
          font-size: 11px;
          color: rgba(255,255,255,0.55);
          margin-top: 2px;
        }

        .rg-nav{
          padding: 12px 10px;
          display: flex;
          flex-direction: column;
          gap: 6px;
          flex: 1;
        }

        .rg-item{
          position: relative;
          width: 100%;
          border: 0;
          background: transparent;
          color: rgba(255,255,255,0.72);
          padding: 10px 12px;
          border-radius: 14px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 10px;
          text-align: left;
          transition: transform 120ms ease, background 120ms ease, color 120ms ease, box-shadow 120ms ease;
        }
        .rg-item:hover{
          background: rgba(255,255,255,0.06);
          color: rgba(255,255,255,0.95);
          transform: translateY(-1px);
        }
        .rg-item:focus-visible{
          outline: none;
          box-shadow: 0 0 0 3px rgba(var(--accent-rgb), 0.28);
        }

        .rg-item[data-active="true"]{
          background: rgba(var(--accent-rgb), 0.16);
          color: #fff;
          box-shadow: 0 0 0 1px rgba(var(--accent-rgb), 0.28) inset;
        }
        .rg-item[data-active="true"]::before{
          content:"";
          position:absolute;
          left: 6px;
          top: 10px;
          bottom: 10px;
          width: 3px;
          border-radius: 3px;
          background: var(--accent);
        }

        .rg-icon{
          width: 34px;
          height: 34px;
          border-radius: 12px;
          display: grid;
          place-items: center;
          background: rgba(255,255,255,0.06);
          box-shadow: 0 0 0 1px rgba(255,255,255,0.06) inset;
          font-size: 16px;
        }
        .rg-item[data-active="true"] .rg-icon{
          background: rgba(var(--accent-rgb), 0.22);
          box-shadow: 0 0 0 1px rgba(var(--accent-rgb), 0.35) inset;
        }

        .rg-label{
          font-size: 13px;
          font-weight: 600;
        }

        .rg-bottom{
          padding: 10px;
          border-top: 1px solid rgba(255,255,255,0.08);
        }

        .rg-logout:hover{
          background: rgba(239, 68, 68, 0.14);
          color: #fecaca;
          transform: none;
        }
        .rg-logout:focus-visible{
          box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.25);
        }
      `}</style>

      {/* Brand */}
      <div className="rg-brand" onClick={() => navigate("/home")}>
        <div className="rg-icon" style={{ background: "rgba(255,255,255,0.08)" }}>
          🗺️
        </div>
        <div style={{ position: "relative", zIndex: 1 }}>
          <div className="rg-brandTitle">Rotation Guide</div>
          <div className="rg-brandSub">Explore • Save • Contribute</div>
        </div>
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
        <button type="button" className="rg-item rg-logout" onClick={handleLogout}>
          <span className="rg-icon">🚪</span>
          <span className="rg-label">Logout</span>
        </button>
      </div>
    </aside>
  )
}
