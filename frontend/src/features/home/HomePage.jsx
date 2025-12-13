import React, { useEffect, useState } from "react";
import { getCurrentUser } from "../../api/user";
import { apiFetch } from "../../api";

const animationStyles = `
    @keyframes fadeInSlideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .home-container {
        background: linear-gradient(135deg, #cc0000 0%, #ff4444 100%);
        background-size: cover;
        background-position: center;
        transition: background-image 0.8s ease-out, background 0.8s ease-out;
        position: relative;
    }

    .home-container.show-photo {
        background-image: url('/sf.jpg');
        background-size: cover;
        background-position: center;
        background-blend-mode: overlay;
    }

    .home-container.transition-green {
        background: linear-gradient(135deg, #1d9a5c 0%, #2fb872 100%) !important;
        background-image: url('/tp.jpg') !important;
        background-size: 120% !important;
        background-repeat: no-repeat !important;
        background-position: center;
        background-blend-mode: overlay;
    }

    .home-container.transition-korea {
        background: linear-gradient(135deg, #c60c30 0%, #e91e63 100%) !important;
        background-image: url('/sl.jpg') !important;
        background-size: cover !important;
        background-position: center;
        background-blend-mode: overlay;
    }

    .home-container.transition-argentina {
        background: linear-gradient(135deg, #d9a300 0%, #e6b800 100%) !important;
        background-image: url('/ba.jpg') !important;
        background-size: cover !important;
        background-position: center;
        background-blend-mode: overlay;
    }

    .home-container.transition-india {
        background: linear-gradient(135deg, #ff9933 0%, #ffcc33 100%) !important;
        background-image: url('/hyd.jpg') !important;
        background-size: cover !important;
        background-position: center;
        background-blend-mode: overlay;
    }

    .home-container.transition-germany {
        background: linear-gradient(135deg, #4a90e2 0%, #7bb3e8 100%) !important;
        background-image: url('/br.jpg') !important;
        background-size: cover !important;
        background-position: center;
        background-blend-mode: overlay;
    }

    .overlay {
        background-color: rgba(204, 0, 0, 0.8);
        transition: background-color 0.8s ease-out;
    }

    .overlay.show-photo {
        background-color: rgba(204, 0, 0, 0.5);
    }

    .overlay.transition-green {
        background-color: rgba(29, 154, 92, 0.7) !important;
    }

    .overlay.transition-korea {
        background-color: rgba(198, 12, 48, 0.6) !important;
    }

    .overlay.transition-argentina {
        background-color: rgba(217, 163, 0, 0.65) !important;
    }

    .overlay.transition-india {
        background-color: rgba(255, 153, 51, 0.62) !important;
    }

    .overlay.transition-germany {
        background-color: rgba(122, 179, 232, 0.65) !important;
    }

    .fade-in {
        animation: fadeInSlideUp 0.8s ease-out 1.2s forwards;
        opacity: 0;
    }
`;

// Category color palettes per locale
const localeCategoryPalettes = {
    usa: ['#B80000', '#C97B2B', '#F3E2C7', '#002147', '#2D0036', '#B80000', '#C97B2B', '#002147', '#2D0036'],
    china: ['#1d9a5c', '#2fb872', '#45c984', '#5dd996', '#74e9a8', '#1d9a5c', '#2fb872', '#45c984', '#5dd996'],
    korea: ['#c60c30', '#e91e63', '#f06292', '#f48fb1', '#f8bbd9', '#c60c30', '#e91e63', '#f06292', '#f48fb1'],
    argentina: ['#d9a300', '#e6b800', '#f0c800', '#fad700', '#ffe680', '#d9a300', '#e6b800', '#f0c800', '#fad700'],
    india: ['#ff9933', '#ffb347', '#ffcc66', '#ffe680', '#fff0b3', '#ff9933', '#ffb347', '#ffcc66', '#ffe680'],
    germany: ['#4a90e2', '#6ba3e8', '#8cb6ee', '#adc9f4', '#cedcfa', '#4a90e2', '#6ba3e8', '#8cb6ee', '#adc9f4']
};

