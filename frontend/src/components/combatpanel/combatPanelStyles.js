export const getCombatPanelStyles = (theme) => ({
    card: {
        padding: "18px",
        borderRadius: "16px",
        border: "1px solid rgba(170,59,255,0.35)",
        background: `linear-gradient(145deg, ${theme.cardBg}, rgba(0,0,0,0.25))`,
        color: theme.text,
        display: "flex",
        flexDirection: "column",
        gap: "14px",
        boxShadow: `
        0 12px 35px rgba(0,0,0,0.25),
        0 0 35px rgba(170,59,255,0.28),
        inset 0 1px 0 rgba(255,255,255,0.05)
    `
    },

    title: {
        fontWeight: 950,
        fontSize: "1.05rem",
        letterSpacing: "2px",
        color: theme.text,
        textTransform: "uppercase",
        textShadow: "0 2px 10px rgba(255,255,255,0.15)"
    },

    enemyBox: {
        padding: "14px",
        borderRadius: "12px",
        background: "linear-gradient(145deg, rgba(180,0,0,0.15), rgba(0,0,0,0.35))",
        border: "1px solid rgba(239,68,68,0.35)",
        boxShadow: `
            inset 0 0 15px rgba(239,68,68,0.15),
            0 4px 15px rgba(0,0,0,0.3)
        `,
        fontWeight: 800
    },

    actions: {
        display: "flex",
        gap: "10px",
        marginTop: "8px"
    },

    button: {
        flex: 1,
        padding: "12px",
        borderRadius: "10px",
        border: "1px solid rgba(255,255,255,0.15)",
        cursor: "pointer",
        background: "linear-gradient(145deg, #6366f1, #4338ca)",
        color: "white",
        fontWeight: 900,
        letterSpacing: "0.5px",
        boxShadow: `
            0 6px 18px rgba(0,0,0,0.35),
            inset 0 1px 0 rgba(255,255,255,0.2)
        `
    },

    log: {
        marginTop: "8px",
        fontSize: "0.8rem",
        opacity: 0.95,
        padding: "14px",
        borderRadius: "12px",
        border: "1px solid rgba(255,255,255,0.12)",
        background: "rgba(0,0,0,0.35)",
        display: "flex",
        flexDirection: "column",
        gap: "8px",
        maxHeight: "240px",
        overflowY: "auto",
        boxShadow: "inset 0 0 20px rgba(0,0,0,0.4)"
    },

    loot: {
        marginTop: "10px",
        padding: "14px",
        borderRadius: "12px",
        background: "linear-gradient(145deg, rgba(34,197,94,0.15), rgba(0,0,0,0.3))",
        border: "1px solid rgba(34,197,94,0.35)",
        boxShadow: `
            inset 0 0 20px rgba(34,197,94,0.1),
            0 6px 20px rgba(0,0,0,0.3)
        `
    }
});