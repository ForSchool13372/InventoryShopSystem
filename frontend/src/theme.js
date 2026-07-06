export const getTheme = (darkMode) => ({
    isLight: !darkMode,

    // Background colors
    background: darkMode ? "#0b0f19" : "#f8fafc",

    // Card surfaces
    cardBg: darkMode ? "#0f172a" : "#ffffff",

    // Primary text color
    text: darkMode ? "#e5e7eb" : "#1a1a1a",

    // Secondary text color
    subText: darkMode ? "#94a3b8" : "#4a4a4a"
});