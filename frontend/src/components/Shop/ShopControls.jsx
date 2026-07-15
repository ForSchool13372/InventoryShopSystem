function ShopControls({
    searchQuery,
    setSearchQuery,
    theme
}) {
    return (
        <div style={{ marginBottom: "18px" }}>
            <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="🔎 Search items..."
                style={{
                    width: "90%",

                    padding: "12px 16px",

                    borderRadius: "14px",

                    border: "1px solid rgba(168,85,247,0.35)",

                    background: `
                        linear-gradient(
                            145deg,
                            rgba(168,85,247,0.08),
                            ${theme.cardBg}
                        )
                    `,

                    color: theme.text,

                    outline: "none",

                    fontSize: "0.9rem",

                    fontWeight: 700,

                    boxShadow: `
                        inset 0 1px rgba(255,255,255,0.08),
                        0 8px 25px rgba(0,0,0,0.25)
                    `,

                    transition: "all 0.2s ease"
                }}
            />
        </div>
    );
}

export default ShopControls;