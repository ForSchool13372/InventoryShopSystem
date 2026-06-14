import { motion } from "framer-motion";

function PlayerStats({ playerStats, theme }) {
    const currentTheme = theme;

    if (!playerStats) {
        return (
            <div style={styles.card(currentTheme)}>
                <h2 style={styles.title(currentTheme)}>PLAYER STATS</h2>
                <p style={{ color: currentTheme.subText }}>
                    📊 No player data loaded
                </p>
            </div>
        );
    }

    const xp = playerStats.xp ?? 0;
    const level = playerStats.level ?? 1;
    const xpNeeded = level * 100;
    const xpPercent = Math.min(100, (xp / xpNeeded) * 100);
    const isMaxXp = xpPercent >= 100;

    return (
        <div style={styles.card(currentTheme)}>
            <h2 style={styles.title(currentTheme)}>PLAYER STATS</h2>

            {/* SECTION LABEL */}
            <div style={styles.sectionLabel(currentTheme)}>CORE STATS</div>

            {/* TOP STATS */}
            <div style={styles.grid}>
                <Stat label="Gold" value={`💰 ${playerStats.gold ?? 0}`} color1="#facc15" color2="#fbbf24" />
                <Stat label="Health" value={`❤️ ${playerStats.hp ?? 0}`} color1="#ef4444" color2="#f87171" />
                <Stat label="Level" value={`⭐ ${level}`} color1="#4f46e5" color2="#6366f1" />
            </div>

            {/* SECTION LABEL */}
            <div style={styles.sectionLabel(currentTheme)}>PROGRESSION</div>

            {/* XP SECTION */}
            <div style={styles.xpSection}>
                <div style={styles.xpHeader(currentTheme, isMaxXp)}>
                    <span>Experience</span>
                    <span>{xp} / {xpNeeded}</span>
                </div>

                <div style={styles.xpBar}>
                    <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${xpPercent}%` }}
                        transition={{ duration: 0.9, ease: "easeOut" }}
                        style={styles.xpFill(isMaxXp)}
                    />
                </div>

                {isMaxXp && (
                    <motion.div
                        initial={{ opacity: 0, y: 8 }}
                        animate={{ opacity: 1, y: 0 }}
                        style={styles.levelUp}
                    >
                        ⚡ READY TO LEVEL UP
                    </motion.div>
                )}
            </div>
        </div>
    );
}

/* ---------------- COMPONENT ---------------- */

function Stat({ label, value, color1, color2 }) {
    return (
        <motion.div
            whileHover={{ scale: 1.06, y: -4 }}
            transition={{ duration: 0.2 }}
            style={{
                background: `linear-gradient(135deg, ${color1}, ${color2})`,
                borderRadius: "16px",
                padding: "14px",
                color: "#111",
                boxShadow: "0 10px 25px rgba(0,0,0,0.15)",
                cursor: "default"
            }}
        >
            <div style={styles.label}>{label}</div>
            <div style={styles.value}>{value}</div>
        </motion.div>
    );
}

/* ---------------- STYLES ---------------- */

const styles = {
    card: (theme) => ({
        background: theme.cardBg,
        color: theme.text,
        padding: "22px",
        borderRadius: "20px",
        border: "1px solid rgba(255,255,255,0.06)",
        boxShadow: "0 18px 50px rgba(0,0,0,0.25)",

        display: "flex",
        flexDirection: "column"
    }),

    title: (theme) => ({
        fontSize: "1.2rem",
        fontWeight: 800,
        letterSpacing: "2px",
        marginBottom: 14,
        color: theme.text
    }),

    sectionLabel: () => ({
        fontSize: "0.7rem",
        fontWeight: 800,
        letterSpacing: "2px",
        marginBottom: 10,
        marginTop: 8,
    }),

    grid: {
        display: "grid",
        gridTemplateColumns: "repeat(3, 1fr)",
        gap: 12,
        marginBottom: 18
    },

    label: {
        fontSize: "0.7rem",
        fontWeight: 700,
        opacity: 0.85,
        marginBottom: 6
    },

    value: {
        fontSize: "1.15rem",
        fontWeight: 900
    },

    xpSection: {
        marginTop: 6
    },

    xpHeader: (theme, isMaxXp) => ({
        display: "flex",
        justifyContent: "space-between",
        fontSize: "0.8rem",
        fontWeight: 700,
        marginBottom: 8,
        color: isMaxXp ? "#22c55e" : theme.subText
    }),

    xpBar: {
        width: "100%",
        height: "14px",
        background: "rgba(255,255,255,0.08)",
        borderRadius: "999px",
        overflow: "hidden",
        position: "relative"
    },

    xpFill: (isMaxXp) => ({
        height: "100%",
        borderRadius: "999px",
        background: isMaxXp
            ? "linear-gradient(90deg, #22c55e, #a3e635)"
            : "linear-gradient(90deg, #4f46e5, #22c55e)",
        boxShadow: isMaxXp
            ? "0 0 18px rgba(34,197,94,0.6)"
            : "0 0 14px rgba(79,70,229,0.4)"
    }),

    levelUp: {
        marginTop: 10,
        fontSize: "0.85rem",
        fontWeight: 900,
        color: "#22c55e",
        textShadow: "0 0 12px rgba(34,197,94,0.5)"
    }
};

export default PlayerStats;