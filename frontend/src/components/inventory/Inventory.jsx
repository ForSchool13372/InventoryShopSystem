import { useState } from "react";
import { AnimatePresence } from "framer-motion";
import InventoryItemCard from "./InventoryItemCard";

function Inventory({ inventory, onSell, theme }) {
    const [loadingItem, setLoadingItem] = useState(null);
    const [search, setSearch] = useState("");
    const [selectedItems, setSelectedItems] = useState(new Set());

    const formatName = (name = "") =>
        name
            .replace(/_/g, " ")
            .split(" ")
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(" ");

    // STACK-SAFE SELECT
    const toggleSelect = (item) => {
        setSelectedItems(prev => {
            const next = new Set(prev);
            const key = `${item.itemName}:${item.quantity}`;

            if (next.has(key)) next.delete(key);
            else next.add(key);

            return next;
        });
    };

    const clearSelection = () => {
        setSelectedItems(new Set());
    };

    const handleSell = async (itemName, quantity = 1) => {
        try {
            setLoadingItem(itemName);
            const safeQty = Math.max(1, quantity);
            await onSell(itemName, safeQty);
        } finally {
            setLoadingItem(null);
        }
    };

    const sellSelected = async (items) => {
        for (const item of items) {
            const key = `${item.itemName}:${item.quantity}`;

            if (selectedItems.has(key)) {
                await handleSell(item.itemName, item.quantity);
            }
        }
        clearSelection();
    };

    const normalizedInventory = inventory.map(item => ({
        itemName: item.itemName ?? item.itemname,
        quantity: item.quantity ?? 0,
        itemType: item.itemType ?? item.itemtype,
        rarity: item.rarity,
        description: item.description,
        price: item.price
    }));

    const filteredInventory = normalizedInventory.filter(item =>
        item.itemName?.toLowerCase().includes(search.toLowerCase())
    );

    const selectAll = () => {
        const next = new Set();

        filteredInventory.forEach(item => {
            next.add(`${item.itemName}:${item.quantity}`);
        });

        setSelectedItems(next);
    };

    const cardStyle = {
        background: theme.cardBg,
        color: theme.text,
        padding: "20px",
        borderRadius: "18px",
        boxShadow: "0 12px 35px rgba(0,0,0,0.08)",
        border: "1px solid rgba(0,0,0,0.05)"
    };

    const buttonBase = {
        padding: "8px 12px",
        borderRadius: "10px",
        border: "none",
        fontWeight: "600",
        cursor: "pointer"
    };

    return (
        <div style={cardStyle}>
            <h2 style={{ color: theme.text, fontWeight: 800 }}>
                Inventory
            </h2>

            {/* SEARCH */}
            <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search items..."
                style={{
                    width: "90%",
                    padding: "10px",
                    borderRadius: "10px",
                    marginBottom: "12px",
                    border: `1px solid ${theme.subText}33`,
                    background: theme.cardBg,
                    color: theme.text
                }}
            />

            {/* GLOBAL ACTIONS */}
            <div style={{ display: "flex", gap: "8px", marginBottom: "12px" }}>
                <button
                    onClick={selectAll}
                    style={{ ...buttonBase, background: "#374151", color: "white" }}
                >
                    Select All
                </button>

                <button
                    onClick={clearSelection}
                    style={{ ...buttonBase, background: "#6b7280", color: "white" }}
                >
                    Clear
                </button>

                <button
                    onClick={() => sellSelected(filteredInventory)}
                    disabled={selectedItems.size === 0}
                    style={{ ...buttonBase, background: "#ef4444", color: "white" }}
                >
                    Sell Selected
                </button>
            </div>

            {/* GRID */}
            <div style={{ display: "grid", gap: "10px" }}>
                <AnimatePresence>
                    {filteredInventory.map((item) => (
                        <InventoryItemCard
                            key={item.itemName + item.quantity}
                            item={item}
                            theme={theme}
                            formatName={formatName}
                            onSell={handleSell}
                            isLoading={loadingItem === item.itemName}
                            isSelected={selectedItems.has(`${item.itemName}:${item.quantity}`)}
                            toggleSelect={toggleSelect}
                        />
                    ))}
                </AnimatePresence>
            </div>

            {filteredInventory.length === 0 && (
                <p style={{ color: theme.subText, padding: "10px 0" }}>
                    🎒 No matching items found
                </p>
            )}
        </div>
    );
}

export default Inventory;