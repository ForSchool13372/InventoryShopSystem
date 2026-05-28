import { useState } from "react";

function Inventory({ inventory, token, onSell }) {
    const [loadingItem, setLoadingItem] = useState(null);

    const handleSell = async (itemName) => {
        try {
            setLoadingItem(itemName);
            await onSell(itemName);
        } finally {
            setLoadingItem(null);
        }
    };

    return (
        <div style={{
            background: "#fff",
            padding: "20px",
            borderRadius: "14px",
            boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
            marginBottom: "20px",
            border: "1px solid rgba(0,0,0,0.05)"
        }}>
            <h2>Inventory</h2>

            {!token && (
                <p style={{ color: "#6b7280" }}>
                    Please login to view inventory
                </p>
            )}

            {token && inventory.length === 0 && (
                <p style={{ color: "#6b7280" }}>
                    No items in inventory
                </p>
            )}

            {inventory.map((item, i) => {
                const isLoading = loadingItem === item.itemName;

                return (
                    <div
                        key={i}
                        style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            padding: "12px",
                            border: "1px solid #eee",
                            borderRadius: "10px",
                            marginTop: "10px",
                            opacity: isLoading ? 0.6 : 1,
                            transition: "0.2s"
                        }}
                    >
                        <span style={{ fontWeight: "600" }}>
                            {item.itemName} x {item.quantity}
                        </span>

                        <button
                            onClick={() => handleSell(item.itemName)}
                            disabled={isLoading}
                            style={{
                                padding: "6px 12px",
                                borderRadius: "8px",
                                border: "none",
                                cursor: isLoading ? "not-allowed" : "pointer",
                                background: isLoading ? "#9ca3af" : "#ef4444",
                                color: "white",
                                fontWeight: "600",
                                transition: "0.2s"
                            }}
                        >
                            {isLoading ? "Selling..." : "Sell"}
                        </button>
                    </div>
                );
            })}
        </div>
    );
}

export default Inventory;