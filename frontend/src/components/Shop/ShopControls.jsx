function ShopControls({
    searchQuery,
    setSearchQuery,
    theme
}) {
    return (
        <div style={{ marginBottom: "14px" }}>
            <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search items..."
                style={{
                    width: "90%",
                    padding: "10px 12px",
                    borderRadius: "10px",
                    border: `1px solid ${theme.subText}55`,
                    background: theme.cardBg,
                    color: theme.text,
                    outline: "none"
                }}
            />
        </div>
    );
}

export default ShopControls;