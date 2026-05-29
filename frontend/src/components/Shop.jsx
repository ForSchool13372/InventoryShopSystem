import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

function Shop({ items, token, onBuy, theme }) {
    const [loadingItem, setLoadingItem] = useState(null);
    const [purchasedItem, setPurchasedItem] = useState(null);

    const handleBuy = async (itemName) => {
        try {
            setLoadingItem(itemName);

            // trigger visual feedback instantly
            setPurchasedItem(itemName);
            setTimeout(() => setPurchasedItem(null), 800);

            await onBuy(itemName);

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

    const buttonBase = {
        padding: "8px 14px",
        borderRadius: "10px",
        border: "none",
        fontWeight: "600"
    };

    const emptyStateStyle = {
        color: theme.subText,
        padding: "10px 0"
    };

    return (
        <motion.div
            style={cardStyle}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
        >
            {/* HEADER */}
            <h2 style={titleStyle}>Shop</h2>

            {/* 💥 PURCHASE GLOW EFFECT */}
            <AnimatePresence>
                {purchasedItem && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.8, y: 10 }}
                        animate={{ opacity: 1, scale: 1.2, y: -10 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.6 }}
                        style={{
                            position: "absolute",
                            top: "12px",
                            right: "16px",
                            color: "#22c55e",
                            fontWeight: "800",
                            fontSize: "0.95rem",
                            pointerEvents: "none"
                        }}
                    >
                        +Purchased ✔
                    </motion.div>
                )}
            </AnimatePresence>

            {/* EMPTY STATE */}
            {items.length === 0 && (
                <div style={emptyStateStyle}>
                    🛒 Shop is currently empty
                </div>
            )}

            {/* ITEMS */}
            <AnimatePresence>
                {items.map((item) => {
                    const isLoading = loadingItem === item.itemName;
                    const isDisabled = !token || item.stock === 0 || isLoading;

                    return (
                        <motion.div
                            key={item.itemName}
                            layout
                            initial={{ opacity: 0, y: 10, scale: 0.98 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            whileHover={{ scale: 1.02 }}
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
                                boxShadow: isLoading
                                    ? "0 6px 14px rgba(0,0,0,0.05)"
                                    : "0 10px 22px rgba(0,0,0,0.06)",
                                opacity: item.stock === 0 ? 0.6 : 1
                            }}
                        >
                            {/* ITEM INFO */}
                            <div style={{ display: "flex", flexDirection: "column" }}>
                                <span style={{ fontWeight: "800" }}>
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
                                    Stock: {item.stock}
                                </span>
                            </div>

                            {/* BUTTON */}
                            {token && (
                                <motion.button
                                    onClick={() => handleBuy(item.itemName)}
                                    disabled={isDisabled}
                                    whileTap={{ scale: 0.95 }}
                                    whileHover={{ scale: isDisabled ? 1 : 1.08 }}
                                    style={{
                                        ...buttonBase,
                                        cursor: isDisabled ? "not-allowed" : "pointer",
                                        background: isLoading
                                            ? "#9ca3af"
                                            : item.stock === 0
                                                ? "#ef4444"
                                                : "#4f46e5",
                                        color: "white",
                                        transform: isLoading ? "scale(0.97)" : "scale(1)",
                                        transition: "0.2s"
                                    }}
                                >
                                    {isLoading
                                        ? "Buying..."
                                        : item.stock === 0
                                            ? "Out of stock"
                                            : "Buy"}
                                </motion.button>
                            )}
                        </motion.div>
                    );
                })}
            </AnimatePresence>
        </motion.div>
    );
}

export default Shop;