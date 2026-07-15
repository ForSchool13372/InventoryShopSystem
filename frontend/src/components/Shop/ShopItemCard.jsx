import { motion } from "framer-motion";
import { getShopItemCardStyles } from "./shopItemCardStyles";

function ShopItemCard({ item, theme, addToCart, formatName }) {
    const rarityGlow =
        item.rarity === "common"
            ? "rgba(34,197,94,0.35)"
            : item.rarity === "trash"
                ? "rgba(156,163,175,0.35)"
                : "rgba(251,191,36,0.40)";

    const styles = getShopItemCardStyles(theme, item, rarityGlow);
        
    const rarityColor =
        item.rarity === "common"
            ? "#22c55e"
            : item.rarity === "trash"
                ? "#9ca3af"
                : "#fbbf24";

    return (
        <motion.div
            key={`${item?.itemName ?? "item"}-${item.price ?? 0}`}
            whileHover={styles.hover}
            transition={{
                type: "spring",
                stiffness: 300,
                damping: 22
            }}
            onClick={() => addToCart(item)}
            style={styles.card}
        >

            <div style={styles.header}>

                <div style={styles.titleContainer}>
                    <div style={styles.title}>
                        {formatName(item.itemName)}
                    </div>

                    <div style={styles.description}>
                        {item.description || "No description available"}
                    </div>
                </div>


                <div style={styles.price}>
                    💰 {item.price}
                </div>

            </div>


            <div style={styles.bottomBar}>

                <div style={styles.badges}>

                    <span style={styles.typeBadge}>
                        {item.itemType}
                    </span>


                    <span
                        style={{
                            ...styles.rarityBadge,
                            color: rarityColor
                        }}
                    >
                        {item.rarity}
                    </span>


                    <span style={styles.stockBadge}>
                        Stock: {item.stock}
                    </span>

                </div>


                <span style={styles.availability}>
                    {item.stock > 0
                        ? "Available"
                        : "Out of stock"}
                </span>

            </div>

        </motion.div>
    );
}

export default ShopItemCard;