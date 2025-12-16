import React from "react";

export default function CategoryTag({ categories, selectedCategoryIds, onToggleCategory, currentLocale }) {
    const localeCategoryPalettes = {
        usa: ["#002856", "#A50404", "#B8500C", "#F6DBAF", "#F6DBAF"],        
        china: ["#2c6e49", "#4c956c", "#ffc9b9", "#d68c45"],
        korea: ["#f9dbbd", "#ffa5ab", "#da627d", "#a53860", "#450920"],
        // Buenos Aires requested palette (multi-tile): 264653, 2a9d8f, e9c46a, f4a261, e76f51
        argentina: ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"],
        india: ["#cc5803", "#e2711d", "#ff9505", "#ffb627", "#ffc971"],
        germany: ["#003459", "#007ea7", "#00a8e8"],
    };

    const palette = localeCategoryPalettes[currentLocale] || localeCategoryPalettes['usa'];

    return (
        <div className="mb-8">
            <div className="relative">
                <div className="flex flex-wrap gap-4 pb-2">
                    {categories.map((cat, idx) => {
                        const isSelected = selectedCategoryIds.includes(cat.id);
                        const tileColor = palette[idx % palette.length];
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
