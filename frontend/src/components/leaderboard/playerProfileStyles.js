export const getPlayerProfileStyles = (theme) => ({

    overlay: {
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.75)",
        backdropFilter: "blur(8px)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000
    },


    modal: {
        width: "420px",
        padding: "28px",
        borderRadius: "24px",
        background: theme.cardBg,
        color: theme.text,
        boxShadow: "0 30px 90px rgba(0,0,0,0.55)",
        border: "1px solid rgba(255,255,255,0.12)"
    },


    title: {
        textAlign: "center",
        marginBottom: "24px"
    },


    subtitle: {
        margin: "8px 0 0",
        color: theme.subText,
        fontWeight: 700
    },


    section: {
        padding: "16px",
        borderRadius: "16px",
        background: theme.isLight
            ? "rgba(0,0,0,0.04)"
            : "rgba(255,255,255,0.05)",
        border: "1px solid rgba(255,255,255,0.08)",
        marginBottom: "14px"
    },


    statRow: {
        display: "flex",
        justifyContent: "space-between",
        marginBottom: "8px",
        fontWeight: 700
    },


    progressBackground: {
        height: "12px",
        borderRadius: "20px",
        background: "rgba(128,128,128,0.25)",
        overflow: "hidden"
    },


    xpBar: (percent) => ({
        width: `${percent}%`,
        height: "100%",
        background:
            "linear-gradient(90deg,#6366f1,#a855f7)",
        transition: "0.3s"
    }),


    hpBar: (percent) => ({
        width: `${percent}%`,
        height: "100%",
        background:
            "linear-gradient(90deg,#ef4444,#f97316)"
    }),


    closeButton: {
        width: "100%",
        padding: "13px",
        borderRadius: "14px",
        border: "none",
        cursor: "pointer",
        background:
            "linear-gradient(135deg,#6366f1,#8b5cf6)",
        color: "white",
        fontWeight: 900,
        fontSize: "1rem",
        boxShadow:
            "0 8px 25px rgba(99,102,241,0.35)"
    }

});