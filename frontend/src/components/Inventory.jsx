import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

function Inventory({ inventory, onSell, theme }) {
    const [loadingItem, setLoadingItem] = useState(null);
    const [selectedItems, setSelectedItems] = useState(new Set());
    const [search, setSearch] = useState("");

    const formatName = (name = "") =>
        name
            .replace(/_/g, " ")
            .split(" ")
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(" ");

    const toggleSelect = (itemName) => {
        setSelectedItems(prev => {
            const next = new Set(prev);
            if (next.has(itemName)) next.delete(itemName);
            else next.add(itemName);
            return next;
        });
    };

    const selectAll = () => {
        setSelectedItems(new Set(filteredInventory.map(i => i.itemName)));
    };

    const clearSelection = () => {
        setSelectedItems(new Set());
    };

    const handleSell = async (itemName, quantity) => {
        try {
            setLoadingItem(itemName);
            await onSell(itemName, quantity);
        } finally {
            setLoadingItem(null);
        }
    };

    const sellSelected = async () => {
        for (const item of filteredInventory) {
            if (selectedItems.has(item.itemName)) {
                await handleSell(item.itemName, item.quantity);
            }
        }
        clearSelection();
    };

    const sellAllInventory = async () => {
        for (const item of filteredInventory) {
            await handleSell(item.itemName, item.quantity);
        }
        clearSelection();
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

    const mutedText = {
        color: theme.subText,
        padding: "10px 0"
    };

    const normalizedInventory = inventory.map(item => ({
        itemName: item.itemName ?? item.itemname,
        quantity: item.quantity ?? 0
    }));

    const filteredInventory = normalizedInventory.filter(item => {
        return item.itemName?.toLowerCase().includes(search.toLowerCase());
    });

    return (
        <div style={cardStyle}>
            <h2 style={{
                color: theme.text,
                fontWeight: 800,
                marginBottom: "10px",
            }}>
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
                    style={{ ...buttonBase, background: "#111827", color: "white" }}
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
                    onClick={sellSelected}
                    disabled={selectedItems.size === 0}
                    style={{ ...buttonBase, background: "#ef4444", color: "white" }}
                >
                    Sell Selected
                </button>

                <button
                    onClick={sellAllInventory}
                    style={{ ...buttonBase, background: "#dc2626", color: "white" }}
                >
                    Sell All
                </button>
            </div>

            {filteredInventory.length === 0 && (
                <p style={mutedText}>🎒 No matching items found</p>
            )}

            {/* GRID */}
            <div style={{ display: "grid", gap: "10px" }}>
                <AnimatePresence>
                    {filteredInventory.map(item => {
                        const isSelected = selectedItems.has(item.itemName);
                        const isLoading = loadingItem === item.itemName;

                        return (
                            <motion.div
                                key={item.itemName}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0 }}
                                style={{
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "space-between",
                                    padding: "12px",
                                    borderRadius: "12px",
                                    border: `1px solid ${theme.subText}33`,
                                    background: isSelected
                                        ? theme.subText + "15"
                                        : theme.cardBg,
                                    opacity: isLoading ? 0.5 : 1
                                }}
                            >
                                {/* LEFT */}
                                <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
                                    <input
                                        type="checkbox"
                                        checked={isSelected}
                                        onChange={() => toggleSelect(item.itemName)}
                                    />

                                    <div style={{ fontWeight: "700" }}>
                                        {formatName(item.itemName)}
                                    </div>
                                </div>

                                {/* RIGHT */}
                                <div style={{ fontWeight: "600", color: theme.subText }}>
                                    x{item.quantity}
                                </div>
                            </motion.div>
                        );
                    })}
                </AnimatePresence>
            </div>
        </div>
    );
}

export default Inventory;