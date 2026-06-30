import { motion } from "framer-motion";
import { buttonBase } from "../../styles/uiStyles";

function ShopCart({
    cart,
    setQty,
    handleBuy,
    theme,
    token,
    loadingItem,
    canAfford
}) {
    const cartHasItems = Object.keys(cart).length > 0;

    const totalCartCost = Object.values(cart).reduce(
        (sum, entry) => sum + (entry.item.price ?? 0) * entry.qty,
        0
    );

    const formatName = (name) =>
        name.charAt(0).toUpperCase() + name.slice(1);

    return (
        <div
            style={{
                flex: "0 0 320px",
                padding: "14px",
                borderRadius: "12px",
                border: `1px solid ${theme.subText}33`,
                background: theme.cardBg,
                height: "fit-content",
                position: "sticky",
                top: "20px",
                display: "flex",
                flexDirection: "column",
                gap: "12px"
            }}
        >
            {/* HEADER */}
            <h3 style={{
                fontWeight: 900,
                color: theme.text,
                fontSize: "1.1rem",
                margin: 0
            }}>
                🧾 Cart
            </h3>

            {/* EMPTY STATE */}
            {!cartHasItems ? (
                <p style={{ color: theme.subText, margin: 0 }}>
                    Cart is empty
                </p>
            ) : (
                <>
                    {/* ITEMS */}
                    {Object.values(cart).map((entry) => {
                        const total = entry.item.price * entry.qty;

                        return (
                            <div
                                key={`${entry?.item?.itemName ?? "item"}-${entry.item?.price ?? 0}`}
                                style={{
                                    padding: "12px",
                                    borderRadius: "12px",
                                    border: `1px solid ${theme.subText}22`,
                                    background: theme.cardBg,
                                    display: "flex",
                                    flexDirection: "column",
                                    gap: "10px"
                                }}
                            >
                                {/* NAME + TOTAL */}
                                <div style={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "flex-start",
                                    gap: "10px"
                                }}>
                                    <div style={{
                                        fontWeight: 900,
                                        color: theme.text,
                                        fontSize: "0.95rem"
                                    }}>
                                        {formatName(entry.item.itemName)}
                                    </div>

                                    <div style={{
                                        fontSize: "0.8rem",
                                        fontWeight: 900,
                                        color: "#22c55e",
                                        background: "rgba(34,197,94,0.12)",
                                        padding: "4px 10px",
                                        borderRadius: "999px",
                                        whiteSpace: "nowrap",
                                        border: "1px solid rgba(34,197,94,0.25)"
                                    }}>
                                        💰 {total}
                                    </div>
                                </div>

                                {/* BADGES */}
                                <div style={{
                                    display: "flex",
                                    gap: "6px",
                                    flexWrap: "wrap"
                                }}>
                                    <span style={{
                                        padding: "3px 8px",
                                        borderRadius: "999px",
                                        background: "rgba(251,191,36,0.10)",
                                        color: "#fbbf24",
                                        fontWeight: 700,
                                        fontSize: "0.7rem"
                                    }}>
                                        Unit: 💰 {entry.item.price}
                                    </span>

                                    <span style={{
                                        padding: "3px 8px",
                                        borderRadius: "999px",
                                        background: "rgba(99,102,241,0.12)",
                                        color: "#818cf8",
                                        fontWeight: 700,
                                        fontSize: "0.7rem"
                                    }}>
                                        Qty: {entry.qty}
                                    </span>

                                    <span style={{
                                        padding: "3px 8px",
                                        borderRadius: "999px",
                                        background: "rgba(107,114,128,0.12)",
                                        color: theme.subText,
                                        fontSize: "0.7rem"
                                    }}>
                                        Stock: {entry.item.stock}
                                    </span>
                                </div>

                                {/* CONTROLS */}
                                <div style={{
                                    display: "flex",
                                    alignItems: "center",
                                    gap: "6px",
                                    flexWrap: "wrap"
                                }}>
                                    <button
                                        style={{
                                            ...buttonBase,
                                            background: theme.mode === "dark"
                                                ? "rgba(255,255,255,0.06)"
                                                : "rgba(0,0,0,0.06)",
                                            color: theme.text,
                                            border: `1px solid ${theme.subText}22`
                                        }}
                                        onClick={() =>
                                            setQty(
                                                entry.item.itemName,
                                                Math.max(1, entry.qty - 1),
                                                entry.item.stock
                                            )
                                        }
                                    >
                                        −
                                    </button>

                                    <span style={{
                                        fontWeight: 900,
                                        minWidth: "28px",
                                        color: theme.text
                                    }}>
                                        x{entry.qty}
                                    </span>

                                    <button
                                        style={{
                                            ...buttonBase,
                                            background: theme.mode === "dark"
                                                ? "rgba(255,255,255,0.06)"
                                                : "rgba(0,0,0,0.06)",
                                            color: theme.text,
                                            border: `1px solid ${theme.subText}22`
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

                                    <button
                                        style={{
                                            ...buttonBase,
                                            marginLeft: "auto",
                                            background: "transparent",
                                            color: theme.text,
                                            border: `1px solid ${theme.subText}33`
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

                                    <button
                                        style={{
                                            ...buttonBase,
                                            background: theme.mode === "dark"
                                                ? "rgba(239,68,68,0.15)"
                                                : "rgba(239,68,68,0.10)",
                                            color: "#ef4444",
                                            border: "1px solid rgba(239,68,68,0.25)"
                                        }}
                                        onClick={() =>
                                            setQty(entry.item.itemName, 0, entry.item.stock)
                                        }
                                    >
                                        🗑️
                                    </button>
                                </div>
                            </div>
                        );
                    })}

                    {/* DIVIDER */}
                    <div style={{
                        height: "1px",
                        background: `${theme.subText}22`,
                        margin: "6px 0"
                    }} />

                    {/* SUMMARY */}
                    <div style={{
                        padding: "12px",
                        borderRadius: "12px",
                        background: `${theme.subText}10`,
                        border: `1px solid ${theme.subText}22`,
                        display: "flex",
                        flexDirection: "column",
                        gap: "6px"
                    }}>
                        <div style={{
                            display: "flex",
                            justifyContent: "space-between",
                            fontWeight: 900,
                            color: theme.text
                        }}>
                            <span>Total</span>
                            <span>💰 {totalCartCost}</span>
                        </div>

                        <div style={{
                            color: canAfford ? "#22c55e" : "#ef4444",
                            fontWeight: 800,
                            fontSize: "0.85rem"
                        }}>
                            {canAfford ? "✓ Can afford" : "✕ Not enough gold"}
                        </div>
                    </div>

                    {/* BUY BUTTON */}
                    <motion.button
                        whileTap={{ scale: 0.95 }}
                        onClick={handleBuy}
                        disabled={!token || !cartHasItems || !canAfford}
                        style={{
                            ...buttonBase,
                            width: "100%",
                            background: canAfford ? "#4f46e5" : "#ef4444",
                            color: "white",
                            fontWeight: 900
                        }}
                    >
                        {loadingItem ? "Buying..." : "Buy Cart"}
                    </motion.button>
                </>
            )}
        </div>
    );
}

export default ShopCart;