export const getShopCartStyles = (theme) => ({
    container: {
        flex: "0 0 320px",
        padding: "18px",
        borderRadius: "18px",

        background: `
            linear-gradient(
                145deg,
                rgba(168,85,247,0.12),
                ${theme.cardBg}
            )
        `,

        border: "1px solid rgba(168,85,247,0.35)",

        height: "fit-content",
        position: "sticky",
        top: "20px",

        display: "flex",
        flexDirection: "column",
        gap: "14px",

        boxShadow: `
            0 0 35px rgba(168,85,247,0.18),
            0 20px 50px rgba(0,0,0,0.45),
            inset 0 1px rgba(255,255,255,0.08)
        `
    },

    header: {
        fontWeight: 1000,
        color: theme.text,
        fontSize: "1.25rem",
        margin: 0,
        letterSpacing: "0.5px"
    },

    empty: {
        color: theme.subText,
        margin: 0,
        opacity: 0.8
    },

    item: {
        padding: "14px",
        borderRadius: "14px",

        background: "rgba(255,255,255,0.03)",

        border: "1px solid rgba(255,255,255,0.08)",

        display: "flex",
        flexDirection: "column",
        gap: "10px",

        boxShadow: `
            0 8px 25px rgba(0,0,0,0.25)
        `
    },

    itemHeader: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        gap: "10px"
    },

    itemName: {
        fontWeight: 950,
        color: theme.text,
        fontSize: "1rem"
    },

    totalBadge: {
        fontSize: "0.8rem",
        fontWeight: 950,

        color: "#fbbf24",

        background: "rgba(251,191,36,0.12)",

        padding: "5px 12px",
        borderRadius: "999px",

        whiteSpace: "nowrap",

        border: "1px solid rgba(251,191,36,0.35)",

        boxShadow: `
            0 0 15px rgba(251,191,36,0.25)
        `
    },

    badges: {
        display: "flex",
        gap: "6px",
        flexWrap: "wrap"
    },

    unitBadge: {
        padding: "4px 9px",
        borderRadius: "999px",

        background: "rgba(251,191,36,0.12)",
        color: "#fbbf24",

        fontWeight: 800,
        fontSize: "0.7rem",

        border: "1px solid rgba(251,191,36,0.25)"
    },

    qtyBadge: {
        padding: "4px 9px",
        borderRadius: "999px",

        background: "rgba(99,102,241,0.15)",
        color: "#a5b4fc",

        fontWeight: 800,
        fontSize: "0.7rem",

        border: "1px solid rgba(99,102,241,0.25)"
    },

    stockBadge: {
        padding: "4px 9px",
        borderRadius: "999px",

        background: "rgba(148,163,184,0.12)",
        color: theme.subText,

        fontSize: "0.7rem",

        border: "1px solid rgba(148,163,184,0.18)"
    },

    controls: {
        display: "flex",
        alignItems: "center",
        gap: "8px",
        flexWrap: "wrap"
    },

    quantity: {
        fontWeight: 950,
        minWidth: "30px",
        color: theme.text,
        fontSize: "1rem"
    },

    divider: {
        height: "1px",
        background: "rgba(255,255,255,0.08)",
        margin: "8px 0"
    },

    summary: {
        padding: "14px",
        borderRadius: "14px",

        background: "rgba(99,102,241,0.08)",

        border: "1px solid rgba(99,102,241,0.25)",

        display: "flex",
        flexDirection: "column",
        gap: "8px"
    },

    summaryRow: {
        display: "flex",
        justifyContent: "space-between",

        fontWeight: 950,
        color: theme.text
    },

    affordability: (canAfford) => ({
        color: canAfford ? "#22c55e" : "#ef4444",

        fontWeight: 900,

        fontSize: "0.85rem"
    }),

    buyButton: (canAfford) => ({
        width: "100%",

        background: canAfford
            ? "linear-gradient(135deg,#8b5cf6,#4f46e5)"
            : "#ef4444",

        color: "white",

        fontWeight: 1000,

        borderRadius: "12px",

        boxShadow: canAfford
            ? "0 0 25px rgba(139,92,246,0.45)"
            : "none"
    })
});