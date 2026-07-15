export const styles = {
    card: (t) => ({
        padding: "16px",
        borderRadius: "12px",
        border: "1px solid rgba(170,59,255,0.35)",
        background: t.cardBg,
        color: t.text,
        display: "flex",
        flexDirection: "column",
        gap: "14px",
        boxShadow: `
        0 12px 35px rgba(0,0,0,0.25),
        0 0 35px rgba(170,59,255,0.28)
    `
    }),

    title: (t) => ({
        fontWeight: 900,
        fontSize: "1rem",
        letterSpacing: "1px",
        color: t.text
    }),

    lockedMessage: {
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        minHeight: "220px",
        fontWeight: 900,
        fontSize: "1rem",
        lineHeight: "1.5"
    },

    actions: {
        display: "flex",
        gap: "8px",
        marginTop: "4px"
    },

    button: {
        flex: 1,
        padding: "10px 14px",
        borderRadius: "10px",
        border: "1px solid rgba(99,102,241,0.35)",
        cursor: "pointer",
        background: "linear-gradient(135deg, #6366f1, #4f46e5)",
        color: "white",
        fontWeight: 800,
        fontSize: "0.82rem",
        letterSpacing: "0.4px",
        boxShadow: "0 0 18px rgba(99,102,241,0.25)",
        transition: "all 0.2s ease"
    },

    claimButton: {
        padding: "6px 10px",
        borderRadius: "6px",
        border: "none",
        cursor: "pointer",
        background: "#22c55e",
        color: "black",
        fontWeight: 800,
        fontSize: "0.75rem"
    },

    list: {
        marginTop: "6px",
        fontSize: "0.85rem",
        display: "flex",
        flexDirection: "column",
        gap: "12px",
        maxHeight: "40vh",
        overflowY: "auto",
        paddingRight: "4px"
    },

    questCard: (t) => ({
        padding: "16px",
        borderRadius: "10px",
        border: `1px solid ${t.subText}33`,
        background: "rgba(255,255,255,0.06)",
        display: "flex",
        flexDirection: "column",
        gap: "10px"
    }),

    questName: {
        fontWeight: 900,
        fontSize: "0.95rem",
        marginBottom: "4px"
    },

    sectionTitle: (t) => ({
        marginTop: "4px",
        fontWeight: 700,
        fontSize: "0.75rem",
        opacity: 0.8,
        borderBottom: `1px solid ${t.subText}33`,
        paddingBottom: "2px"
    }),

    row: {
        display: "flex",
        justifyContent: "space-between",
        fontSize: "0.8rem",
        opacity: 0.95
    }
};