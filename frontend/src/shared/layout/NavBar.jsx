import { useNavigate, useLocation } from "react-router-dom"
import { clearTokens } from "@/features/auth/services/authservice.js"
import { useEffect, useMemo, useState } from "react"
import { getCurrentUser } from "@/api/user"

const localeColors = {
<<<<<<< HEAD
  usa: "#A50404",
  china: "#2c6e49",
  korea: "#da627d",
=======
  usa: "#cc0000",
  china: "#1d9a5c",
  korea: "#c60c30",
>>>>>>> 7d9d74130f074d479a37109a13798d426c2cd339
  argentina: "#d9a300",
  india: "#ff9933",
  germany: "#4a90e2",
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
<<<<<<< HEAD
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
=======
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
>>>>>>> 7d9d74130f074d479a37109a13798d426c2cd339
          flex: 1;
        }

        .nav-item {
          width: 100%;
<<<<<<< HEAD
          border: none;
          background: rgba(255, 255, 255, 0.05);
          color: rgba(255, 255, 255, 0.7);
          padding: 12px 16px;
          border-radius: 12px;
=======
          border: 0;
          background: transparent;
          color: rgba(255,255,255,0.72);
          padding: 10px 12px;
          border-radius: 14px;
>>>>>>> 7d9d74130f074d479a37109a13798d426c2cd339
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 10px;
          text-align: left;
<<<<<<< HEAD
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
=======
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
>>>>>>> 7d9d74130f074d479a37109a13798d426c2cd339
        }
      `}</style>

      {/* Brand */}
<<<<<<< HEAD
      <div className="nav-brand" onClick={() => navigate("/home")}>
        <span className="nav-brand-logo">🗺️</span>
        <div className="nav-brand-title">Rotation Ready</div>
        <div className="nav-brand-subtitle">explore · rotate · repeat</div>
=======
      <div className="rg-brand" onClick={() => navigate("/home")}>
        <div className="rg-icon" style={{ background: "rgba(255,255,255,0.08)" }}>
          🗺️
        </div>
        <div style={{ position: "relative", zIndex: 1 }}>
          <div className="rg-brandTitle">Rotation Guide</div>
          <div className="rg-brandSub">Explore • Save • Contribute</div>
        </div>
>>>>>>> 7d9d74130f074d479a37109a13798d426c2cd339
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
<<<<<<< HEAD
      <div className="nav-bottom">
        <button type="button" className="nav-item nav-logout" onClick={handleLogout}>
          <span className="nav-icon">🚪</span>
          <span>Logout</span>
=======
      <div className="rg-bottom">
        <button type="button" className="rg-item rg-logout" onClick={handleLogout}>
          <span className="rg-icon">🚪</span>
          <span className="rg-label">Logout</span>
>>>>>>> 7d9d74130f074d479a37109a13798d426c2cd339
        </button>
      </div>
    </aside>
  )
}
