import { motion } from "framer-motion";
import { useMemo } from "react";
import Progression from "./Progression";
import Combat from "./Combat";
import Core from "./Core";
import { playerStatsStyles as styles } from "./styles";

function PlayerStats({ playerStats, theme }) {
    const playerGold = playerStats?.core?.gold ?? 0;

    const { core, progression, combat } = useMemo(() => {
        return {
            core: playerStats?.core ?? {},
            progression: playerStats?.progression ?? {},
            combat: playerStats?.combat ?? {}
        };
    }, [playerStats]);

    if (!playerStats) {
        return (
            <div style={styles.card(theme)}>
                <h2 style={styles.title(theme)}>🧍 PLAYER</h2>
                <p style={{ color: theme.subText, fontWeight: 700 }}>
                    No player data loaded
                </p>
            </div>
        );
    }

    return (
        <motion.div
            style={styles.card(theme)}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, ease: "easeOut" }}
        >
            {/* HEADER (HUD STYLE) */}
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "14px",
                    paddingBottom: "8px",
                    borderBottom: "1px solid rgba(255,255,255,0.06)"
                }}
            >
                <h2 style={styles.title(theme)}>
                    PLAYER STATS
                </h2>

                <div style={styles.goldPill(theme)}>
                    💰 {playerGold}
                </div>
            </div>

            {/* CORE */}
            <Core core={core} progression={progression} theme={theme} />

            {/* COMBAT */}
            <div style={{ marginTop: "8px" }}>
                <Combat combat={combat} theme={theme} />
            </div>

            {/* PROGRESSION */}
            <div style={{ marginTop: "8px" }}>
                <Progression progression={progression} theme={theme} />
            </div>
        </motion.div>
    );
}

export default PlayerStats;
