import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

function Inventory({ inventory, token, onSell, theme }) {
    const [loadingItem, setLoadingItem] = useState(null);
    const [floatingGold, setFloatingGold] = useState(null);

    const handleSell = async (itemName) => {
        try {
            setLoadingItem(itemName);

            // fake gold animation trigger BEFORE request finishes
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

    if (!token) {
        return (
            <div style={cardStyle}>
                <h2 style={titleStyle}>Inventory</h2>
                <p style={mutedText}>🔒 Please login to view inventory</p>
            </div>
        );
    }

    return (
        <div style={cardStyle}>
            <h2 style={titleStyle}>Inventory</h2>

            {/* 💰 FLOATING GOLD ANIMATION */}
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
            {inventory.length === 0 && (
                <p style={mutedText}>🎒 No items in inventory yet</p>
            )}

            {/* ITEMS */}
            <AnimatePresence>
                {inventory.map((item) => {
                    const isLoading = loadingItem === item.itemName;

                    return (
                        <motion.div
                            key={item.itemName}
                            initial={{ opacity: 0, y: 10, scale: 0.98 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            transition={{ duration: 0.2 }}
                            style={{
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
                            }}
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
                                    cursor: isLoading ? "not-allowed" : "pointer",
                                    background: isLoading ? "#9ca3af" : "#ef4444",
                                    color: "white",
                                    transform: isLoading ? "scale(0.97)" : "scale(1)",
                                    transition: "0.2s"
                                }}
                            >
                                {isLoading ? "Selling..." : "Sell"}
                            </button>
                        </motion.div>
                    );
                })}
            </AnimatePresence>
        </div>
    );
}

export default Inventory;