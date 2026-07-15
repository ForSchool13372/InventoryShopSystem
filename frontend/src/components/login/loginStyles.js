export const getLoginStyles = (theme) => ({
    card: {
        background: theme.cardBg,
        color: theme.text,
        padding: "22px",
        borderRadius: "16px",
        border: "1px solid rgba(170,59,255,0.35)",
        boxShadow: `
        0 12px 35px rgba(0,0,0,0.25),
        0 0 35px rgba(170,59,255,0.28)
    `
    },

    title: {
        marginBottom: "12px",
        color: theme.text,
        fontWeight: "800",
        fontSize: "1.4rem",
        letterSpacing: "-0.02em"
    },

    formRow: {
        display: "flex",
        gap: "10px",
        flexWrap: "wrap"
    },

    loggedInRow: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center"
    },

    loggedInStatus: {
        display: "flex",
        alignItems: "center",
        gap: "8px",
        fontWeight: "600",
        color: "#22c55e"
    },

    statusDot: {
        width: "8px",
        height: "8px",
        borderRadius: "50%",
        background: "#22c55e",
        display: "inline-block",
        boxShadow: "0 0 10px #22c55e"
    },

    input: {
        flex: 1,
        padding: "11px 12px",
        borderRadius: "10px",
        border: `1px solid ${theme.subText}55`,
        outline: "none",
        background: theme.cardBg,
        color: theme.text,
        transition: "0.2s ease"
    },

    button: (active, color) => ({
        padding: "10px 14px",
        borderRadius: "10px",
        border: "none",
        fontWeight: "600",
        cursor: active ? "pointer" : "not-allowed",
        background: active ? color : "#9ca3af",
        color: "white",
        transition: "all 0.2s ease",
        transform: "translateY(0px)",
        boxShadow: active
            ? `0 0 15px ${color}66`
            : "none"
    }),

    error: {
        marginTop: "12px",
        padding: "10px",
        borderRadius: "10px",
        background: "rgba(239,68,68,0.08)",
        color: "#ef4444",
        fontWeight: "500",
        animation: "fadeIn 0.2s ease"
    }
});