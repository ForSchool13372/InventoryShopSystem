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

// Components
import Login from "./components/Login";
import Shop from "./components/Shop";
import Inventory from "./components/Inventory";
import PlayerStats from "./components/PlayerStats";

function App() {
    const { token, playerId, login, logout } = useAuth();

    const [items, setItems] = useState([]);
    const [inventory, setInventory] = useState([]);
    const [playerStats, setPlayerStats] = useState(null);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);

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
        const timer = setTimeout(() => setError(""), 1500);
        return () => clearTimeout(timer);
    }, [error]);

    // ----------------------------
    // AUTH
    // ----------------------------

    const handleLogin = async (id) => {
        if (!id) return;

        try {
            setError("");

            const data = await loginPlayer(id);
            const jwt = data.data.token;

            login(jwt, id);

            await refreshAll();
        } catch (err) {
            setError(err.message);
        }
    };

    const handleLogout = () => {
        logout();
        setItems([]);
        setInventory([]);
        setPlayerStats(null);
        setError("");
    };

    // ----------------------------
    // GAME ACTIONS
    // ----------------------------

    const handleBuy = async (itemName) => {
        try {
            await buyItem(playerId, token, itemName, 1);
            await refreshAll();
        } catch (err) {
            setError(err.message);
        }
    };

    const handleSell = async (itemName) => {
        try {
            await sellItem(playerId, token, itemName, 1);
            await refreshAll();
        } catch (err) {
            setError(err.message);
        }
    };

    // ----------------------------
    // UI COMPOSITION (CLEAN)
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
            <div style={{
                width: "100%",
                maxWidth: "900px",
                display: "flex",
                flexDirection: "column",
                gap: "20px"
            }}>

                <h1 style={{
                    textAlign: "center",
                    color: "#111827",
                    fontSize: "2.2rem",
                    fontWeight: "800"
                }}>
                    Inventory Shop System
                </h1>

                {loading && (
                    <p style={{ textAlign: "center" }}>
                        Loading game world...
                    </p>
                )}

                {error && (
                    <p style={{ color: "red", textAlign: "center" }}>
                        {error}
                    </p>
                )}

                {/* COMPONENTS */}
                <Login
                    token={token}
                    onLogin={handleLogin}
                    onLogout={handleLogout}
                    error={error}
                    playerStats={playerStats}
                />

                <Shop
                    items={items}
                    token={token}
                    onBuy={handleBuy}
                />

                <PlayerStats playerStats={playerStats} />

                <Inventory
                    inventory={inventory}
                    token={token}
                    onSell={handleSell}
                />

            </div>
        </div>
    );
}

export default App;