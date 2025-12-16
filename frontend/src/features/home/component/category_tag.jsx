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
    const cardColor = palette[0];
    const cardColorSelected = palette[1] || palette[0];
    const textColor = getContrastColor(cardColor);
    const textColorSelected = getContrastColor(cardColorSelected);

    return (
        <div className="mb-8">
            <div className="relative">
                <div className="flex flex-wrap gap-2 pb-2">
                    {categories.map((cat) => {
                        const isSelected = selectedCategoryIds.includes(cat.id);
                        const tileColor = palette[idx % palette.length];
                        const selectedColor = tileColor; // keep same hue, emphasize via scale
                        return (
                            <button
                                key={cat.id}
                                onClick={() => onToggleCategory(cat.id)}
                                className={`
                                    relative rounded-full
                                    flex items-center gap-2
                                    cursor-pointer transition-all duration-150 ease-out
                                    group
                                    px-4 py-2
                                    ${ 
                                        isSelected 
                                            ? 'shadow-md scale-105' 
                                            : 'hover:scale-105 hover:shadow-sm opacity-90 hover:opacity-100'
                                    }
                                `}
                                style={{ 
                                    backgroundColor: isSelected ? cardColorSelected : cardColor,
                                    ringColor: isSelected ? 'rgba(255, 255, 255, 0.8)' : 'transparent'
                                }}
                                aria-label={`Toggle ${cat.name}`}
                                aria-pressed={isSelected}
                            >
                                {/* Selection indicator - small checkmark */}
                                {isSelected && (
                                    <div className="flex-shrink-0 w-4 h-4 bg-white rounded-full shadow-sm flex items-center justify-center">
                                        <svg 
                                            className="w-3 h-3 text-green-600" 
                                            fill="currentColor" 
                                            viewBox="0 0 20 20"
                                        >
                                            <path 
                                                fillRule="evenodd" 
                                                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" 
                                                clipRule="evenodd" 
                                            />
                                        </svg>
                                    </div>
                                )}

                                {/* Category icon */}
                                {cat.image && (
                                    <img 
                                        src={`data:image/png;base64,${cat.image}`}
                                        alt={cat.name}
                                        className="w-5 h-5 object-contain filter drop-shadow-sm flex-shrink-0"
                                    />
                                )}

                                {/* Category name */}
                                <span 
                                    className="text-sm font-semibold whitespace-nowrap"
                                    style={{ color: currentTextColor }}
                                >
                                    {cat.name}
                                </span>

                                {/* Hover effect overlay */}
                                <div className={`
                                    absolute inset-0 rounded-full bg-white opacity-0 
                                    transition-opacity duration-150
                                    ${!isSelected && 'group-hover:opacity-10'}
                                `} />
                            </button>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};
