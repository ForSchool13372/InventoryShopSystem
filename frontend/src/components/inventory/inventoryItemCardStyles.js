export const getInventoryItemCardStyles = (
    theme,
    item,
    isSelected,
    isLoading,
    rarity
) => ({
    card: {
        display: "flex",
        justifyContent: "space-between",
        gap: "12px",
        padding: "14px",
        borderRadius: "14px",
        cursor: "pointer",
        position: "relative",

        background: isSelected
            ? "linear-gradient(135deg, rgba(168,85,247,0.18), rgba(34,197,94,0.10))"
            : theme.cardBg,

        border: isSelected
            ? "2px solid rgba(168,85,247,0.75)"
            : `1px solid ${rarity.color}55`,

        boxShadow: isSelected
            ? `
        0 0 0 3px rgba(168,85,247,0.25),
        0 0 30px rgba(168,85,247,0.65),
        0 0 55px rgba(34,197,94,0.25),
        0 15px 40px rgba(0,0,0,0.45)
        `
            : `
        0 0 12px ${rarity.glow},
        0 10px 25px rgba(0,0,0,0.25)
        `,

        transform: isSelected
            ? "scale(1.015)"
            : "scale(1)",

        transition: "all 0.2s ease",

        opacity: isLoading ? 0.6 : 1
    },

    hover: {
        boxShadow: `
            0 0 0 2px ${rarity.color}55,
            0 0 25px ${rarity.glow},
            0 15px 35px rgba(0,0,0,0.45)
        `
    },

    leftSection: {
        display: "flex",
        gap: "10px",
        alignItems: "flex-start"
    },

    content: {
        display: "flex",
        flexDirection: "column",
        gap: "6px",
        justifyContent: "flex-start"
    },

    name: {
        fontWeight: 900,
        fontSize: "0.95rem",
        color: theme.text,
        lineHeight: "1.1"
    },

    description: {
        fontSize: "0.72rem",
        color: theme.subText,
        opacity: 0.9,
        lineHeight: "1.35",
        maxWidth: "320px",

        display: "-webkit-box",
        WebkitLineClamp: 2,
        WebkitBoxOrient: "vertical",
        overflow: "hidden",
        wordBreak: "break-word"
    },

    tags: {
        display: "flex",
        gap: "6px",
        flexWrap: "wrap",
        alignItems: "center"
    },

    typeBadge: {
        fontSize: "0.65rem",
        padding: "3px 8px",
        borderRadius: "999px",
        background: "rgba(99,102,241,0.15)",
        color: "#a5b4fc",
        border: "1px solid rgba(99,102,241,0.25)"
    },

    rarityBadge: {
        fontSize: "0.65rem",
        padding: "3px 8px",
        borderRadius: "999px",
        background: rarity.glow,
        color: rarity.color,
        border: "1px solid rgba(255,255,255,0.08)",
        fontWeight: 700,
        letterSpacing: "0.4px"
    },

    rightSection: {
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-end",
        justifyContent: "space-between",
        width: "140px",
        flexShrink: 0
    },

    quantity: {
        fontWeight: 900,
        fontSize: "0.75rem",
        color: "#fbbf24"
    },

    price: {
        textAlign: "right",
        fontSize: "0.75rem",
        fontWeight: 800,
        color: "#22c55e"
    },

    total: {
        opacity: 0.75,
        fontWeight: 600
    },

    buttons: {
        display: "flex",
        gap: "6px"
    },

    sellButton: {
        padding: "5px 10px",
        borderRadius: "7px",
        border: "1px solid rgba(34,197,94,0.25)",
        fontSize: "0.65rem",
        background: "rgba(34,197,94,0.10)",
        color: "#22c55e",
        fontWeight: 700,
        cursor: "pointer",
        opacity: isLoading ? 0.5 : 1
    },

    sellAllButton: {
        padding: "5px 10px",
        borderRadius: "7px",
        border: "1px solid rgba(34,197,94,0.35)",
        fontSize: "0.65rem",
        background: "rgba(34,197,94,0.14)",
        color: "#22c55e",
        fontWeight: 800,
        cursor: "pointer",
        opacity: isLoading ? 0.5 : 1
    }
});