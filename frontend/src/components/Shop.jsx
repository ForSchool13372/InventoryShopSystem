import { useState, useCallback, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

function Shop({ items, token, onBuy, theme }) {
    const [loadingItem, setLoadingItem] = useState(null);
    const [purchasedItem, setPurchasedItem] = useState(null);
    const [quantities, setQuantities] = useState({});
    const [searchQuery, setSearchQuery] = useState("");

    const setQty = useCallback((itemName, value, maxStock = Infinity) => {
        setQuantities((prev) => ({
            ...prev,
            [itemName]: Math.max(1, Math.min(value, maxStock))
        }));
    }, []);

    const getQty = (itemName) => quantities[itemName] || 1;

    const filteredItems = useMemo(() => {
        return items.filter((item) =>
            item.itemName.toLowerCase().includes(searchQuery.toLowerCase())
        );
    }, [items, searchQuery]);

    const handleBuy = async (item) => {
        const itemName = item.itemName;
        const quantity = getQty(itemName);

        if (!token || item.stock === 0 || quantity > item.stock) return;

        setPurchasedItem(null);
        setLoadingItem(itemName);

        try {
            const success = await onBuy(itemName, quantity);

            if (success === true) {
                setPurchasedItem(itemName);
                setTimeout(() => setPurchasedItem(null), 800);
            } else {
                setPurchasedItem(null);
            }
        } catch {
            setPurchasedItem(null);
        } finally {
            setLoadingItem(null);
        }
    };

    const buyMax = (item) => {
        setQty(item.itemName, item.stock, item.stock);
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
        color: theme.text,
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

    const metaStyle = {
        color: theme.subText,
        fontSize: "0.8rem"
    };

    return (
        <motion.div
            style={cardStyle}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
        >
            <h2 style={titleStyle}>Shop</h2>

            {/* SEARCH */}
            <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search items..."
                style={{
                    width: "90%",
                    padding: "10px 12px",
                    marginBottom: "14px",
                    borderRadius: "10px",
                    border: `1px solid ${theme.subText}55`,
                    background: theme.cardBg,
                    color: theme.text
                }}
            />

            <AnimatePresence>
                {purchasedItem && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.8, y: 10 }}
                        animate={{ opacity: 1, scale: 1.2, y: -10 }}
                        exit={{ opacity: 0 }}
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

            {filteredItems.length === 0 && (
                <div style={{ color: theme.subText, padding: "10px 0" }}>
                    🛒 No items found
                </div>
            )}

            {/* GRID */}
            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
                    gap: "12px",

                    maxHeight: "70vh",
                    overflowY: "auto",
                    overflowX: "hidden",
                    paddingRight: "6px",

                    scrollBehavior: "smooth"
                }}
            >
                {filteredItems.map((item) => {
                    const isLoading = loadingItem === item.itemName;
                    const qty = getQty(item.itemName);

                    const isDisabled =
                        !token ||
                        item.stock === 0 ||
                        isLoading ||
                        qty > item.stock;

                    return (
                        <motion.div
                            key={item.itemName}
                            whileHover={{ scale: 1.02 }}
                            style={{
                                padding: "14px",
                                borderRadius: "12px",
                                border: `1px solid ${theme.subText}33`,
                                background: theme.cardBg,
                                opacity: item.stock === 0 ? 0.6 : 1,
                                display: "flex",
                                flexDirection: "column",
                                justifyContent: "space-between"
                            }}
                        >
                            {/* HEADER ROW (name + price) */}
                            <div style={{
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                marginBottom: "6px"
                            }}>
                                <div style={{ fontWeight: "800" }}>
                                    {item.itemName.charAt(0).toUpperCase() + item.itemName.slice(1)}
                                </div>

                                <div style={{
                                    color: "#fbbf24",
                                    fontSize: "0.85rem",
                                    fontWeight: "700"
                                }}>
                                    💰 {item.price ?? "N/A"}
                                </div>
                            </div>

                            {/* META ROW (stock + total) */}
                            <div style={{
                                display: "flex",
                                justifyContent: "space-between",
                                marginBottom: "10px"
                            }}>
                                <div style={metaStyle}>
                                    Stock: {item.stock}
                                </div>

                                <div style={metaStyle}>
                                    Total: {(item.price ?? 0) * qty}
                                </div>
                            </div>

                            {/* QTY CONTROLS */}
                            {token && item.stock > 0 && (
                                <div style={{
                                    display: "flex",
                                    alignItems: "center",
                                    gap: "6px",
                                    flexWrap: "wrap"
                                }}>
                                    <button
                                        onClick={() => setQty(item.itemName, qty - 1, item.stock)}
                                        style={{ ...buttonBase, padding: "4px 10px" }}
                                    >
                                        -
                                    </button>

                                    <span style={{ fontWeight: "700" }}>
                                        x{qty}
                                    </span>

                                    <button
                                        onClick={() => setQty(item.itemName, qty + 1, item.stock)}
                                        disabled={qty >= item.stock}
                                        style={{ ...buttonBase, padding: "4px 10px" }}
                                    >
                                        +
                                    </button>

                                    <button
                                        onClick={() => buyMax(item)}
                                        style={{
                                            ...buttonBase,
                                            background: "#111827",
                                            color: "white",
                                            marginLeft: "6px"
                                        }}
                                    >
                                        Max
                                    </button>
                                </div>
                            )}

                            {/* BUY BUTTON */}
                            {token && (
                                <motion.button
                                    onClick={() => handleBuy(item)}
                                    disabled={isDisabled}
                                    whileTap={{ scale: 0.95 }}
                                    style={{
                                        ...buttonBase,
                                        marginTop: "10px",
                                        cursor: isDisabled ? "not-allowed" : "pointer",
                                        background: isLoading
                                            ? "#9ca3af"
                                            : item.stock === 0
                                                ? "#ef4444"
                                                : "#4f46e5",
                                        color: "white"
                                    }}
                                >
                                    {isLoading
                                        ? "Buying..."
                                        : item.stock === 0
                                            ? "Out of stock"
                                            : `Buy x${qty}`}
                                </motion.button>
                            )}
                        </motion.div>
                    );
                })}
            </div>
        </motion.div>
    );
}

export default Shop;