import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { getCurrentUser } from "../../api/user";
import { apiFetch } from "../../api";

// Example API endpoints
const CATEGORIES_API = "/api/categories";
const PLACES_API = "/api/places";

// Locale-based category palettes (from provided swatches)
const localeCategoryPalettes = {
    usa: ["#E31B23", "#9A2623", "#5C2A28", "#E53935", "#A63A3A"],
    china: ["#9AD9C2", "#B8E7F4", "#D7F3FF", "#F7CDE5", "#A4D7E1"],
    korea: ["#0F1B4C", "#1F3B73", "#D67AB1", "#F0A6C1", "#F7C7DC"],
    argentina: ["#5A8CE8", "#7FB3F4", "#F5A3C7", "#FADF6A", "#FFCF5C"],
    india: ["#CC5803", "#E2711D", "#FF9505", "#FFB627", "#FFC971"],
    germany: ["#94D3FC", "#A3A88A", "#42481C", "#696572", "#94D3FC"],
};

const iconMap = [
    "🏠", "🏛️", "🍽️", "🛒", "☕", "📖", "💊", "🚚", "🔗"
];
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

    @keyframes welcomeFadeUp {
        from { opacity: 0; transform: translateY(24px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes contentFadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
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
        background: linear-gradient(135deg, #6d70bd 0%, #8b6fc3 100%) !important;
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

    .welcome-hero {
        opacity: 0;
        animation: welcomeFadeUp 0.8s ease-out forwards;
    }

    .content-fade-in {
        opacity: 0;
        animation: contentFadeIn 0.7s ease-out 0.2s forwards;
    }
`;

function HomePage() {
    const [categories, setCategories] = useState([]);
    const [places, setPlaces] = useState([]);
    const [search, setSearch] = useState("");
    const [filteredPlaces, setFilteredPlaces] = useState([]);
    const [view, setView] = useState("list");
    const [currentLocale, setCurrentLocale] = useState('usa');
    const [activeCategoryId, setActiveCategoryId] = useState(null);
    const [selectedConditions, setSelectedConditions] = useState([]);
    const [selectedHours, setSelectedHours] = useState([]);
    const [selectedPrices, setSelectedPrices] = useState([]);
    const [distanceLimit, setDistanceLimit] = useState(null);
    const [maxDistance, setMaxDistance] = useState(0);
    const [showFilterMenu, setShowFilterMenu] = useState(false);
    const [showContent, setShowContent] = useState(false);

    useEffect(() => {
        const loadData = async () => {
            try {
                // Fetch current user
                const user = await getCurrentUser();
                console.log("User data from backend:", user);
                
                // Set user name from first_name and last_name
                const firstName = (user.first_name || '').trim();
                setUserName(firstName || user.email || "User");

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
                const mappedItems = items.map(item => ({
                    id: item.item_id,
                    name: item.name,
                    address: item.location,
                    distanceMeters: item.walking_distance || null,
                    distanceKm: item.walking_distance ? (item.walking_distance / 1000).toFixed(1) : null,
                    tags: (item.tags || []).map(t => ({
                        id: t.tag_id,
                        name: t.name,
                        valueType: t.value_type,
                        value: t.value
                    })),
                    verifiedCount: item.number_of_verifications || 0,
                    lastVerified: item.created_at ? new Date(item.created_at).toLocaleDateString() : null,
                    priceLevel: 1,
                    categories: (item.categories || []).map(c => ({ id: c.category_id, name: c.category_name })),
                }));

                setPlaces(mappedItems);

                const maxDist = Math.max(0, ...mappedItems.map(i => i.distanceMeters || 0));
                setMaxDistance(maxDist || 0);
                setDistanceLimit(maxDist || null);
            } catch (e) {
                console.error(e);
            }
        };
        loadData();
        setShowContent(true);
    }, []);

    // Locale is set from backend and remains stable for the session

    useEffect(() => {
        const bySearch = (p) => p.name.toLowerCase().includes(search.toLowerCase());
        const byCategory = (p) => !activeCategoryId || (p.categories || []).some(c => c.id === activeCategoryId);
        const byDistance = (p) => !distanceLimit || !p.distanceMeters || p.distanceMeters <= distanceLimit;

        const hasTagValue = (p, tagName, values) => {
            if (!values.length) return true;
            return (p.tags || []).some(t => t.name === tagName && values.includes(String(t.value)));
        };

        const byCondition = (p) => hasTagValue(p, 'Condition', selectedConditions);
        const byHours = (p) => hasTagValue(p, 'Operating Hours', selectedHours);
        const byPrice = (p) => hasTagValue(p, 'Price Range', selectedPrices);

        setFilteredPlaces(places.filter(p => bySearch(p) && byCategory(p) && byDistance(p) && byCondition(p) && byHours(p) && byPrice(p)));
    }, [search, places, activeCategoryId, selectedConditions, selectedHours, selectedPrices, distanceLimit]);

    const toggleValue = (setter, current) => (val) => {
        setter(prev => prev.includes(val) ? prev.filter(v => v !== val) : [...prev, val]);
    };

    const toggleCondition = toggleValue(setSelectedConditions);
    const toggleHours = toggleValue(setSelectedHours);
    const togglePrice = toggleValue(setSelectedPrices);

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
            china: '#6fbec7',
            korea: '#d67ab1',
            argentina: '#5a8ce8',
            india: '#cc5803',
            germany: '#42481c'
        }
        return colorMap[currentLocale] || '#cc0000'
    }

    const getOverlayShadowColor = () => {
        const shadowMap = {
            usa: 'rgba(204, 0, 0, 0.3)',
            china: 'rgba(29, 154, 92, 0.3)',
            korea: 'rgba(198, 12, 48, 0.3)',
            argentina: 'rgba(233, 174, 66, 0.3)',
            india: 'rgba(255, 153, 51, 0.3)',
            germany: 'rgba(122, 179, 232, 0.3)'
        }
        return shadowMap[currentLocale] || 'rgba(204, 0, 0, 0.3)'
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

    const palette = localeCategoryPalettes[currentLocale] || localeCategoryPalettes['usa'];
    const conditionColor = palette[0] || getLocaleColor();
    const hoursColor = palette[1] || getLocaleColor();
    const priceColor = palette[2] || getLocaleColor();
    const distanceColor = palette[3] || getLocaleColor();

    return (
        <div style={{ paddingBottom: "2rem" }}>
            <style>{animationStyles}</style>
            <div className={`home-container ${getLocaleClass()}`} style={{ color: "white", padding: "3rem 2rem 2rem 2rem" }}>
                <div className={`overlay absolute inset-0 ${getLocaleClass()}`}></div>
                <h1 className="welcome-hero" style={{ fontSize: "2.5rem", margin: 0, fontWeight: 300, letterSpacing: "1px", position: "relative", zIndex: 10, fontFamily: 'Fraunces, serif' }}>
                    {getLocaleText()}, <Link to="/profile" style={{ color: "inherit", textDecoration: "underline", textUnderlineOffset: "4px", cursor: "pointer" }}>{userName}</Link>
                </h1>
            </div>
            <div className={showContent ? "content-fade-in" : ""} style={{ padding: "2rem", maxWidth: "1200px", margin: "0 auto" }}>
                <div style={{ display: "flex", gap: "1rem", marginBottom: "2rem" }}>
                    <input
                        type="text"
                        placeholder="Search..."
                        value={search}
                        onChange={e => setSearch(e.target.value)}
                        style={{
                            flex: 1, padding: "1rem 1.5rem", borderRadius: "8px",
                            border: "none", background: "#fff", color: "#333", fontSize: "1rem",
                            boxShadow: `0 4px 12px ${getOverlayShadowColor()}`
                        }}
                    />
                    <div style={{ position: "relative" }}>
                        <button onClick={() => setShowFilterMenu(!showFilterMenu)} style={{
                            background: getLocaleColor(), color: "white", border: "none",
                            borderRadius: "8px", padding: "1rem 2rem", fontSize: "1rem", fontWeight: 600,
                            cursor: "pointer", transition: "background 0.3s"
                        }}>
                            Filters ▾
                        </button>
                        {showFilterMenu && (
                            <div style={{
                                position: "absolute",
                                right: 0,
                                marginTop: "0.5rem",
                                background: "#ffffff",
                                borderRadius: "12px",
                                boxShadow: "0 10px 30px rgba(0,0,0,0.15)",
                                padding: "1rem",
                                minWidth: "320px",
                                zIndex: 20,
                                display: "grid",
                                gap: "1rem"
                            }}>
                                <div>
                                    <div style={{ fontWeight: 700, marginBottom: "0.35rem", color: "#333" }}>Distance (m)</div>
                                    <input type="range" min={0} max={Math.max(maxDistance, 1000)} step={50} value={distanceLimit || 0}
                                        onChange={(e) => setDistanceLimit(Number(e.target.value) || null)}
                                        style={{ width: "100%", accentColor: distanceColor }} />
                                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", color: "#666", marginTop: "0.25rem" }}>
                                        <span>0</span>
                                        <span>{distanceLimit ? `${distanceLimit} m` : 'Any'}</span>
                                        <span>{Math.max(maxDistance, 1000)} m</span>
                                    </div>
                                </div>

                                <div>
                                    <div style={{ fontWeight: 700, marginBottom: "0.35rem", color: "#333" }}>Condition</div>
                                    <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
                                        {['Excellent','Good','Fair'].map(val => {
                                            const on = selectedConditions.includes(val);
                                            return (
                                                <button key={val} onClick={() => toggleCondition(val)} style={{
                                                    border: "1px solid #ddd",
                                                    background: on ? conditionColor : "#f7f7f8",
                                                    color: on ? "#fff" : "#444",
                                                    borderRadius: "999px",
                                                    padding: "6px 12px",
                                                    fontSize: "0.85rem",
                                                    cursor: "pointer",
                                                    transition: "all 0.2s"
                                                }}>{val}</button>
                                            );
                                        })}
                                    </div>
                                </div>

                                <div>
                                    <div style={{ fontWeight: 700, marginBottom: "0.35rem", color: "#333" }}>Operating Hours</div>
                                    <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
                                        {["Morning (6AM-12PM)", "Afternoon (12PM-6PM)", "Evening (6PM-12AM)"].map(val => {
                                            const on = selectedHours.includes(val);
                                            return (
                                                <button key={val} onClick={() => toggleHours(val)} style={{
                                                    border: "1px solid #ddd",
                                                    background: on ? hoursColor : "#f7f7f8",
                                                    color: on ? "#fff" : "#444",
                                                    borderRadius: "999px",
                                                    padding: "6px 12px",
                                                    fontSize: "0.85rem",
                                                    cursor: "pointer",
                                                    transition: "all 0.2s"
                                                }}>{val}</button>
                                            );
                                        })}
                                    </div>
                                </div>

                                <div>
                                    <div style={{ fontWeight: 700, marginBottom: "0.35rem", color: "#333" }}>Price Range</div>
                                    <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
                                        {["Budget", "Mid-Range", "Premium"].map(val => {
                                            const on = selectedPrices.includes(val);
                                            return (
                                                <button key={val} onClick={() => togglePrice(val)} style={{
                                                    border: "1px solid #ddd",
                                                    background: on ? priceColor : "#f7f7f8",
                                                    color: on ? "#fff" : "#444",
                                                    borderRadius: "999px",
                                                    padding: "6px 12px",
                                                    fontSize: "0.85rem",
                                                    cursor: "pointer",
                                                    transition: "all 0.2s"
                                                }}>{val}</button>
                                            );
                                        })}
                                    </div>
                                </div>

                                <div style={{ display: "flex", justifyContent: "space-between", marginTop: "0.25rem" }}>
                                    <button onClick={() => { setSelectedConditions([]); setSelectedHours([]); setSelectedPrices([]); setDistanceLimit(maxDistance || null); }} style={{
                                        background: "#f1f1f4", border: "1px solid #e0e0e5", color: "#444",
                                        borderRadius: "8px", padding: "0.5rem 0.9rem", cursor: "pointer"
                                    }}>Clear</button>
                                    <button onClick={() => setShowFilterMenu(false)} style={{
                                        background: getLocaleColor(), border: "none", color: "#fff",
                                        borderRadius: "8px", padding: "0.5rem 0.9rem", cursor: "pointer",
                                        fontWeight: 600
                                    }}>Done</button>
                                </div>
                            </div>
                        )}
                    </div>
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
                                📍 {place.address} {place.distanceKm && `${place.distanceKm} km away`}
                            </div>
                            <div style={{ margin: "8px 0", display: "flex", gap: 6, flexWrap: "wrap" }}>
                                {place.tags && place.tags.map((tag, i) => (
                                    <span key={i} style={{
                                        background: "#f5f5f7",
                                        color: "#333",
                                        borderRadius: 6, padding: "4px 10px", fontSize: "0.78rem", fontWeight: 600,
                                        border: "1px solid #e4e4e7"
                                    }}>{`${tag.name}: ${tag.value}`}</span>
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