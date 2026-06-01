import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

function Inventory({ inventory, token, onSell, theme }) {
    const [loadingItem, setLoadingItem] = useState(null);
    const [floatingGold, setFloatingGold] = useState(null);
    const [viewMode, setViewMode] = useState("list");
    const [search, setSearch] = useState("");

    const handleSell = async (itemName) => {
        try {
            setLoadingItem(itemName);
            setFloatingGold(itemName);

            setTimeout(() => {
                setFloatingGold(null);
            }, 900);

            await onSell(itemName);

        } finally {
            setLoadingItem(null);
        }
    };

    const cardStyle = {
        background: theme.cardBg,
        color: theme.text,
        padding: "20px",
        borderRadius: "18px",
        boxShadow: "0 12px 35px rgba(0,0,0,0.08)",
        border: "1px solid rgba(0,0,0,0.05)",
        position: "relative",
        overflow: "hidden"
    };

    const titleStyle = {
        fontSize: "1.2rem",
        fontWeight: "800",
        marginBottom: "12px"
    };

    const mutedText = {
        color: theme.subText,
        padding: "10px 0"
    };

    const buttonBase = {
        padding: "8px 14px",
        borderRadius: "10px",
        border: "none",
        fontWeight: "600"
    };

    const toggleBtn = {
        padding: "6px 10px",
        borderRadius: "8px",
        border: "none",
        marginBottom: "12px",
        cursor: "pointer",
        fontWeight: "600",
        background: theme.subText + "20",
        color: theme.text
    };

    const searchBar = {
        width: "100%",
        padding: "10px 12px",
        borderRadius: "10px",
        border: `1px solid ${theme.subText}33`,
        marginBottom: "12px",
        outline: "none",
        background: theme.cardBg,
        color: theme.text
    };

    if (!token) {
        return (
            <div style={cardStyle}>
                <h2 style={titleStyle}>Inventory</h2>
                <p style={mutedText}>🔒 Please login to view inventory</p>
            </div>
        );
    }

    // FILTER ITEMS BASED ON SEARCH
    const filteredInventory = inventory.filter((item) =>
        item.itemName.toLowerCase().includes(search.toLowerCase())
    );

    const containerStyle =
        viewMode === "grid"
            ? {
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))",
                gap: "12px",
                marginTop: "12px"
            }
            : {
                display: "block"
            };

    return (
        <div style={cardStyle}>
            <h2 style={titleStyle}>Inventory</h2>

            {/* SEARCH BAR */}
            <input
                type="text"
                placeholder="Search items..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                style={searchBar}
            />

            {/* VIEW TOGGLE */}
            <button
                style={toggleBtn}
                onClick={() =>
                    setViewMode((prev) =>
                        prev === "list" ? "grid" : "list"
                    )
                }
            >
                Switch to {viewMode === "list" ? "Grid" : "List"}
            </button>

            {/* FLOATING GOLD ANIMATION */}
            <AnimatePresence>
                {floatingGold && (
                    <motion.div
                        initial={{ opacity: 0, y: 10, scale: 0.8 }}
                        animate={{ opacity: 1, y: -20, scale: 1.2 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.8 }}
                        style={{
                            position: "absolute",
                            top: "10px",
                            right: "20px",
                            color: "#fbbf24",
                            fontWeight: "800",
                            fontSize: "1rem",
                            pointerEvents: "none"
                        }}
                    >
                        +Gold 💰
                    </motion.div>
                )}
            </AnimatePresence>

            {/* EMPTY STATE */}
            {filteredInventory.length === 0 && (
                <p style={mutedText}>🎒 No matching items found</p>
            )}

            {/* ITEMS */}
            <div style={containerStyle}>
                <AnimatePresence>
                    {filteredInventory.map((item) => {
                        const isLoading = loadingItem === item.itemName;

                        const itemCardStyle =
                            viewMode === "grid"
                                ? {
                                    padding: "14px",
                                    borderRadius: "14px",
                                    border: `1px solid ${theme.subText}33`,
                                    background: theme.cardBg,
                                    boxShadow: "0 8px 18px rgba(0,0,0,0.06)",
                                    opacity: isLoading ? 0.6 : 1,
                                    display: "flex",
                                    flexDirection: "column",
                                    gap: "10px"
                                }
                                : {
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    padding: "14px",
                                    marginTop: "12px",
                                    borderRadius: "12px",
                                    border: `1px solid ${theme.subText}33`,
                                    background: theme.cardBg,
                                    boxShadow: "0 8px 18px rgba(0,0,0,0.06)",
                                    opacity: isLoading ? 0.6 : 1
                                };

                        return (
                            <motion.div
                                key={item.itemName}
                                initial={{ opacity: 0, y: 10, scale: 0.98 }}
                                animate={{ opacity: 1, y: 0, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                transition={{ duration: 0.2 }}
                                style={itemCardStyle}
                            >
                                {/* ITEM INFO */}
                                <div style={{ display: "flex", flexDirection: "column" }}>
                                    <span style={{ fontWeight: "700" }}>
                                        {item.itemName}
                                    </span>

                                    <span
                                        style={{
                                            color: theme.subText,
                                            fontSize: "0.85rem",
                                            marginTop: "4px",
                                            background: `${theme.subText}20`,
                                            padding: "2px 8px",
                                            borderRadius: "999px",
                                            width: "fit-content"
                                        }}
                                    >
                                        Qty: {item.quantity}
                                    </span>
                                </div>

                                {/* SELL BUTTON */}
                                <button
                                    onClick={() => handleSell(item.itemName)}
                                    disabled={isLoading}
                                    style={{
                                        ...buttonBase,
                                        cursor: isLoading
                                            ? "not-allowed"
                                            : "pointer",
                                        background: isLoading
                                            ? "#9ca3af"
                                            : "#ef4444",
                                        color: "white",
                                        transform: isLoading
                                            ? "scale(0.97)"
                                            : "scale(1)",
                                        transition: "0.2s",
                                        marginTop:
                                            viewMode === "grid" ? "auto" : "0"
                                    }}
                                >
                                    {isLoading ? "Selling..." : "Sell"}
                                </button>
                            </motion.div>
                        );
                    })}
                </AnimatePresence>
            </div>
        </div>
    );
}

export default Inventory;