function HomePage() {
    const [categories, setCategories] = useState([]);
    const [places, setPlaces] = useState([]);
    const [search, setSearch] = useState("");
    const [filteredPlaces, setFilteredPlaces] = useState([]);
    const [view, setView] = useState("list");
    const [currentLocale, setCurrentLocale] = useState('usa');
    const [activeCategoryId, setActiveCategoryId] = useState(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                // Fetch current user
                const user = await getCurrentUser();
                console.log("User data from backend:", user);
                
                // Set user name from first_name and last_name
                const fullName = `${user.first_name || ''} ${user.last_name || ''}`.trim();
                setUserName(fullName || user.email || "User");

                // Map rotation city id to locale - get city_id from rotation_city object
                const cityId = user.rotation_city?.city_id;
                console.log("Extracted city_id:", cityId);
                const localeMap = { 1: 'usa', 2: 'china', 3: 'korea', 4: 'argentina', 5: 'india', 6: 'germany' };
                const selectedLocale = localeMap[cityId] || 'usa';
                console.log("Selected locale:", selectedLocale);
                setCurrentLocale(selectedLocale);

                // Fetch categories with images
                const cats = await apiFetch("/category/", { method: "GET" });
                setCategories(cats.map(c => ({ 
                    id: c.category_id, 
                    name: c.category_name,
                    image: c.category_pic // base64 image data
                })));

                // Fetch items for user's rotation city
                const items = await apiFetch("/item/", { method: "GET" });
                console.log("Items from backend:", items);
                setPlaces(items.map(item => ({
                    id: item.item_id,
                    name: item.name,
                    address: item.location,
                    distance: item.walking_distance ? (item.walking_distance / 1000).toFixed(1) : null,
                    tags: (item.tags || []).map(t => t.tag_name || t.name),
                    verifiedCount: item.number_of_verifications || 0,
                    lastVerified: item.created_at ? new Date(item.created_at).toLocaleDateString() : null,
                    priceLevel: 1,
                    categories: (item.categories || []).map(c => ({ id: c.category_id, name: c.category_name })),
                })));
            } catch (e) {
                console.error(e);
            }
        };
        loadData();
    }, []);

    // Locale is set from backend and remains stable for the session

    useEffect(() => {
        const bySearch = (p) => p.name.toLowerCase().includes(search.toLowerCase());
        const byCategory = (p) => !activeCategoryId || (p.categories || []).some(c => c.id === activeCategoryId);
        setFilteredPlaces(places.filter(p => bySearch(p) && byCategory(p)));
    }, [search, places, activeCategoryId]);

    const getLocaleClass = () => {
        const classMap = {
            usa: 'show-photo',
            china: 'transition-green',
            korea: 'transition-korea',
            argentina: 'transition-argentina',
            india: 'transition-india',
            germany: 'transition-germany'
        }
        return classMap[currentLocale] || 'show-photo'
    }

    const getLocaleColor = () => {
        const colorMap = {
            usa: '#cc0000',
            china: '#2fb872',
            korea: '#e91e63',
            argentina: '#d9a300',
            india: '#ffcc33',
            germany: '#7bb3e8'
        }
        return colorMap[currentLocale] || '#cc0000'
    }

    const [userName, setUserName] = useState("User");

    const getLocaleText = () => {
        const textMap = {
            usa: 'Welcome',
            china: '欢迎',
            korea: '어서 오세요',
            argentina: 'Bienvenido',
            india: 'స్వాగతం',
            germany: 'Willkommen'
        };
        return textMap[currentLocale] || 'Welcome';
    };

    return (
        <div style={{ paddingBottom: "2rem" }}>
            <style>{animationStyles}</style>
            <div className={`home-container ${getLocaleClass()}`} style={{ color: "white", padding: "3rem 2rem 2rem 2rem" }}>
                <div className={`overlay absolute inset-0 ${getLocaleClass()}`}></div>
                <h1 style={{ fontSize: "2.5rem", margin: 0, fontWeight: 300, letterSpacing: "1px", position: "relative", zIndex: 10, fontFamily: 'Fraunces, serif' }}>{getLocaleText()}, {userName}</h1>
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
                        background: getLocaleColor(), color: "white", border: "none",
                        borderRadius: "8px", padding: "1rem 2rem", fontSize: "1rem", fontWeight: 600,
                        cursor: "pointer", transition: "background 0.3s"
                    }}>
                        Filter
                    </button>
                </div>
                <div style={{ display: "flex", gap: "1rem", marginBottom: "2rem", overflowX: "auto", paddingBottom: "0.5rem" }}>
                    {categories.map((cat, idx) => {
                        const palette = localeCategoryPalettes[currentLocale] || localeCategoryPalettes['usa'];
                        const bg = palette[idx % palette.length];
                        const isActive = activeCategoryId === cat.id;
                        return (
                            <div key={cat.id}
                                onClick={() => setActiveCategoryId(isActive ? null : cat.id)}
                                style={{
                                    background: bg,
                                    width: 90, height: 90, borderRadius: 16,
                                    display: "flex", alignItems: "center", justifyContent: "center",
                                    flexShrink: 0,
                                    cursor: "pointer",
                                    transition: "transform 0.2s, box-shadow 0.2s",
                                    boxShadow: isActive ? "0 0 0 3px rgba(255,255,255,0.9)" : "0 2px 8px rgba(0,0,0,0.1)",
                                    overflow: "hidden",
                                    position: "relative",
                                    border: isActive ? "2px solid #fff" : "none"
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
                                    <span style={{ fontSize: 14, color: "#fff", fontWeight: 700 }}>{cat.name}</span>
                                )}
                            </div>
                        );
                    })}
                </div>
            <div style={{ display: "flex", alignItems: "center", marginBottom: 20 }}>
                <h3 style={{ margin: 0, fontSize: "1.1rem", fontWeight: 600 }}>All Places <span style={{ color: "#999" }}>({filteredPlaces.length})</span></h3>
                <div style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
                    <button
                        onClick={() => setView("list")}
                        style={{
                            background: view === "list" ? getLocaleColor() : "#fff",
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
                            background: view === "grid" ? getLocaleColor() : "#fff",
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
                                background: getLocaleColor(), color: "#fff", border: "none",
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