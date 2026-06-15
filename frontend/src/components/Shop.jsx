import { useState, useCallback, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

function Shop({ items, token, onBuy, theme, playerStats }) {
    const [loadingItem, setLoadingItem] = useState(null);
    const [purchasedItem, setPurchasedItem] = useState(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [cart, setCart] = useState({});

    const playerGold = playerStats?.gold ?? 0;

    const formatName = (name) =>
        name.charAt(0).toUpperCase() + name.slice(1);

    const setQty = useCallback((itemName, value, maxStock) => {
        setCart((prev) => {
            const current = prev[itemName];

            if (!current) return prev;

            // HANDLE REMOVE ONLY when explicitly called (value === 0)
            if (value === 0) {
                const updated = { ...prev };
                delete updated[itemName];
                return updated;
            }

            // ALWAYS clamp between 1 and maxStock
            const newQty = Math.max(1, Math.min(value, maxStock));

            return {
                ...prev,
                [itemName]: {
                    ...current,
                    qty: newQty
                }
            };
        });
    }, []);

    const addToCart = (item) => {
        setCart((prev) => ({
            ...prev,
            [item.itemName]: {
                item,
                qty: prev[item.itemName]?.qty || 1
            }
        }));
    };

    const totalCartCost = useMemo(() => {
        return Object.values(cart).reduce((sum, entry) => {
            return sum + (entry.item.price ?? 0) * entry.qty;
        }, 0);
    }, [cart]);

    const canAfford = playerGold >= totalCartCost;

    const filteredItems = useMemo(() => {
        return items.filter((item) =>
            item.itemName.toLowerCase().includes(searchQuery.toLowerCase())
        );
    }, [items, searchQuery]);

    const handleBuy = async () => {
        if (!token || Object.keys(cart).length === 0) return;
        if (!canAfford) return;

        setLoadingItem("cart");

        try {
            for (const entry of Object.values(cart)) {
                await onBuy(entry.item.itemName, entry.qty);
            }

            setCart({});
            setPurchasedItem(true);
            setTimeout(() => setPurchasedItem(false), 900);
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
        display: "flex",
        gap: "16px"
    };

    const buttonBase = {
        padding: "6px 10px",
        borderRadius: "10px",
        border: "none",
        fontWeight: "600",
        cursor: "pointer",
        minWidth: "34px", 
        textAlign: "center"
    };

    return (
        <motion.div
            style={cardStyle}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
        >
            {/* LEFT - ITEMS */}
            <div style={{ flex: 2 }}>
                <h2 style={{
                    fontWeight: "800",
                    color: theme.text,
                    fontSize: "1.4rem"
                }}>
                    🛒 Shop
                </h2>

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

                <div style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
                    gap: "12px",
                    maxHeight: "70vh",
                    overflowY: "auto"
                }}>
                    {filteredItems.map((item) => (
                        <motion.div
                            key={item.itemName}
                            whileHover={{ scale: 1.02 }}
                            onClick={() => addToCart(item)}
                            style={{
                                padding: "14px",
                                borderRadius: "12px",
                                border: `1px solid ${theme.subText}33`,
                                background: theme.cardBg,
                                cursor: "pointer",
                                opacity: item.stock === 0 ? 0.5 : 1,
                                display: "flex",
                                flexDirection: "column",
                                gap: "8px"
                            }}
                        >
                            {/* TOP ROW */}
                            <div style={{
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center"
                            }}>
                                <div style={{ fontWeight: "800" }}>
                                    {formatName(item.itemName)}
                                </div>

                                <div style={{
                                    fontWeight: "800",
                                    fontSize: "0.85rem",
                                    color: "#fbbf24",
                                    background: "rgba(251,191,36,0.08)",
                                    padding: "3px 8px",
                                    borderRadius: "999px"
                                }}>
                                    💰 {item.price}
                                </div>
                            </div>

                            {/* META ROW */}
                            <div style={{
                                display: "flex",
                                gap: "6px",
                                flexWrap: "wrap"
                            }}>
                                <span style={{
                                    fontSize: "0.7rem",
                                    padding: "3px 8px",
                                    borderRadius: "999px",
                                    background: theme.subText + "20",
                                    color: theme.subText
                                }}>
                                    Stock: {item.stock}
                                </span>

                                <span style={{
                                    fontSize: "0.7rem",
                                    padding: "3px 8px",
                                    borderRadius: "999px",
                                    background: item.stock > 0
                                        ? "rgba(34,197,94,0.1)"
                                        : "rgba(239,68,68,0.1)",
                                    color: item.stock > 0 ? "#22c55e" : "#ef4444"
                                }}>
                                    {item.stock > 0 ? "Available" : "Out of stock"}
                                </span>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* RIGHT - CART */}
            <div style={{
                flex: "0 0 320px", 
                padding: "14px",
                borderRadius: "12px",
                border: `1px solid ${theme.subText}33`,
                background: theme.cardBg,
                height: "fit-content",
                position: "sticky",
                top: "20px"
            }}>
                <h3>🧾 Cart</h3>

                {Object.keys(cart).length === 0 ? (
                    <p style={{ color: theme.subText }}>Cart is empty</p>
                ) : (
                    <>
                            {Object.values(cart).map((entry) => (
                                <div
                                    key={entry.item.itemName}
                                    style={{
                                        marginBottom: "12px",
                                        padding: "10px",
                                        borderRadius: "12px",
                                        border: `1px solid ${theme.subText}22`,
                                        background: theme.cardBg,
                                        display: "flex",
                                        flexDirection: "column",
                                        gap: "8px"
                                    }}
                                >
                                    {/* TOP ROW */}
                                    <div style={{
                                        display: "flex",
                                        justifyContent: "space-between",
                                        alignItems: "center"
                                    }}>
                                        <div style={{ fontWeight: "800" }}>
                                            {formatName(entry.item.itemName)}
                                        </div>

                                        <div style={{
                                            fontSize: "0.8rem",
                                            fontWeight: "700",
                                            color: "#fbbf24",
                                            background: "rgba(251,191,36,0.08)",
                                            padding: "3px 8px",
                                            borderRadius: "999px"
                                        }}>
                                            💰 {entry.item.price}
                                        </div>
                                    </div>

                                    {/* QTY CONTROLS */}
                                    <div style={{
                                        display: "flex",
                                        alignItems: "center",
                                        gap: "6px",
                                        flexWrap: "wrap"
                                    }}>
                                        <button
                                            style={{
                                                ...buttonBase,
                                                width: "32px",
                                                height: "32px",
                                                padding: 0
                                            }}
                                            onClick={() =>
                                                setQty(
                                                    entry.item.itemName,
                                                    Math.max(1, entry.qty - 1),
                                                    entry.item.stock
                                                )
                                            }
                                        >
                                            -
                                        </button>

                                        <span style={{
                                            fontWeight: "800",
                                            minWidth: "28px",
                                            textAlign: "center"
                                        }}>
                                            x{entry.qty}
                                        </span>

                                        <button
                                            style={{
                                                ...buttonBase,
                                                width: "32px",
                                                height: "32px",
                                                padding: 0
                                            }}
                                            onClick={() =>
                                                setQty(
                                                    entry.item.itemName,
                                                    entry.qty + 1,
                                                    entry.item.stock
                                                )
                                            }
                                        >
                                            +
                                        </button>

                                        {/* MAX */}
                                        <button
                                            style={{
                                                ...buttonBase,
                                                marginLeft: "auto",
                                                background: "#111827",
                                                color: "white",
                                                padding: "6px 10px"
                                            }}
                                            onClick={() =>
                                                setQty(
                                                    entry.item.itemName,
                                                    entry.item.stock,
                                                    entry.item.stock
                                                )
                                            }
                                        >
                                            Max
                                        </button>

                                        {/* REMOVE */}
                                        <button
                                            style={{
                                                ...buttonBase,
                                                background: "#ef4444",
                                                color: "white",
                                                padding: "6px 10px"
                                            }}
                                            onClick={() =>
                                                setQty(entry.item.itemName, 0, entry.item.stock)
                                            }
                                        >
                                            Remove
                                        </button>
                                    </div>
                                </div>
                            ))}

                        <hr />

                        <div style={{ marginTop: "10px" }}>
                            <div>Total: 💰 {totalCartCost}</div>

                            <div style={{
                                color: canAfford ? "#22c55e" : "#ef4444",
                                fontWeight: "600"
                            }}>
                                {canAfford ? "Can afford" : "Not enough gold"}
                            </div>
                        </div>

                        <motion.button
                            whileTap={{ scale: 0.95 }}
                            onClick={handleBuy}
                            disabled={!token || !canAfford}
                            style={{
                                ...buttonBase,
                                width: "100%",
                                marginTop: "10px",
                                background: canAfford ? "#4f46e5" : "#ef4444",
                                color: "white"
                            }}
                        >
                            {loadingItem ? "Buying..." : "Buy Cart"}
                        </motion.button>
                    </>
                )}
            </div>

            {/* SUCCESS */}
            <AnimatePresence>
                {purchasedItem && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0 }}
                        style={{
                            position: "absolute",
                            top: "12px",
                            right: "16px",
                            color: "#22c55e",
                            fontWeight: "800"
                        }}
                    >
                        ✔ Purchased
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}

export default Shop;