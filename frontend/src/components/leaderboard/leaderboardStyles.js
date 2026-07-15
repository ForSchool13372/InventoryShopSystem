export const getRankGlow = (index) => {
    if (index === 0) return "0 0 25px rgba(234,179,8,0.35)";
    if (index === 1) return "0 0 20px rgba(100,116,139,0.45)";
    if (index === 2) return "0 0 20px rgba(180,83,9,0.25)";
    return "none";
};


export const getLeaderboardStyles = (theme, currentPlayerId) => ({
    cardStyle: {
        background: theme.cardBg,
        color: theme.text,
        padding: "20px",
        borderRadius: "18px",
        marginTop: "20px",
        border: "1px solid rgba(170,59,255,0.35)",
        boxShadow: `
        0 12px 35px rgba(0,0,0,0.25),
        0 0 35px rgba(170,59,255,0.28)
    `
    },


    titleStyle: {
        fontSize: "1.5rem",
        fontWeight: "900",
        marginBottom: "18px",
        color: theme.text
    },


    titleContainerStyle: {
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between"
    },


    infoButtonStyle: {
        cursor: "pointer",
        border: "1px solid rgba(129,140,248,0.4)",
        background:
            "linear-gradient(180deg, rgba(79,70,229,0.35), rgba(30,27,75,0.6))",
        color: "#e0e7ff",
        borderRadius: "8px",
        padding: "5px 12px",
        fontSize: "14px",
        fontWeight: "700",
        display: "flex",
        alignItems: "center",
        gap: "6px",
        boxShadow: "0 0 15px rgba(79,70,229,0.35)",
        transition: "0.2s ease"
    },


    podiumContainerStyle: {
        display: "flex",
        gap: "12px",
        marginBottom: "20px"
    },


    podiumIconStyle: {
        fontSize: "2rem"
    },


    podiumStyle: (index) => ({
        flex: 1,
        padding: "18px",
        borderRadius: "16px",
        textAlign: "center",
        background:
            index === 0
                ? "rgba(234,179,8,0.12)"
                : index === 1
                    ? "rgba(148,163,184,0.12)"
                    : "rgba(180,83,9,0.12)",
        boxShadow: getRankGlow(index),
        border: "1px solid rgba(255,255,255,0.08)"
    }),


    rowStyle: (player) => ({
        padding: "14px",
        marginTop: "10px",
        borderRadius: "14px",
        background:
            player.playerId === currentPlayerId
                ? "rgba(99,102,241,0.15)"
                : "rgba(255,255,255,0.03)",
        border:
            player.playerId === currentPlayerId
                ? "1px solid rgba(99,102,241,0.5)"
                : "1px solid rgba(255,255,255,0.05)",
        transition: "0.2s ease"
    })
});