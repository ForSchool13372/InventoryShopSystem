export const playerStatsStyles = {
    card: (t) => ({
        background: t.cardBg,
        border: "1px solid rgba(170,59,255,0.35)",
        borderRadius: "12px",
        padding: "14px",
        color: t.text,
        display: "flex",
        flexDirection: "column",
        gap: "12px",
        boxShadow: `
        0 12px 35px rgba(0,0,0,0.25),
        0 0 35px rgba(170,59,255,0.28)
    `
    }),

    title: (t) => ({
        fontWeight: 800,
        fontSize: "1.2rem",
        color: t.text
    }),

    section: (t) => ({
        padding: "12px",
        borderRadius: "12px",
        border: `1px solid ${t.subText}22`,
        background: t.cardBg
    }),

    sectionLabel: (t) => ({
        fontSize: "0.7rem",
        fontWeight: 800,
        letterSpacing: "2px",
        marginBottom: "10px",
        color: t.subText
    }),

    statList: () => ({
        display: "flex",
        flexDirection: "column",
        gap: "6px"
    }),

    diabloRow: (t) => ({
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "8px 10px",
        background: "rgba(0,0,0,0.15)",
        border: `1px solid ${t.subText}22`,
        borderRadius: "6px"
    }),

    leftLabel: (t) => ({
        color: t.subText,
        fontWeight: 700,
        fontSize: "0.7rem",
        letterSpacing: "1px",
        textTransform: "uppercase"
    }),

    rightValue: (t) => ({
        color: t.text,
        fontWeight: 900
    }),

    goldPill: (t) => ({
        fontWeight: 800,
        fontSize: "0.85rem",
        color: "#fbbf24",

        background: t.isLight
            ? "rgba(251,191,36,0.20)"   // darker + richer gold tint
            : "rgba(251,191,36,0.08)",

        padding: "4px 10px",
        borderRadius: "999px",

        border: t.isLight
            ? "1px solid rgba(251,191,36,0.45)"   // stronger outline
            : "1px solid rgba(251,191,36,0.15)",

        boxShadow: t.isLight
            ? "0 2px 4px rgba(0,0,0,0.12)"        // subtle dark shadow for depth
            : "none"
    })
};
