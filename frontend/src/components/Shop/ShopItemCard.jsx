import { motion } from "framer-motion";

function ShopItemCard({ item, theme, addToCart, formatName }) {
    const rarityGlow =
        item.rarity === "common"
            ? "rgba(34,197,94,0.35)"
            : item.rarity === "trash"
                ? "rgba(156,163,175,0.35)"
                : "rgba(251,191,36,0.35)";

    return (
        <motion.div
            key={`${item?.itemName ?? "item"}-${item.price ?? 0}`}
            whileHover={{
                y: -4,
                boxShadow: "0 14px 30px rgba(0,0,0,0.12)"
            }}
            transition={{ type: "spring", stiffness: 300, damping: 22 }}
            onClick={() => addToCart(item)}
            style={{
                padding: "14px",
                borderRadius: "12px",
                background: theme.cardBg,
                border: `1px solid ${rarityGlow}`,
                boxShadow: `0 0 0px ${rarityGlow}`,
                cursor: item.stock === 0 ? "not-allowed" : "pointer",
                opacity: item.stock === 0 ? 0.45 : 1,
                display: "flex",
                flexDirection: "column",
                gap: "10px",
                position: "relative",
                overflow: "hidden"
            }}
        >
            {/* HEADER */}
            <div style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                gap: "10px"
            }}>
                <div style={{ display: "flex", flexDirection: "column" }}>
                    <div style={{
                        fontWeight: 900,
                        color: theme.text,
                        fontSize: "0.95rem"
                    }}>
                        {formatName(item.itemName)}
                    </div>

                    <div style={{
                        fontSize: "0.72rem",
                        color: theme.subText,
                        marginTop: "4px",
                        lineHeight: "1.3"
                    }}>
                        {item.description || "No description available"}
                    </div>
                </div>

                {/* PRICE BADGE */}
                <div style={{
                    fontWeight: 900,
                    fontSize: "0.8rem",
                    color: "#fbbf24",
                    background: "rgba(251,191,36,0.10)",
                    padding: "4px 10px",
                    borderRadius: "999px",
                    whiteSpace: "nowrap",
                    border: "1px solid rgba(251,191,36,0.25)"
                }}>
                    💰 {item.price}
                </div>
            </div>

            {/* BOTTOM BAR */}
            <div style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                fontSize: "0.7rem",
                flexWrap: "wrap",
                gap: "6px"
            }}>
                <div style={{
                    display: "flex",
                    gap: "6px",
                    flexWrap: "wrap"
                }}>
                    {/* TYPE */}
                    <span style={{
                        padding: "3px 8px",
                        borderRadius: "999px",
                        background: "rgba(99,102,241,0.12)",
                        color: "#818cf8"
                    }}>
                        {item.itemType}
                    </span>

                    {/* RARITY */}
                    <span style={{
                        padding: "3px 8px",
                        borderRadius: "999px",
                        background: rarityGlow,
                        color:
                            item.rarity === "common"
                                ? "#22c55e"
                                : item.rarity === "trash"
                                    ? "#9ca3af"
                                    : "#fbbf24",
                        fontWeight: 700
                    }}>
                        {item.rarity}
                    </span>

                    {/* STOCK */}
                    <span style={{
                        padding: "3px 8px",
                        borderRadius: "999px",
                        background: "rgba(107,114,128,0.12)",
                        color: theme.subText
                    }}>
                        Stock: {item.stock}
                    </span>
                </div>

                {/* AVAILABILITY */}
                <span style={{
                    padding: "3px 8px",
                    borderRadius: "999px",
                    background: item.stock > 0
                        ? "rgba(34,197,94,0.12)"
                        : "rgba(239,68,68,0.12)",
                    color: item.stock > 0 ? "#22c55e" : "#ef4444",
                    fontWeight: 700
                }}>
                    {item.stock > 0 ? "Available" : "Out of stock"}
                </span>
            </div>
        </motion.div>
    );
}

export default ShopItemCard;