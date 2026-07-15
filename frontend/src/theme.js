export const getTheme = (darkMode) => ({
    isLight: !darkMode,

    // Background colors
    background: darkMode ? "#050816" : "#f6f7fb",

    // Card surfaces
    cardBg: darkMode ? "#0b1224" : "#ffffff",

    // Primary text color
    text: darkMode ? "#f8fafc" : "#111827",

    // Secondary text color
    subText: darkMode ? "#94a3b8" : "#475569"
});