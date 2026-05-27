import { useEffect, useState, useCallback } from "react";
import { useAuth } from "./useAuth";

import {
    getShop,
    buyItem,
    sellItem,
    getInventory,
    getPlayer,
    loginPlayer
} from "./apiClient";

function App() {
    const { token, playerId, login, logout } = useAuth();

    const [items, setItems] = useState([]);
    const [inventory, setInventory] = useState([]);
    const [playerStats, setPlayerStats] = useState(null);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);
    const [inputPlayerId, setInputPlayerId] = useState("");

    // ----------------------------
    // STYLES (clean system)
    // ----------------------------
    const cardStyle = {
        background: "#fff",
        padding: "20px",
        borderRadius: "14px",
        boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
        marginBottom: "20px",
        border: "1px solid rgba(0,0,0,0.05)"
    };

    const buttonStyle = {
        padding: "8px 12px",
        borderRadius: "8px",
        border: "none",
        cursor: "pointer",
        fontWeight: "600",
        transition: "0.2s"
    };

    // ----------------------------
    // API LOADERS
    // ----------------------------

    const loadShop = useCallback(async () => {
        const data = await getShop();
        setItems(data.data);
    }, []);

    const loadInventory = useCallback(async () => {
        if (!token || !playerId) return;

        const data = await getInventory(playerId, token);
        setInventory(data.data.items);
    }, [token, playerId]);

    const loadPlayerStats = useCallback(async () => {
        if (!token || !playerId) return;

        const data = await getPlayer(playerId, token);
        setPlayerStats(data.data);
    }, [token, playerId]);

    const refreshAll = useCallback(async () => {
        await loadShop();
        await loadInventory();
        await loadPlayerStats();
    }, [loadShop, loadInventory, loadPlayerStats]);

    // ----------------------------
    // INIT
    // ----------------------------
    useEffect(() => {
        const init = async () => {
            try {
                setLoading(true);
                await refreshAll();
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        init();
    }, [refreshAll]);

    // ----------------------------
    // AUTO CLEAR ERROR
    // ----------------------------
    useEffect(() => {
        if (!error) return;
        const timer = setTimeout(() => setError(""), 3000);
        return () => clearTimeout(timer);
    }, [error]);

    // ----------------------------
    // LOGIN
    // ----------------------------
    const handleLogin = async (id) => {
        if (!id) return;

        try {
            setError("");

            const data = await loginPlayer(id);
            const jwt = data.data.token;

            login(jwt, id);
            setInputPlayerId("");

            await refreshAll();
        } catch (err) {
            setError(err.message);
        }
    };

    // ----------------------------
    // LOGOUT
    // ----------------------------
    const handleLogout = () => {
        logout();
        setItems([]);
        setInventory([]);
        setPlayerStats(null);
        setError("");
    };

    // ----------------------------
    // BUY
    // ----------------------------
    const handleBuy = async (itemName) => {
        try {
            await buyItem(playerId, token, itemName, 1);
            await refreshAll();
        } catch (err) {
            setError(err.message);
        }
    };

    // ----------------------------
    // SELL
    // ----------------------------
    const handleSell = async (itemName) => {
        try {
            await sellItem(playerId, token, itemName, 1);
            await refreshAll();
        } catch (err) {
            setError(err.message);
        }
    };

    // ----------------------------
    // UI
    // ----------------------------
    return (
        <div style={{
            padding: "20px",
            minHeight: "100vh",
            background: "linear-gradient(180deg, #f5f7fb, #e9eef7)",
            fontFamily: "Arial",
            display: "flex",
            justifyContent: "center"
        }}>

            <div style={{ width: "100%", maxWidth: "900px" }}>

                <h1 style={{
                    textAlign: "center",
                    color: "#111827",
                    marginBottom: "25px",
                    fontSize: "2.2rem",
                    fontWeight: "800"
                }}>
                    Inventory Shop System
                </h1>

                {loading && <p>Loading game world...</p>}

                {/* LOGIN */}
                <div style={cardStyle}>
                    <h2>Login</h2>

                    {!token ? (
                        <>
                            <input
                                placeholder="Player ID"
                                value={inputPlayerId}
                                onChange={(e) => setInputPlayerId(e.target.value)}
                                style={{
                                    padding: "8px",
                                    borderRadius: "8px",
                                    border: "1px solid #ddd",
                                    marginRight: "10px"
                                }}
                            />

                            <button
                                onClick={() => handleLogin(inputPlayerId)}
                                style={{
                                    ...buttonStyle,
                                    background: "#4f46e5",
                                    color: "white"
                                }}
                            >
                                Login
                            </button>
                        </>
                    ) : (
                        <>
                            <p>Logged in ✔</p>

                            <button
                                onClick={handleLogout}
                                style={{
                                    ...buttonStyle,
                                    background: "#ef4444",
                                    color: "white"
                                }}
                            >
                                Logout
                            </button>
                        </>
                    )}

                    {error && (
                        <p style={{ color: "red", marginTop: "10px" }}>
                            {error}
                        </p>
                    )}

                    {playerStats && (
                        <div>
                            <p>Gold: {playerStats.gold}</p>
                            <p>HP: {playerStats.hp}</p>
                            <p>Level: {playerStats.level}</p>
                        </div>
                    )}
                </div>

                {/* SHOP */}
                <div style={cardStyle}>
                    <h2>Shop</h2>

                    {items.length === 0 && <p>No items available</p>}

                    {items.map((item, i) => (
                        <div key={i} style={{
                            display: "flex",
                            justifyContent: "space-between",
                            padding: "8px 0"
                        }}>
                            <span>{item.itemName} - {item.stock}</span>

                            {token && (
                                <button
                                    onClick={() => handleBuy(item.itemName)}
                                    style={{
                                        ...buttonStyle,
                                        background: "#4f46e5",
                                        color: "white"
                                    }}
                                >
                                    Buy
                                </button>
                            )}
                        </div>
                    ))}
                </div>

                {/* INVENTORY */}
                {token && (
                    <div style={cardStyle}>
                        <h2>Inventory</h2>

                        {inventory.length === 0 && <p>No items in inventory</p>}

                        {inventory.map((item, i) => (
                            <div key={i} style={{
                                display: "flex",
                                justifyContent: "space-between",
                                padding: "8px 0"
                            }}>
                                <span>{item.itemName} x {item.quantity}</span>

                                <button
                                    onClick={() => handleSell(item.itemName)}
                                    style={{
                                        ...buttonStyle,
                                        background: "#ef4444",
                                        color: "white"
                                    }}
                                >
                                    Sell
                                </button>
                            </div>
                        ))}
                    </div>
                )}

            </div>
        </div>
    );
}

export default App;