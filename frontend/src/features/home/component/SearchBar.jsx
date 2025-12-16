import React, { useState, useEffect, useCallback } from "react";

export default function SearchBar({ places, locale, onSearchChange, tags, selectedTagIds, onTagsChange }) {
    const [search, setSearch] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [selectedIndex, setSelectedIndex] = useState(-1);
    const [showFilterMenu, setShowFilterMenu] = useState(false);

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
        setShowFilterMenu(!showFilterMenu);
    };

    const toggleTag = (id) => {
        const newSelectedTagIds = selectedTagIds.includes(id)
            ? selectedTagIds.filter(t => t !== id)
            : [...selectedTagIds, id];
        onTagsChange(newSelectedTagIds);
    };

    const clearTags = () => {
        onTagsChange([]);
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
                    className="w-full px-6 py-3 rounded-lg border-none bg-white text-gray-800 text-base shadow-[0_2px_4px_rgba(0,0,0,0.1)] focus:outline-none focus:ring-2 focus:ring-opacity-50"
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
                style={{ backgroundColor: locale.color }}>
                Filters ▾
            </button>
            {showFilterMenu && (
                <div className="absolute right-0 mt-2 bg-white rounded-xl shadow-[0_10px_30px_rgba(0,0,0,0.15)] p-4 min-w-[260px] z-20">
                    <div className="font-bold mb-2 text-gray-800">Tags</div>
                    <div className="flex flex-wrap gap-2 max-h-[200px] overflow-y-auto">
                        {tags.map(tag => {
                            const isOn = selectedTagIds.includes(tag.id);
                            return (
                                <button
                                    key={tag.id}
                                    onClick={() => toggleTag(tag.id)}
                                    className={`border rounded-full px-3 py-1.5 text-sm cursor-pointer transition-all duration-200 ${
                                        isOn ? 'border-transparent text-white' : 'border-gray-300 bg-[#f7f7f8] text-[#444]'
                                    }`}
                                    style={isOn ? { backgroundColor: locale.color } : {}}
                                >
                                    {tag.name}
                                </button>
                            );
                        })}
                    </div>
                    <div className="flex justify-between mt-3">
                        <button 
                            onClick={clearTags}
                            className="bg-gray-100 border border-gray-300 text-gray-700 rounded-lg px-3.5 py-2 cursor-pointer hover:bg-gray-200">
                            Clear
                        </button>
                        <button 
                            onClick={() => setShowFilterMenu(false)}
                            className="border-none text-white rounded-lg px-3.5 py-2 cursor-pointer font-semibold"
                            style={{ backgroundColor: locale.color }}>
                            Done
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}