import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCurrentUser } from "../../api/user";
import { apiFetch } from "../../api";
import "@/shared/styles/locale-theme.css";
import SearchBar from "./component/SearchBar";




// Locale-based category palettes (from provided swatches)
const localeCategoryPalettes = {
    usa: ["#E31B23", "#9A2623", "#5C2A28", "#E53935", "#A63A3A"],
    china: ["#55B89C", "#5AD4A8", "#49C792", "#6AD9A7", "#7AE3B0"],
    korea: ["#FF7890", "#F3A1B6", "#E67A94", "#FF9AB0", "#F8B0C6"],
    argentina: ["#D9A300", "#F7A721", "#E5B74A", "#C8922E", "#B47F21"],
    india: ["#F7A721", "#E58B20", "#D0771D", "#C16A1B", "#A85A18"],
    germany: ["#005493", "#85A0CB", "#5688C0", "#1E5F90", "#0A3F66"],
};

const iconMap = [
    "🏠", "🏛️", "🍽️", "🛒", "☕", "📖", "💊", "🚚", "🔗"
];

function HomePage() {
    const [categories, setCategories] = useState([]);
    const [places, setPlaces] = useState([]);
    const [tags, setTags] = useState([]);
    const [search, setSearch] = useState("");
    const [filteredPlaces, setFilteredPlaces] = useState([]);
    const [view, setView] = useState("list");
    const [currentLocale, setCurrentLocale] = useState('usa');
    const [activeCategoryId, setActiveCategoryId] = useState(null);
    const [selectedTagIds, setSelectedTagIds] = useState([]);
    const navigate = useNavigate();

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
                const cityName = user.rotation_city?.name?.toLowerCase() || '';
                console.log("Extracted city name:", cityName);
                // Map based on city name to locale
                const localeMap = {
                    'san francisco': 'usa',
                    'taipei': 'china',
                    'seoul': 'korea',
                    'buenos aires': 'argentina',
                    'hyderabad': 'india',
                    'berlin': 'germany'
                };
                const selectedLocale = localeMap[cityName] || 'usa';
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

                // Fetch tags from backend
                const tagList = await apiFetch("/tag/", { method: "GET" });
                setTags(tagList.map(t => ({ id: t.tag_id, name: t.name || t.tag_name })));
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
        const selectedTagNames = selectedTagIds
            .map(id => (tags.find(t => t.id === id)?.name || "").toLowerCase())
            .filter(Boolean);
        const byTags = (p) => selectedTagNames.length === 0 || selectedTagNames.some(tag => (p.tags || []).map(t => t.toLowerCase()).includes(tag));
        setFilteredPlaces(places.filter(p => bySearch(p) && byCategory(p) && byTags(p)));
    }, [search, places, activeCategoryId, selectedTagIds, tags]);

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
            china: '#1d9a5c',
            korea: '#c60c30',
            argentina: '#d9a300',
            india: '#ff9933',
            germany: '#4a90e2'
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
            <div className={`locale-container ${getLocaleClass()}`} style={{ color: "white", padding: "3rem 2rem 2rem 2rem" }}>
                <div className={`locale-overlay absolute inset-0 ${getLocaleClass()}`}></div>
                <h1 style={{ fontSize: "2.5rem", margin: 0, fontWeight: 300, letterSpacing: "1px", position: "relative", zIndex: 10, fontFamily: 'Fraunces, serif' }}>{getLocaleText()}, {userName}</h1>
            </div>
            <div style={{ padding: "2rem", maxWidth: "1200px", margin: "0 auto" }}>
                <SearchBar 
                    places={places}
                    locale={{ color: getLocaleColor() }}
                    onSearchChange={setSearch}
                    tags={tags}
                    selectedTagIds={selectedTagIds}
                    onTagsChange={setSelectedTagIds}
                />
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
                            <button 
                                onClick={() => navigate(`/item/${place.id}`)}
                                style={{
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