import { motion } from "framer-motion";

import useGamePage from "./hooks/useGamePage";

import Login from "./components/Login";
import Shop from "./components/Shop/Shop";
import Inventory from "./components/inventory/Inventory";
import PlayerStats from "./components/playerstats/PlayerStats";
import Toasts from "./components/Toasts";
import Leaderboard from "./components/Leaderboard";
import Header from "./components/header/Header";
import CombatPanel from "./components/combatPanel";
import { QuestPanel } from "./components/QuestPanel";

import { getTheme } from "./theme";
import { page, fadeUp } from "./animations";

// =========================================================
// OUTSIDE COMPONENTS
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

        fightData,
        fightLoading,
        handleFight,
        clearFight,

        buyingItem,
        sellingItem,
        toasts,
        darkMode,
        toggleDarkMode,

        refreshGame
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
                    <>
                        {/* MAIN CONTENT (NO GRID) */}
                        <Section delay={0.1}>
                            <div style={{
                                display: "flex",
                                flexDirection: "column",
                                gap: "24px",
                                marginTop: "20px",
                                marginBottom: "20px"
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

                                <Section delay={0.22}>
                                    <QuestPanel theme={theme} refreshGame={refreshGame} />
                                </Section>

                            </div>
                        </Section>

                        {/* PLAYER STATS (MOVED DOWN = CLEAN UX) */}
                        <Section delay={0.12}>
                            <PlayerStats
                                playerStats={playerStats}
                                theme={theme}
                            />
                        </Section>

                        {/* COMBAT FULL WIDTH SECTION */}
                        <Section delay={0.18}>
                            <div style={{
                                width: "100%",
                                marginTop: "20px"
                            }}>
                                <CombatPanel
                                    theme={theme}
                                    fightData={fightData}
                                    fightLoading={fightLoading}
                                    handleFight={handleFight}
                                    clearFight={clearFight}
                                />
                            </div>
                        </Section>
                    </>
                )}
            </Layout>

            <Toasts toasts={toasts} />
        </motion.div>
    );
}

export default App;