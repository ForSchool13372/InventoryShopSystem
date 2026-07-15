import { useState, useCallback, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ShopCart from "./ShopCart";
import ShopItemCard from "./ShopItemCard";
import ShopControls from "./ShopControls";

import { getCardStyle } from "../../styles/uiStyles";

function Shop({ items, token, onBuy, theme, playerStats }) {
    const [loadingItem, setLoadingItem] = useState(null);
    const [purchasedItem, setPurchasedItem] = useState(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [cart, setCart] = useState({});

    const playerGold = playerStats?.core?.gold ?? 0;

    const formatName = (name = "") => {
        if (!name) return "";
        return name.charAt(0).toUpperCase() + name.slice(1);
    };

    const setQty = useCallback((itemName, value, maxStock) => {
        setCart((prev) => {
            const current = prev[itemName];
            if (!current) return prev;

            if (value === 0) {
                const updated = { ...prev };
                delete updated[itemName];
                return updated;
            }

            const newQty = Math.max(1, Math.min(value, maxStock));

            return {
                ...prev,
                [itemName]: { ...current, qty: newQty }
            };
        });
    }, []);

    const addToCart = (item) => {
        if (item.stock === 0) return;

        setCart((prev) => ({
            ...prev,
            [item.itemName]: {
                item,
                qty: prev[item.itemName]?.qty || 1
            }
        }));
    };

    const totalCartCost = useMemo(() => {
        return Object.values(cart).reduce(
            (sum, entry) => sum + (entry.item.price ?? 0) * entry.qty,
            0
        );
    }, [cart]);

    const cartHasItems = Object.keys(cart).length > 0;
    const canAfford = cartHasItems && playerGold >= totalCartCost;

    const filteredItems = useMemo(() => {
        return (items ?? []).filter((item) =>
            (item?.itemName ?? "")
                .toLowerCase()
                .includes(searchQuery.toLowerCase())
        );
    }, [items, searchQuery]);

    const handleBuy = async () => {
        if (!token || !cartHasItems || !canAfford) return;

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

    const cardStyle = getCardStyle(theme);

    return (
        <motion.div
            style={cardStyle}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
        >
            {/* LEFT */}
            <div style={{ flex: 2 }}>
                <h2 style={{ fontWeight: 800, color: theme.text, fontSize: "1.4rem" }}>
                    🛒 Shop
                </h2>

                <ShopControls
                    searchQuery={searchQuery}
                    setSearchQuery={setSearchQuery}
                    theme={theme}
                />

                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
                        gap: "12px",

                        maxHeight: "70vh",
                        overflowY: "auto",

                        paddingTop: "20px",
                        paddingBottom: "30px",
                        paddingLeft: "10px",
                        paddingRight: "10px",

                        scrollPaddingTop: "20px"
                    }}
                >
                    {filteredItems.map((item) => (
                        <ShopItemCard
                            key={`${item?.itemName ?? "item"}-${item.price ?? 0}`}
                            item={item}
                            theme={theme}
                            addToCart={addToCart}
                            formatName={formatName}
                        />
                    ))}
                </div>
            </div>

            {/* RIGHT */}
            <ShopCart
                cart={cart}
                setQty={setQty}
                handleBuy={handleBuy}
                playerGold={playerGold}
                theme={theme}
                token={token}
                loadingItem={loadingItem}
                canAfford={canAfford}
            />

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
                            fontWeight: 800
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