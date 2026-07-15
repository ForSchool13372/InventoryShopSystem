export const getCardStyle = (theme) => ({
    background: theme.cardBg,
    color: theme.text,
    padding: "20px",
    borderRadius: "18px",
    border: "1px solid rgba(170,59,255,0.35)",
    boxShadow: `
        0 12px 35px rgba(0,0,0,0.25),
        0 0 35px rgba(170,59,255,0.28)
    `,
    display: "flex",
    gap: "16px"
});

export const buttonBase = {
    padding: "6px 10px",
    borderRadius: "10px",
    border: "none",
    fontWeight: "600",
    cursor: "pointer",
    minWidth: "34px",
    textAlign: "center",
    transition: "transform 0.15s ease, background 0.2s ease"
};