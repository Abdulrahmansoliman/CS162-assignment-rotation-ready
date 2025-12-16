import React from "react";

export default function CategoryTag({ categories, selectedCategoryIds, onToggleCategory, currentLocale }) {
    const localeCategoryPalettes = {
        usa: ["#E31B23", "#B71C1C"],        
        china: ["#55B89C", "#21806A"],
        korea: ["#FF7890", "#C2185B"],
        // Buenos Aires requested palette (multi-tile): 264653, 2a9d8f, e9c46a, f4a261, e76f51
        argentina: ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"],
        india: ["#F7A721", "#B8860B"],
        germany: ["#85A0CB", "#5688C0"],
    };

    const palette = localeCategoryPalettes[currentLocale] || localeCategoryPalettes['usa'];

    return (
        <div className="mb-8">
            <div className="relative">
                <div className="flex flex-wrap gap-4 pb-2">
                    {categories.map((cat, idx) => {
                        const isSelected = selectedCategoryIds.includes(cat.id);
                        const tileColor = palette[(currentLocale === 'argentina' ? idx : 0) % palette.length];
                        const selectedColor = tileColor; // keep same hue, emphasize via scale
                        return (
                            <button
                                key={cat.id}
                                onClick={() => onToggleCategory(cat.id)}
                                className={`group w-[72px] h-[72px] rounded-2xl flex flex-col items-center justify-center shadow-[0_4px_12px_rgba(0,0,0,0.08)] transition-transform duration-150 ${isSelected ? 'scale-105' : 'hover:scale-105'}`}
                                style={{ backgroundColor: isSelected ? selectedColor : tileColor }}
                                aria-label={`Toggle ${cat.name}`}
                                aria-pressed={isSelected}
                            >
                                {cat.image && (
                                    <img 
                                        src={`data:image/png;base64,${cat.image}`}
                                        alt={cat.name}
                                        className="w-10 h-10 object-contain drop-shadow-sm"
                                    />
                                )}
                            </button>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};
