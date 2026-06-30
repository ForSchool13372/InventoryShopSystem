import { motion } from "framer-motion";

function InventoryItemCard({
    item,
    theme,
    isSelected,
    isLoading,
    toggleSelect,
    formatName,
    onSell
}) {
    const rarityStyles = {
        trash: { glow: "rgba(148,163,184,0.12)", color: "#64748b" },
        common: { glow: "rgba(34,197,94,0.25)", color: "#22c55e" },
        rare: { glow: "rgba(59,130,246,0.25)", color: "#60a5fa" },
        epic: { glow: "rgba(168,85,247,0.25)", color: "#c084fc" },
        legendary: { glow: "rgba(251,191,36,0.25)", color: "#fbbf24" }
    };

    const rarity = rarityStyles[item.rarity] || rarityStyles.common;

    return (
        <motion.div
            className="inventoryCard"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            whileHover={{ scale: 1.015 }}
            style={{
                display: "flex",
                justifyContent: "space-between",
                gap: "12px",
                padding: "14px",
                borderRadius: "14px",
                cursor: "pointer",
                position: "relative",

                background: isSelected
                    ? "linear-gradient(135deg, rgba(34,197,94,0.10), transparent)"
                    : theme.cardBg,

                border: isSelected
                    ? "1px solid rgba(34,197,94,0.55)"
                    : `1px solid ${theme.subText}22`,

                boxShadow: isSelected
                    ? `0 0 0 1px rgba(34,197,94,0.15), 0 10px 30px rgba(0,0,0,0.25)`
                    : "0 10px 25px rgba(0,0,0,0.18)",

                opacity: isLoading ? 0.6 : 1,
            }}
        >

            {/* LEFT SIDE FIXED ALIGNMENT */}
            <div style={{
                display: "flex",
                gap: "10px",
                alignItems: "flex-start"
            }}>

                {/* checkbox */}
                <div style={{
                    paddingTop: "2px",
                    flexShrink: 0
                }}>
                    <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => toggleSelect(item)}
                        style={{
                            transform: "scale(1.1)",
                            cursor: "pointer"
                        }}
                    />
                </div>

                {/* Content block  */}
                <div style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "6px",
                    justifyContent: "flex-start"
                }}>

                    {/* NAME */}
                    <div style={{
                        fontWeight: 900,
                        fontSize: "0.95rem",
                        color: theme.text,
                        lineHeight: "1.1"
                    }}>
                        {formatName(item.itemName)}
                    </div>

                    {/* DESCRIPTION */}
                    <div style={{
                        fontSize: "0.72rem",
                        color: theme.subText,
                        opacity: 0.9,
                        lineHeight: "1.35",
                        maxWidth: "320px",

                        display: "-webkit-box",
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: "vertical",
                        overflow: "hidden",
                        wordBreak: "break-word"
                    }}>
                        {item.description || "No description available"}
                    </div>

                    {/* TAGS (stable row) */}
                    <div style={{
                        display: "flex",
                        gap: "6px",
                        flexWrap: "wrap",
                        alignItems: "center"
                    }}>
                        <span style={{
                            fontSize: "0.65rem",
                            padding: "3px 8px",
                            borderRadius: "999px",
                            background: "rgba(99,102,241,0.15)",
                            color: "#a5b4fc",
                            border: "1px solid rgba(99,102,241,0.25)"
                        }}>
                            {formatName(item.itemType)}
                        </span>

                        <span style={{
                            fontSize: "0.65rem",
                            padding: "3px 8px",
                            borderRadius: "999px",
                            background: rarity.glow,
                            color: rarity.color,
                            border: "1px solid rgba(255,255,255,0.08)",
                            fontWeight: 700,
                            letterSpacing: "0.4px"
                        }}>
                            {formatName(item.rarity)}
                        </span>
                    </div>

                </div>
            </div>

            {/* RIGHT SIDE */}
            <div style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "flex-end",
                justifyContent: "space-between",
                width: "140px",
                flexShrink: 0
            }}>

                <div style={{
                    fontWeight: 900,
                    fontSize: "0.75rem",
                    color: "#fbbf24"
                }}>
                    x{item.quantity}
                </div>

                <div style={{
                    textAlign: "right",
                    fontSize: "0.75rem",
                    fontWeight: 800,
                    color: "#22c55e"
                }}>
                    💰 {item.price ?? 0}
                    <div style={{ opacity: 0.75, fontWeight: 600 }}>
                        Total: {(item.price ?? 0) * item.quantity}
                    </div>
                </div>

                <div style={{ display: "flex", gap: "6px" }}>
                    <button
                        onClick={() => onSell(item.itemName, 1)}
                        disabled={isLoading}
                        style={{
                            padding: "5px 10px",
                            borderRadius: "7px",
                            border: "1px solid rgba(34,197,94,0.25)",
                            fontSize: "0.65rem",
                            background: "rgba(34,197,94,0.10)",
                            color: "#22c55e",
                            fontWeight: 700,
                            cursor: "pointer",
                            opacity: isLoading ? 0.5 : 1
                        }}
                    >
                        Sell
                    </button>

                    <button
                        onClick={() => onSell(item.itemName, item.quantity)}
                        disabled={isLoading}
                        style={{
                            padding: "5px 10px",
                            borderRadius: "7px",
                            border: "1px solid rgba(34,197,94,0.35)",
                            fontSize: "0.65rem",
                            background: "rgba(34,197,94,0.14)",
                            color: "#22c55e",
                            fontWeight: 800,
                            cursor: "pointer",
                            opacity: isLoading ? 0.5 : 1
                        }}
                    >
                        Sell All
                    </button>
                </div>
            </div>

            {/* HOVER */}
            <style>{`
                .inventoryCard:hover {
                    transform: scale(1.015);
                }
            `}</style>

        </motion.div>
    );
}

export default InventoryItemCard;