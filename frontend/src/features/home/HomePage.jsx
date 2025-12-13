import React, { useEffect, useState } from "react";
import { fetchHomePageData } from "./services/homeService";
import { DEFAULT_LOCALE } from "../../config/localeConfig";
import "../../shared/styles/localeTransitions.css";

const categoryColors = [
    "#B80000", "#C97B2B", "#F3E2C7", "#002147", "#2D0036", "#B80000", "#C97B2B", "#002147", "#2D0036"
];

const iconMap = [
    "🏠", "🏛️", "🍽️", "🛒", "☕", "📖", "💊", "🚚", "🔗"
];

function HomePage() {
    const [categories, setCategories] = useState([]);
    const [places, setPlaces] = useState([]);
    const [search, setSearch] = useState("");
    const [filteredPlaces, setFilteredPlaces] = useState([]);
    const [view, setView] = useState("list");
    const [locale, setLocale] = useState(DEFAULT_LOCALE);
    const [userName, setUserName] = useState("User");

    useEffect(() => {
        const loadData = async () => {
            try {
                const data = await fetchHomePageData();
                setUserName(data.userName);
                setLocale(data.locale);
                setCategories(data.categories);
                setPlaces(data.places);
            } catch (e) {
                console.error("Failed to load home page data:", e);
            }
        };
        loadData();
    }, []);

    // Locale is set from backend and remains stable for the session

    useEffect(() => {
        setFilteredPlaces(
            places.filter(place =>
                place.name.toLowerCase().includes(search.toLowerCase())
            )
        );
    }, [search, places]);

    return (
        <div style={{ paddingBottom: "2rem" }}>
            <div className={`locale-container ${locale.cssClass}`} style={{ color: "white", padding: "3rem 2rem 2rem 2rem" }}>
                <div className={`locale-overlay absolute inset-0 ${locale.cssClass}`}></div>
                <h1 style={{ fontSize: "2.5rem", margin: 0, fontWeight: 300, letterSpacing: "1px", position: "relative", zIndex: 10, fontFamily: 'Fraunces, serif' }}>{locale.welcomeText}, {userName}</h1>
            </div>
            <div style={{ padding: "2rem", maxWidth: "1200px", margin: "0 auto" }}>
                <div style={{ display: "flex", gap: "1rem", marginBottom: "2rem" }}>
                    <input
                        type="text"
                        placeholder="Search..."
                        value={search}
                        onChange={e => setSearch(e.target.value)}
                        style={{
                            flex: 1, padding: "1rem 1.5rem", borderRadius: "8px",
                            border: "none", background: "#fff", color: "#333", fontSize: "1rem",
                            boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
                        }}
                    />
                    <button style={{
                        background: locale.color, color: "white", border: "none",
                        borderRadius: "8px", padding: "1rem 2rem", fontSize: "1rem", fontWeight: 600,
                        cursor: "pointer", transition: "background 0.3s"
                    }}>
                        Filter
                    </button>
                </div>
                <div style={{ display: "flex", gap: "1rem", marginBottom: "2rem", overflowX: "auto", paddingBottom: "0.5rem" }}>
                    {categories.map((cat, idx) => (
                        <div key={cat.id}
                            style={{
                                background: categoryColors[idx % categoryColors.length],
                                width: 90, height: 90, borderRadius: 16,
                                display: "flex", alignItems: "center", justifyContent: "center",
                                flexShrink: 0,
                                cursor: "pointer",
                                transition: "transform 0.2s",
                                boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
                                overflow: "hidden",
                                position: "relative"
                            }}
                            onMouseEnter={(e) => e.currentTarget.style.transform = "scale(1.05)"}
                            onMouseLeave={(e) => e.currentTarget.style.transform = "scale(1)"}
                        >
                            {cat.image ? (
                                <img 
                                    src={`data:image/png;base64,${cat.image}`}
                                    alt={cat.name}
                                    style={{
                                        width: "60%",
                                        height: "60%",
                                        objectFit: "contain"
                                    }}
                                />
                            ) : (
                                <span style={{ fontSize: 40 }}>{iconMap[idx % iconMap.length]}</span>
                            )}
                        </div>
                    ))}
                </div>
            <div style={{ display: "flex", alignItems: "center", marginBottom: 20 }}>
                <h3 style={{ margin: 0, fontSize: "1.1rem", fontWeight: 600 }}>All Places <span style={{ color: "#999" }}>({filteredPlaces.length})</span></h3>
                <div style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
                    <button
                        onClick={() => setView("list")}
                        style={{
                            background: view === "list" ? locale.color : "#fff",
                            color: view === "list" ? "#fff" : "#999",
                            border: "1px solid #ddd", borderRadius: 8, padding: 8,
                            cursor: "pointer", fontSize: "0.9rem", width: 36, height: 36,
                            display: "flex", alignItems: "center", justifyContent: "center"
                        }}>
                        ☰
                    </button>
                    <button
                        onClick={() => setView("grid")}
                        style={{
                            background: view === "grid" ? locale.color : "#fff",
                            color: view === "grid" ? "#fff" : "#999",
                            border: "1px solid #ddd", borderRadius: 8, padding: 8,
                            cursor: "pointer", fontSize: "0.9rem", width: 36, height: 36,
                            display: "flex", alignItems: "center", justifyContent: "center"
                        }}>
                        ▦
                    </button>
                </div>
            </div>
            <div style={{ display: view === "grid" ? "grid" : "block", gridTemplateColumns: view === "grid" ? "repeat(auto-fill, minmax(280px, 1fr))" : "none", gap: "1.5rem" }}>
                {filteredPlaces.map(place => (
                    <div key={place.id}
                        style={{
                            background: "#fff", borderRadius: 12, boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
                            padding: 20, marginBottom: view === "list" ? 16 : 0, display: "flex", flexDirection: view === "list" ? "row" : "column", alignItems: view === "list" ? "flex-start" : "flex-start", gap: 16
                        }}>
                        <div style={{ flex: 1 }}>
                            <div style={{ fontWeight: 600, fontSize: "1rem", marginBottom: 4 }}>{place.name}</div>
                            <div style={{ color: "#666", fontSize: "0.9rem", margin: "4px 0 8px 0", display: "flex", alignItems: "center", gap: 4 }}>
                                📍 {place.address} {place.distance && `${place.distance} km away`}
                            </div>
                            <div style={{ margin: "8px 0", display: "flex", gap: 6, flexWrap: "wrap" }}>
                                {place.tags && place.tags.map((tag, i) => (
                                    <span key={i} style={{
                                        background: tag === "Foreign Cards" ? "#b2f2bb" :
                                            tag === "English" ? "#e0b3ff" :
                                            tag === "Walk-in" ? "#fff3cd" :
                                            tag === "24/7" ? "#d1e7f5" :
                                            tag === "Fast service" ? "#f8d7da" : "#eee",
                                        color: tag === "English" ? "#333" : "#333", 
                                        borderRadius: 4, padding: "3px 8px", fontSize: "0.75rem", fontWeight: 500
                                    }}>{tag}</span>
                                ))}
                            </div>
                            <div style={{ color: "#4caf50", fontSize: "0.85rem", display: "flex", alignItems: "center", gap: 8 }}>
                                <span>✓ {place.verifiedCount || 0} verified</span>
                                <span style={{ color: "#999", fontSize: "0.85rem" }}>
                                    🕐 {place.lastVerified || "N/A"}
                                </span>
                            </div>
                        </div>
                        <div style={{ display: "flex", flexDirection: "column", gap: 8, alignItems: view === "list" ? "flex-end" : "stretch", flexShrink: 0, width: view === "list" ? "auto" : "100%" }}>
                            <div style={{ color: "#999", fontWeight: 600, fontSize: "1rem", minWidth: 40, textAlign: view === "list" ? "right" : "left" }}>
                                {"$".repeat(place.priceLevel || 1)}
                            </div>
                            <button style={{
                                background: locale.color, color: "#fff", border: "none",
                                borderRadius: 6, padding: "8px 16px", fontWeight: 600, fontSize: "0.85rem",
                                cursor: "pointer", transition: "background 0.3s", width: view === "list" ? "auto" : "100%"
                            }}>
                                View Details
                            </button>
                        </div>
                    </div>
                ))}
            </div>
            </div>
        </div>
    );
}

export default HomePage;