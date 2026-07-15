import { motion } from "framer-motion";

import { buttonBase } from "../../styles/uiStyles";
import { getShopCartStyles } from "./shopCartStyles";

function ShopCart({
    cart,
    setQty,
    handleBuy,
    theme,
    token,
    loadingItem,
    canAfford
}) {
    const styles = getShopCartStyles(theme);

    const cartHasItems = Object.keys(cart).length > 0;

    const totalCartCost = Object.values(cart).reduce(
        (sum, entry) => sum + (entry.item.price ?? 0) * entry.qty,
        0
    );

    const formatName = (name) =>
        name.charAt(0).toUpperCase() + name.slice(1);

    const buttonStyle = {
        ...buttonBase,
        background: theme.mode === "dark"
            ? "rgba(255,255,255,0.06)"
            : "rgba(0,0,0,0.06)",
        color: theme.text,
        border: `1px solid ${theme.subText}22`
    };

    return (
        <div style={styles.container}>

            <h3 style={styles.header}>
                🧾 Cart
            </h3>

            {!cartHasItems ? (
                <p style={styles.empty}>
                    Cart is empty
                </p>
            ) : (
                <>
                    {Object.values(cart).map((entry) => {
                        const total = entry.item.price * entry.qty;

                        return (
                            <div
                                key={`${entry?.item?.itemName ?? "item"}-${entry.item?.price ?? 0}`}
                                style={styles.item}
                            >

                                <div style={styles.itemHeader}>
                                    <div style={styles.itemName}>
                                        {formatName(entry.item.itemName)}
                                    </div>

                                    <div style={styles.totalBadge}>
                                        💰 {total}
                                    </div>
                                </div>


                                <div style={styles.badges}>
                                    <span style={styles.unitBadge}>
                                        Unit: 💰 {entry.item.price}
                                    </span>

                                    <span style={styles.qtyBadge}>
                                        Qty: {entry.qty}
                                    </span>

                                    <span style={styles.stockBadge}>
                                        Stock: {entry.item.stock}
                                    </span>
                                </div>


                                <div style={styles.controls}>

                                    <button
                                        style={buttonStyle}
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


                                    <span style={styles.quantity}>
                                        x{entry.qty}
                                    </span>


                                    <button
                                        style={buttonStyle}
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
                                            setQty(
                                                entry.item.itemName,
                                                0,
                                                entry.item.stock
                                            )
                                        }
                                    >
                                        🗑️
                                    </button>

                                </div>

                            </div>
                        );
                    })}


                    <div style={styles.divider} />


                    <div style={styles.summary}>

                        <div style={styles.summaryRow}>
                            <span>Total</span>
                            <span>💰 {totalCartCost}</span>
                        </div>


                        <div style={styles.affordability(canAfford)}>
                            {canAfford
                                ? "✓ Can afford"
                                : "✕ Not enough gold"}
                        </div>

                    </div>


                    <motion.button
                        whileTap={{ scale: 0.95 }}
                        onClick={handleBuy}
                        disabled={!token || !cartHasItems || !canAfford}
                        style={{
                            ...buttonBase,
                            ...styles.buyButton(canAfford)
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