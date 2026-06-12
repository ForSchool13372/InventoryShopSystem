// =========================================================
// REACT CORE / LIBRARIES
// =========================================================
import { motion } from "framer-motion";

// =========================================================
// MAIN HOOK
// =========================================================
import useGamePage from "./hooks/useGamePage";

// =========================================================
// COMPONENTS
// =========================================================
import Login from "./components/Login";
import Shop from "./components/Shop";
import Inventory from "./components/Inventory";
import PlayerStats from "./components/PlayerStats";
import Toasts from "./components/Toasts";
import Leaderboard from "./components/Leaderboard";
import Header from "./components/Header";

// =========================================================
// UTILITIES / CONFIG
// =========================================================
import { getTheme } from "./theme";
import { page, fadeUp } from "./animations";
function App() {
    const {
        token,
        playerId,
        handleLogin,
        handleLogout,
        items,
        inventory,
        playerStats,
        loading,
        handleBuy,
        handleSell,
        buyingItem,
        sellingItem,
        toasts,
        darkMode,
        toggleDarkMode
    } = useGamePage();

    const theme = getTheme(darkMode);

    return (
        <motion.div
            variants={page}
            initial="hidden"
            animate="show"
            style={{
                minHeight: "100vh",
                width: "100%",
                padding: "64px",
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
            <div
                style={{
                    position: "absolute",
                    width: "900px",
                    height: "900px",
                    background: "rgba(99,102,241,0.12)",
                    filter: "blur(160px)",
                    top: "-300px",
                    left: "-300px",
                    borderRadius: "50%",
                }}
            />

            {/* MAIN CONTAINER (FULL WIDTH CONTROL) */}
            <div
                style={{
                    width: "100%",
                    maxWidth: "1920px",
                    margin: "0 auto",
                    zIndex: 2
                }}
            >
                {/* HEADER */}
                <Header
                    token={token}
                    playerId={playerId}
                    darkMode={darkMode}
                    toggleDarkMode={toggleDarkMode}
                    theme={theme}
                />

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

                {/* GRID (WIDER + CLEAN DASHBOARD FEEL) */}
                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns: "3fr 1.2fr",
                        gap: "24px",
                        marginTop: "20px",
                        marginBottom: "20px",
                        width: "100%"
                    }}
                >
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
                        <PlayerStats playerStats={playerStats} theme={theme} />
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

                <motion.div variants={fadeUp(0.25)} initial="hidden" animate="show">
                    <Leaderboard theme={theme} token={token} />
                </motion.div>

            </div>

            {/* TOASTS */}
            <Toasts toasts={toasts} />
        </motion.div>
    );
}

export default App;