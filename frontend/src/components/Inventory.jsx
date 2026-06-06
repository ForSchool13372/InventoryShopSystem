import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

function Inventory({ inventory, token, onSell, theme }) {
    const [loadingItem, setLoadingItem] = useState(null);
    const [floatingGold, setFloatingGold] = useState(null);
    const [viewMode, setViewMode] = useState("list");
    const [search, setSearch] = useState("");

    // quantity state per item
    const [quantities, setQuantities] = useState({});

    const getQty = (name) => quantities[name] || 1;

    const setQty = (name, value) => {
        setQuantities((prev) => ({
            ...prev,
            [name]: Math.max(1, value)
        }));
    };

    const handleSell = async (itemName, quantity = 1) => {
        try {
            setLoadingItem(itemName);
            setFloatingGold(itemName);

            setTimeout(() => {
                setFloatingGold(null);
            }, 900);

            await onSell(itemName, quantity);

        } finally {
            setLoadingItem(null);
        }
    };

    const sellAll = (item) => {
        setQty(item.itemName, item.quantity);
        handleSell(item.itemName, item.quantity);
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
        marginBottom: "12px",
        color: theme.text
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

            <input
                type="text"
                placeholder="Search items..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                style={searchBar}
            />

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

            {/* FLOATING GOLD */}
            <AnimatePresence>
                {floatingGold && (
                    <motion.div
                        initial={{ opacity: 0, y: 10, scale: 0.8 }}
                        animate={{ opacity: 1, y: -20, scale: 1.2 }}
                        exit={{ opacity: 0 }}
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

            {filteredInventory.length === 0 && (
                <p style={mutedText}>🎒 No matching items found</p>
            )}

            <div style={containerStyle}>
                <AnimatePresence>
                    {filteredInventory.map((item) => {
                        const isLoading = loadingItem === item.itemName;
                        const qty = getQty(item.itemName);

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
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0 }}
                                style={itemCardStyle}
                            >
                                <div style={{ display: "flex", flexDirection: "column" }}>
                                    <span style={{ fontWeight: "700" }}>
                                        {item.itemName}
                                    </span>

                                    <span style={{
                                        color: theme.subText,
                                        fontSize: "0.85rem",
                                        marginTop: "4px"
                                    }}>
                                        Qty: {item.quantity}
                                    </span>

                                    {/* QUANTITY CONTROLS */}
                                    <div style={{ display: "flex", gap: "6px", marginTop: "8px", alignItems: "center" }}>

                                        <button
                                            onClick={() => setQty(item.itemName, Math.max(1, qty - 1))}
                                            style={buttonBase}
                                        >
                                            -
                                        </button>

                                        <span style={{ fontWeight: "700", minWidth: "20px", textAlign: "center" }}>
                                            {qty}
                                        </span>

                                        <button
                                            onClick={() =>
                                                setQty(item.itemName, Math.min(item.quantity, qty + 1))
                                            }
                                            disabled={qty >= item.quantity}
                                            style={buttonBase}
                                        >
                                            +
                                        </button>

                                    </div>
                                </div>

                                {/* SELL BUTTONS */}
                                <div style={{ display: "flex", gap: "6px" }}>
                                    <button
                                        onClick={() => handleSell(item.itemName, qty)}
                                        disabled={isLoading}
                                        style={{
                                            ...buttonBase,
                                            background: "#ef4444",
                                            color: "white"
                                        }}
                                    >
                                        {isLoading ? "Selling..." : `Sell x${qty}`}
                                    </button>

                                    <button
                                        onClick={() => sellAll(item)}
                                        disabled={isLoading}
                                        style={{
                                            ...buttonBase,
                                            background: "#111827",
                                            color: "white"
                                        }}
                                    >
                                        Sell All
                                    </button>
                                </div>
                            </motion.div>
                        );
                    })}
                </AnimatePresence>
            </div>
        </div>
    );
}

export default Inventory;