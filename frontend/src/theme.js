export const getTheme = (darkMode) => ({
    // main background (slightly cooler + cleaner white space)
    background: darkMode ? "#0b0f19" : "#f8fafc",

    // cards (adds subtle separation from background)
    cardBg: darkMode ? "#0f172a" : "#ffffff",

    // main text (slightly softened for less harsh black)
    text: darkMode ? "#e5e7eb" : "#0f172a",

    // secondary text (more modern muted tone)
    subText: darkMode ? "#94a3b8" : "#64748b"
});