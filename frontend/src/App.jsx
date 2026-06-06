import { useEffect, useState } from "react";
import { useAuth } from "./useAuth";
import { motion, AnimatePresence } from "framer-motion";
import soundSystem from "./utils/soundSystem";

import {
    setAuthToken,
    loginPlayer,
    getInventory,
    getPlayer,
    buyItem,
    sellItem,
    getShop
} from "./apiClient";

import Login from "./components/Login";
import Shop from "./components/Shop";
import Inventory from "./components/Inventory";
import PlayerStats from "./components/PlayerStats";

function App() {
    const { token, playerId, login, logout } = useAuth();

    const [items, setItems] = useState([]);
    const [inventory, setInventory] = useState([]);
    const [playerStats, setPlayerStats] = useState(null);
    const [loading, setLoading] = useState(true);

    const [toasts, setToasts] = useState([]);
    const [darkMode, setDarkMode] = useState(false);

    const [buyingItem, setBuyingItem] = useState(null);
    const [sellingItem, setSellingItem] = useState(null);

    // ----------------------------
    // THEME
    // ----------------------------
    const theme = {
        background: darkMode ? "#0b1220" : "#f4f7ff",
        cardBg: darkMode ? "#111a2e" : "#ffffff",
        text: darkMode ? "#e5e7eb" : "#111827",
        subText: darkMode ? "#94a3b8" : "#6b7280"
    };

    const toggleDarkMode = () => setDarkMode(prev => !prev);

    // ----------------------------
    // TOASTS
    // ----------------------------
    const addToast = (message, type = "info") => {
        const id = Date.now();

        setToasts(prev => [...prev, { id, message, type }]);

        setTimeout(() => {
            setToasts(prev => prev.filter(t => t.id !== id));
        }, 2200);
    };

    // ----------------------------
    // LOADERS (CLEAN)
    // ----------------------------

    const loadShop = async () => {
        const data = await getShop();
        setItems(data?.data ?? []);
    };

    const loadInventory = async () => {
        if (!token || !playerId) return;

        const data = await getInventory();
        setInventory(data?.items ?? []);
    };

    const loadPlayerStats = async () => {
        if (!token || !playerId) return;

        const data = await getPlayer();
        setPlayerStats(data ?? null);
    };

    // ----------------------------
    // REFRESH ALL (CLEAN)
    // ----------------------------

    const refreshAll = async () => {
        if (!token || !playerId) return;

        await Promise.all([
            loadShop(),
            loadInventory(),
            loadPlayerStats()
        ]);
    };

    // ----------------------------
    // INIT EFFECT (FIXED)
    // ----------------------------
    useEffect(() => {
        if (!token) return;

        const syncData = async () => {
            setLoading(true);
            try {
                const [shop, inventory, player] = await Promise.all([
                    getShop(),
                    getInventory(),
                    getPlayer()
                ]);

                console.log("shop", shop);
                console.log("inventory", inventory);
                console.log("player", player);

                setItems(shop?.data ?? []);
                setInventory(inventory?.items ?? []);
                setPlayerStats(player ?? null);
            } finally {
                setLoading(false);
            }
        };

        syncData();
    }, [token]);

    // ----------------------------
    // AUTH
    // ----------------------------
    const handleLogin = async (id) => {
        try {
            if (!id) throw new Error("Missing ID");

            const res = await loginPlayer(id);

            const newToken = res?.token || res?.data?.token;

            if (!newToken) {
                throw new Error("No token returned from server");
            }

            setAuthToken(newToken);
            login(newToken, id);

            soundSystem.play("success");
            addToast("Welcome back", "success");

            return true;

        } catch (err) {
            soundSystem.play("error");
            addToast(err?.message || "Invalid ID", "error");
            return false;
        }
    };

    const handleLogout = () => {
        logout();

        setItems([]);
        setInventory([]);
        setPlayerStats(null);

        soundSystem.play("click");
        addToast("Logged out", "info");
    };

    // ----------------------------
    // GAME ACTIONS
    // ----------------------------
    const handleBuy = async (itemName) => {
        setBuyingItem(itemName);

        try {
            await buyItem(itemName, 1);
            await refreshAll();

            soundSystem.play("buy");
            addToast(`Bought ${itemName}`, "success");

        } catch (err) {
            soundSystem.play("error");
            addToast(err?.message || "Buy failed", "error");

        } finally {
            setTimeout(() => setBuyingItem(null), 150);
        }
    };

    const handleSell = async (itemName) => {
        setSellingItem(itemName);

        try {
            await sellItem(itemName, 1);
            await refreshAll();

            soundSystem.play("sell");
            addToast(`Sold ${itemName}`, "success");

        } catch (err) {
            soundSystem.play("error");
            addToast(err?.message || "Sell failed", "error");

        } finally {
            setTimeout(() => setSellingItem(null), 150);
        }
    };

    // ----------------------------
    // ANIMATIONS
    // ----------------------------
    const page = {
        hidden: { opacity: 0, y: 12 },
        show: { opacity: 1, y: 0, transition: { duration: 0.35 } }
    };

    const fadeUp = (delay = 0) => ({
        hidden: { opacity: 0, y: 10 },
        show: { opacity: 1, y: 0, transition: { delay, duration: 0.3 } }
    });

    return (
        <motion.div
            variants={page}
            initial="hidden"
            animate="show"
            style={{
                minHeight: "100vh",
                padding: "32px",
                display: "flex",
                justifyContent: "center",
                fontFamily: "Arial",
                background: theme.background,
                color: theme.text,
                position: "relative",
                overflow: "hidden"
            }}
        >
            {/* glow */}
            <div style={{
                position: "absolute",
                width: "700px",
                height: "700px",
                background: "rgba(99,102,241,0.12)",
                filter: "blur(140px)",
                top: "-250px",
                left: "-250px",
                borderRadius: "50%"
            }} />

            <div style={{ width: "100%", maxWidth: "1100px", zIndex: 2 }}>

                {/* HEADER */}
                <motion.div
                    variants={fadeUp(0)}
                    initial="hidden"
                    animate="show"
                    style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        marginBottom: "24px"
                    }}
                >
                    <div>
                        <h1 style={{ fontSize: "2rem", fontWeight: "800", margin: 0 }}>
                            Inventory Shop System
                        </h1>

                        <p style={{ margin: "4px 0 0 0", fontSize: "0.9rem", color: theme.subText }}>
                            {token ? `Logged in as ${playerId}` : "Start your journey today!"}
                        </p>
                    </div>

                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={toggleDarkMode}
                        style={{
                            padding: "8px 12px",
                            borderRadius: "10px",
                            border: "none",
                            cursor: "pointer",
                            background: darkMode ? "#e5e7eb" : "#111827",
                            color: darkMode ? "#111827" : "#fff",
                            fontWeight: "600"
                        }}
                    >
                        {darkMode ? "Light ☀️" : "Dark 🌙"}
                    </motion.button>
                </motion.div>

                {loading && (
                    <motion.p style={{ color: theme.subText }}>
                        Loading world...
                    </motion.p>
                )}

                {/* LOGIN */}
                <motion.div variants={fadeUp(0.05)} initial="hidden" animate="show">
                    <Login
                        token={token}
                        onLogin={handleLogin}
                        onLogout={handleLogout}
                        theme={theme}
                    />
                </motion.div>

                {/* GRID */}
                <div style={{
                    display: "grid",
                    gridTemplateColumns: "2fr 1fr",
                    gap: "20px",
                    marginTop: "18px",
                    marginBottom: "20px"
                }}>
                    <motion.div variants={fadeUp(0.1)} initial="hidden" animate="show">
                        <Shop
                            items={items}
                            token={token}
                            onBuy={handleBuy}
                            theme={theme}
                            buyingItem={buyingItem}
                        />
                    </motion.div>

                    <motion.div variants={fadeUp(0.15)} initial="hidden" animate="show">
                        <PlayerStats
                            playerStats={playerStats}
                            theme={theme}
                        />
                    </motion.div>
                </div>

                <motion.div variants={fadeUp(0.2)} initial="hidden" animate="show">
                    <Inventory
                        inventory={inventory}
                        token={token}
                        onSell={handleSell}
                        theme={theme}
                        sellingItem={sellingItem}
                    />
                </motion.div>
            </div>

            {/* TOASTS */}
            <div style={{
                position: "fixed",
                top: "20px",
                right: "20px",
                display: "flex",
                flexDirection: "column",
                gap: "10px",
                zIndex: 9999
            }}>
                <AnimatePresence>
                    {toasts.map((toast) => (
                        <motion.div
                            key={toast.id}
                            initial={{ opacity: 0, x: 20, scale: 0.95 }}
                            animate={{ opacity: 1, x: 0, scale: 1 }}
                            exit={{ opacity: 0, x: 20, scale: 0.95 }}
                            style={{
                                padding: "10px 14px",
                                borderRadius: "12px",
                                color: "white",
                                fontWeight: "600",
                                background:
                                    toast.type === "success"
                                        ? "#22c55e"
                                        : toast.type === "error"
                                            ? "#ef4444"
                                            : "#4f46e5",
                                boxShadow: "0 10px 25px rgba(0,0,0,0.25)"
                            }}
                        >
                            {toast.message}
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>
        </motion.div>
    );
}

export default App;