import { motion } from "framer-motion";
import { getInventoryItemCardStyles } from "./inventoryItemCardStyles";
import soundSystem from "@/utils/soundSystem";

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

    const rarity =
        rarityStyles[item.rarity] || rarityStyles.common;

    const styles = getInventoryItemCardStyles(
        theme,
        item,
        isSelected,
        isLoading,
        rarity
    );

    return (
        <motion.div
            className="inventoryCard"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            whileHover={{
                boxShadow: styles.hover.boxShadow,
                y: -4
            }}
            onClick={() => {
                soundSystem.play("click");
                toggleSelect(item);
            }}
            style={{
                ...styles.card,
                cursor: "pointer"
            }}
        >
            {/* LEFT SIDE */}
            <div style={styles.leftSection}>
                <div style={styles.content}>
                    <div style={styles.name}>
                        {isSelected ? "✓ " : ""}
                        {formatName(item.itemName)}
                    </div>

                    <div style={styles.description}>
                        {item.description || "No description available"}
                    </div>

                    <div style={styles.tags}>
                        <span style={styles.typeBadge}>
                            {formatName(item.itemType)}
                        </span>

                        <span style={styles.rarityBadge}>
                            {formatName(item.rarity)}
                        </span>
                    </div>
                </div>
            </div>

            {/* RIGHT SIDE */}
            <div style={styles.rightSection}>
                <div style={styles.quantity}>
                    x{item.quantity}
                </div>

                <div style={styles.price}>
                    💰 {item.price ?? 0}

                    <div style={styles.total}>
                        Total: {(item.price ?? 0) * item.quantity}
                    </div>
                </div>

                <div style={styles.buttons}>
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onSell(item.itemName, 1);
                        }}
                        disabled={isLoading}
                        style={styles.sellButton}
                    >
                        Sell
                    </button>

                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onSell(item.itemName, item.quantity);
                        }}
                        disabled={isLoading}
                        style={styles.sellAllButton}
                    >
                        Sell All
                    </button>
                </div>
            </div>
        </motion.div>
    );
}

export default InventoryItemCard;