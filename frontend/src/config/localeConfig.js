/**
 * Locale Configuration
 * 
 * Centralized configuration for rotation city theming.
 * Maps city names to visual themes (colors, backgrounds, welcome text).
 */

export const LOCALE_CONFIG = {
    'san francisco': {
        key: 'usa',
        color: '#cc0000',
        cssClass: 'show-photo',
        welcomeText: 'Welcome',
        backgroundImage: '/sf.jpg'
    },
    'taipei': {
        key: 'china',
        color: '#2fb872',
        cssClass: 'transition-green',
        welcomeText: '欢迎',
        backgroundImage: '/tp.jpg'
    },
    'seoul': {
        key: 'korea',
        color: '#e91e63',
        cssClass: 'transition-korea',
        welcomeText: '어서 오세요',
        backgroundImage: '/sl.jpg'
    },
    'buenos aires': {
        key: 'argentina',
        color: '#d9a300',
        cssClass: 'transition-argentina',
        welcomeText: 'Bienvenido',
        backgroundImage: '/ba.jpg'
    },
    'hyderabad': {
        key: 'india',
        color: '#ffcc33',
        cssClass: 'transition-india',
        welcomeText: 'స్వాగతం',
        backgroundImage: '/hyd.jpg'
    },
    'berlin': {
        key: 'germany',
        color: '#7bb3e8',
        cssClass: 'transition-germany',
        welcomeText: 'Willkommen',
        backgroundImage: '/br.jpg'
    }
};

// Default locale for fallback
export const DEFAULT_LOCALE = LOCALE_CONFIG['san francisco'];

/**
 * Get locale configuration from city name
 * @param {string} cityName - The city name from user's rotation_city
 * @returns {object} Locale configuration object
 */
export function getLocaleFromCity(cityName) {
    if (!cityName) return DEFAULT_LOCALE;
    const normalizedCity = cityName.toLowerCase().trim();
    return LOCALE_CONFIG[normalizedCity] || DEFAULT_LOCALE;
}

/**
 * Get user's full name from user object
 * @param {object} user - User object from API
 * @returns {string} Full name or fallback
 */
export function getUserDisplayName(user) {
    if (!user) return 'User';
    const fullName = `${user.first_name || ''} ${user.last_name || ''}`.trim();
    return fullName || user.email || 'User';
}
