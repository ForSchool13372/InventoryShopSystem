import { motion } from "framer-motion";

import useGamePage from "./hooks/useGamePage";

import Login from "./components/Login";
import Shop from "./components/Shop";
import Inventory from "./components/Inventory";
import PlayerStats from "./components/PlayerStats";
import Toasts from "./components/Toasts";
import Leaderboard from "./components/Leaderboard";
import Header from "./components/Header";

import { getTheme } from "./theme";
import { page, fadeUp } from "./animations";

// =========================================================
// OUTSIDE COMPONENTS (FIX FOR YOUR ERROR)
// =========================================================
const Layout = ({ children }) => (
    <div style={{
        width: "100%",
        maxWidth: "1920px",
        margin: "0 auto",
        zIndex: 2
    }}>
        {children}
    </div>
);

const Section = ({ children, delay = 0 }) => (
    <motion.div
        variants={fadeUp(delay)}
        initial="hidden"
        animate="show"
    >
        {children}
    </motion.div>
);

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

            <Layout>
                <Header
                    token={token}
                    playerId={playerId}
                    darkMode={darkMode}
                    toggleDarkMode={toggleDarkMode}
                    theme={theme}
                />

                {loading && (
                    <Section delay={0.02}>
                        <p style={{ color: theme.subText }}>
                            Loading world...
                        </p>
                    </Section>
                )}

                <Section delay={0.05}>
                    <Login
                        token={token}
                        onLogin={handleLogin}
                        onLogout={handleLogout}
                        theme={theme}
                    />
                </Section>

                {token && (
                    <Section delay={0.1}>
                        <div style={{
                            display: "grid",
                            gridTemplateColumns: "3fr 1.2fr",
                            gap: "24px",
                            marginTop: "20px",
                            marginBottom: "20px",
                            alignItems: "start"
                        }}>
                            <div style={{
                                display: "flex",
                                flexDirection: "column",
                                gap: "24px"
                            }}>
                                <Section delay={0.1}>
                                    <Shop
                                        items={items}
                                        token={token}
                                        onBuy={handleBuy}
                                        theme={theme}
                                        buyingItem={buyingItem}
                                        playerStats={playerStats}
                                    />
                                </Section>

                                <Section delay={0.15}>
                                    <Inventory
                                        inventory={inventory}
                                        token={token}
                                        onSell={handleSell}
                                        theme={theme}
                                        sellingItem={sellingItem}
                                    />
                                </Section>

                                <Section delay={0.2}>
                                    <Leaderboard
                                        theme={theme}
                                        token={token}
                                    />
                                </Section>
                            </div>

                            <Section delay={0.12}>
                                <PlayerStats
                                    playerStats={playerStats}
                                    theme={theme}
                                />
                            </Section>
                        </div>
                    </Section>
                )}
            </Layout>

            <Toasts toasts={toasts} />
        </motion.div>
    );
}

export default App;