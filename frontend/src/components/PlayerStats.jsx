import { motion, AnimatePresence } from "framer-motion";
import { useMemo } from "react";

function PlayerStats({ playerStats, theme }) {
    const playerGold = playerStats?.core?.gold ?? 0;

    const { core, progression, combat } = useMemo(() => {
        return {
            core: playerStats?.core ?? {},
            progression: playerStats?.progression ?? {},
            combat: playerStats?.combat ?? {}
        };
    }, [playerStats]);

    const xp = progression.xp ?? 0;
    const level = progression.level ?? 1;
    const xpNeeded = Math.floor(100 * Math.pow(1.15, level - 1));
    const xpPercent = Math.min(100, (xp / xpNeeded) * 100);
    const isMaxXp = xpPercent >= 100;
    const xpRemaining = Math.max(0, xpNeeded - xp);

    if (!playerStats) {
        return (
            <div style={styles.card(theme)}>
                <h2 style={styles.title(theme)}>🧍 Player</h2>
                <p style={{ color: theme.subText }}>No player data loaded</p>
            </div>
        );
    }

    return (
        <motion.div
            style={styles.card(theme)}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
        >
            {/* HEADER (GLOBAL HUD STYLE GOLD) */}
            <div style={styles.headerRow}>
                <h2 style={styles.title(theme)}>Player Stats</h2>

                <div style={styles.goldPill}>
                    💰 {playerGold}
                </div>
            </div>

            {/* CORE (DIABLO STYLE LIST) */}
            <Section title="CORE" theme={theme}>
                <div style={styles.statList}>
                    <Stat
                        label="Health"
                        value={`${core.hp ?? 0} / ${core.maxhp ?? 0}`}
                        theme={theme}
                    />

                    <Stat
                        label="Level"
                        value={`⭐ ${level}`}
                        theme={theme}
                    />
                </div>
            </Section>

            {/* COMBAT */}
            <Section title="COMBAT" theme={theme}>
                <div style={styles.statList}>
                    <Stat label="Attack" value={combat.attack ?? 0} theme={theme} />
                    <Stat label="Defense" value={combat.defense ?? 0} theme={theme} />
                    <Stat
                        label="Crit"
                        value={`${((combat.critchance ?? 0) * 100).toFixed(1)}%`}
                        theme={theme}
                    />
                    <Stat
                        label="Crit Damage"
                        value={`${(combat.critmultiplier ?? 1).toFixed(2)}x`}
                        theme={theme}
                    />
                </div>
            </Section>

            {/* PROGRESSION */}
            <Section title="PROGRESSION" theme={theme}>
                <div style={styles.xpHeader(theme, isMaxXp)}>
                    <span>XP</span>
                    <span style={styles.xpText(theme)}>
                        {xp} / {xpNeeded} ({xpRemaining} left)
                    </span>
                </div>

                <div style={styles.bar}>
                    <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${xpPercent}%` }}
                        transition={{ duration: 0.6 }}
                        style={styles.fill(isMaxXp)}
                    />
                </div>

                <AnimatePresence>
                    {isMaxXp && (
                        <motion.div
                            initial={{ opacity: 0, y: 5 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0 }}
                            style={styles.levelUp}
                        >
                            ⚡ READY TO LEVEL UP
                        </motion.div>
                    )}
                </AnimatePresence>
            </Section>
        </motion.div>
    );
}

/* ================= UI BLOCKS ================= */

function Section({ title, theme, children }) {
    return (
        <div style={styles.section(theme)}>
            <div style={styles.sectionLabel(theme)}>{title}</div>
            {children}
        </div>
    );
}

function Stat({ label, value, theme }) {
    return (
        <div style={styles.diabloRow(theme)}>
            <div style={styles.leftLabel(theme)}>{label}</div>
            <div style={styles.rightValue(theme)}>{value}</div>
        </div>
    );
}

/* ================= STYLES ================= */

const styles = {
    card: (t) => ({
        background: t.cardBg,
        border: `1px solid ${t.subText}33`,
        borderRadius: "12px",
        padding: "14px",
        color: t.text,
        display: "flex",
        flexDirection: "column",
        gap: "12px"
    }),

    headerRow: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center"
    },

    title: (t) => ({
        fontWeight: 800,
        fontSize: "1.2rem",
        color: t.text
    }),

    goldPill: {
        fontWeight: 800,
        fontSize: "0.85rem",
        color: "#fbbf24",
        background: "rgba(251,191,36,0.08)",
        padding: "4px 10px",
        borderRadius: "999px",
        border: "1px solid rgba(251,191,36,0.15)"
    },

    section: (t) => ({
        padding: "12px",
        borderRadius: "12px",
        border: `1px solid ${t.subText}22`,
        background: t.cardBg
    }),

    sectionLabel: (t) => ({
        fontSize: "0.7rem",
        fontWeight: 800,
        letterSpacing: "2px",
        marginBottom: "10px",
        color: t.subText
    }),

    /* DIABLO LIST MODE */
    statList: {
        display: "flex",
        flexDirection: "column",
        gap: "6px"
    },

    diabloRow: (t) => ({
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "8px 10px",
        background: "rgba(0,0,0,0.15)",
        border: `1px solid ${t.subText}22`,
        borderRadius: "6px"
    }),

    leftLabel: (t) => ({
        color: t.subText,
        fontWeight: 700,
        fontSize: "0.7rem",
        letterSpacing: "1px",
        textTransform: "uppercase"
    }),

    rightValue: (t) => ({
        color: t.text,
        fontWeight: 900
    }),

    xpHeader: (t, max) => ({
        display: "flex",
        justifyContent: "space-between",
        fontSize: "0.8rem",
        fontWeight: 700,
        marginBottom: "8px",
        color: max ? "#22c55e" : t.text
    }),

    xpText: (t) => ({
        color: t.subText
    }),

    bar: {
        height: "10px",
        width: "100%",
        background: "rgba(0,0,0,0.1)",
        borderRadius: "999px",
        overflow: "hidden"
    },

    fill: (max) => ({
        height: "100%",
        borderRadius: "999px",
        background: max
            ? "linear-gradient(90deg, #22c55e, #a3e635)"
            : "linear-gradient(90deg, #4f46e5, #22c55e)"
    }),

    levelUp: {
        marginTop: "10px",
        fontWeight: 900,
        color: "#22c55e"
    }
};

export default PlayerStats;