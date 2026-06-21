export const getCardStyle = (theme) => ({
    background: theme.cardBg,
    color: theme.text,
    padding: "20px",
    borderRadius: "18px",
    boxShadow: "0 12px 35px rgba(0,0,0,0.08)",
    border: "1px solid rgba(0,0,0,0.05)",
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