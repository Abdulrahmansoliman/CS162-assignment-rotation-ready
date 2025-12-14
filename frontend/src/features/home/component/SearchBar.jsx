import React, { useState, useEffect, useCallback } from "react";

export default function SearchBar({ places, locale, onSearchChange }) {
    const [search, setSearch] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [selectedIndex, setSelectedIndex] = useState(-1);

    const [debouncedSearch, setDebouncedSearch] = useState("");
    useEffect(() => {
        const timer = setTimeout(() => setDebouncedSearch(search), 200);
        return () => clearTimeout(timer);
    }, [search]);

    const getFilteredSuggestions = useCallback((query) => {
        if (!query.trim()) return [];
        const filtered = places.filter(place =>
            place.name.toLowerCase().includes(query.toLowerCase())
        );
        return [...new Set(filtered.map(place => place.name))].slice(0, 5);
    }, [places]);

    useEffect(() => {
        const newSuggestions = getFilteredSuggestions(debouncedSearch);
        setSuggestions(newSuggestions);
        setShowSuggestions(debouncedSearch.trim() !== "");
        setSelectedIndex(-1);
        onSearchChange(debouncedSearch);
    }, [debouncedSearch, getFilteredSuggestions, onSearchChange]);

    const handleKeyDown = (e) => {
        if (!showSuggestions) {
            if (e.key === 'Enter') setShowSuggestions(false);
            return;
        }

        const actions = {
            ArrowDown: () => setSelectedIndex(prev => prev < suggestions.length - 1 ? prev + 1 : prev),
            ArrowUp: () => setSelectedIndex(prev => prev > 0 ? prev - 1 : -1),
            Tab: () => {
                const index = selectedIndex >= 0 ? selectedIndex : 0;
                setSearch(suggestions[index]);
                setShowSuggestions(false);
            },
            Enter: () => {
                if (selectedIndex >= 0) setSearch(suggestions[selectedIndex]);
                setShowSuggestions(false);
            },
            Escape: () => {
                setShowSuggestions(false);
                setSelectedIndex(-1);
            }
        };

        if (actions[e.key]) {
            e.preventDefault();
            actions[e.key]();
        }
    };

    const handleSuggestionClick = (suggestion) => {
        setSearch(suggestion);
        setShowSuggestions(false);
        setSelectedIndex(-1);
    };

    const handleFilterClick = () => {
        setShowSuggestions(false);
    };

    return (
        <div className="flex gap-4 mb-6 relative">
            <div className="flex-1 relative">
                <input
                    type="text"
                    placeholder="Search..."
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                    onKeyDown={handleKeyDown}
                    onFocus={() => setShowSuggestions(search.trim() !== "")}
                    className="w-full px-6 py-3 rounded-lg border-none bg-white text-gray-800 text-base shadow-sm focus:outline-none focus:ring-2 focus:ring-opacity-50"
                    style={{ boxShadow: "0 2px 4px rgba(0,0,0,0.1)" }}
                />
                {showSuggestions && (
                    <div className="absolute top-full left-0 right-0 bg-white rounded-lg shadow-lg mt-1 max-h-[300px] overflow-y-auto z-[1000]">
                        {suggestions.length > 0 ? (
                            suggestions.map((suggestion, index) => (
                                <div
                                    key={index}
                                    onClick={() => handleSuggestionClick(suggestion)}
                                    onMouseEnter={() => setSelectedIndex(index)}
                                    className={`py-3 px-6 cursor-pointer text-base text-gray-800 transition-colors duration-100 ${
                                        selectedIndex === index ? "bg-gray-100" : "bg-white hover:bg-gray-50"
                                    } ${
                                        index < suggestions.length - 1 ? "border-b border-gray-200" : ""
                                    }`}
                                >
                                    {suggestion}
                                </div>
                            ))
                        ) : (
                            <div className="py-3 px-6 text-base text-gray-800">
                                No results
                            </div>
                        )}
                    </div>
                )}
            </div>
            <button 
                onClick={handleFilterClick}
                className="text-white border-none rounded-lg px-6 py-2 text-base font-semibold cursor-pointer transition-colors duration-300 hover:opacity-90"
                style={{ background: locale.color }}>
                Filter
            </button>
        </div>
    );
}