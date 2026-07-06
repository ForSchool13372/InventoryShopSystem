export const getTheme = (darkMode) => ({
    isLight: !darkMode,   // <— THIS FIXES EVERYTHING

    // main background
    background: darkMode ? "#0b0f19" : "#f8fafc",

    // cards
    cardBg: darkMode ? "#0f172a" : "#ffffff",

    // main text
    text: darkMode ? "#e5e7eb" : "#1a1a1a",

    // secondary text
    subText: darkMode ? "#94a3b8" : "#4a4a4a"
});
