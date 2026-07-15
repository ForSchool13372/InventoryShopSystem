export const getShopItemCardStyles = (theme, item, rarityGlow) => ({
    card: {
        padding: "10px",
        borderRadius: "14px",

        background: `
        linear-gradient(
            145deg,
            rgba(255,255,255,0.06),
            ${theme.cardBg}
        )
    `,

        border: `1px solid ${rarityGlow}`,

        boxShadow: `
        0 0 15px ${rarityGlow},
        0 10px 30px rgba(0,0,0,0.3),
        inset 0 1px rgba(255,255,255,0.08)
    `,

        cursor: item.stock === 0 ? "not-allowed" : "pointer",

        opacity: item.stock === 0 ? 0.45 : 1,

        display: "flex",
        flexDirection: "column",
        gap: "8px",

        position: "relative",

        // IMPORTANT: lets glow escape
        overflow: "visible",

        zIndex: 1,

        transition: "all 0.2s ease"
    },

    hover: {
        y: -4,

        zIndex: 10,

        boxShadow: `
        0 0 0 2px ${rarityGlow},
        0 0 35px ${rarityGlow},
        0 20px 45px rgba(0,0,0,0.45)
    `
    },

    header: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "flex-start",
        gap: "8px"
    },

    titleContainer: {
        display: "flex",
        flexDirection: "column",
        gap: "3px"
    },

    title: {
        fontWeight: 950,
        color: theme.text,
        fontSize: "0.95rem",
        letterSpacing: "0.4px"
    },

    description: {
        fontSize: "0.7rem",
        color: theme.subText,

        lineHeight: "1.35",

        display: "-webkit-box",
        WebkitLineClamp: 2,
        WebkitBoxOrient: "vertical",
        overflow: "hidden"
    },

    price: {
        fontWeight: 950,
        fontSize: "0.75rem",

        color: "#fbbf24",

        background: "rgba(251,191,36,0.12)",

        padding: "4px 10px",

        borderRadius: "999px",

        whiteSpace: "nowrap",

        border: "1px solid rgba(251,191,36,0.3)",

        boxShadow:
            "0 0 12px rgba(251,191,36,0.2)"
    },

    bottomBar: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",

        fontSize: "0.65rem",

        flexWrap: "wrap",

        gap: "6px"
    },

    badges: {
        display: "flex",
        gap: "5px",
        flexWrap: "wrap"
    },

    typeBadge: {
        padding: "3px 7px",

        borderRadius: "999px",

        background: "rgba(99,102,241,0.15)",

        color: "#a5b4fc",

        border: "1px solid rgba(99,102,241,0.25)",

        fontWeight: 800,

        fontSize: "0.65rem"
    },

    rarityBadge: {
        padding: "3px 7px",

        borderRadius: "999px",

        background: rarityGlow,

        color:
            item.rarity === "common"
                ? "#22c55e"
                : item.rarity === "trash"
                    ? "#9ca3af"
                    : item.rarity === "rare"
                        ? "#60a5fa"
                        : item.rarity === "epic"
                            ? "#c084fc"
                            : "#fbbf24",

        border: "1px solid rgba(255,255,255,0.12)",

        fontWeight: 900,

        fontSize: "0.65rem"
    },

    stockBadge: {
        padding: "3px 7px",

        borderRadius: "999px",

        background: "rgba(148,163,184,0.12)",

        color: theme.subText,

        border: "1px solid rgba(148,163,184,0.18)",

        fontSize: "0.65rem"
    },

    availability: {
        padding: "3px 7px",

        borderRadius: "999px",

        background: item.stock > 0
            ? "rgba(34,197,94,0.14)"
            : "rgba(239,68,68,0.14)",

        color: item.stock > 0
            ? "#22c55e"
            : "#ef4444",

        border: item.stock > 0
            ? "1px solid rgba(34,197,94,0.25)"
            : "1px solid rgba(239,68,68,0.25)",

        fontWeight: 900,

        fontSize: "0.65rem"
    }
});