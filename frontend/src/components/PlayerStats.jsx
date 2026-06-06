import { motion } from "framer-motion";

function PlayerStats({ playerStats, theme }) {

    const cardStyle = {
        background: theme.cardBg,
        color: theme.text,
        padding: "20px",
        borderRadius: "18px",
        boxShadow: "0 12px 35px rgba(0,0,0,0.08)",
        border: "1px solid rgba(0,0,0,0.05)"
    };

    const titleStyle = {
        fontSize: "1.2rem",
        fontWeight: "800",
        marginBottom: "12px",
        color: theme.text
    };

    const statsGrid = {
        display: "grid",
        gridTemplateColumns: "repeat(3, 1fr)",
        gap: "12px"
    };

    const baseStatCard = {
        padding: "14px",
        borderRadius: "14px",
        border: `1px solid ${theme.subText}25`,
        background: theme.cardBg,
        cursor: "default"
    };

    const labelStyle = {
        fontSize: "0.75rem",
        color: theme.subText,
        fontWeight: "600",
        marginBottom: "6px"
    };

    const valueStyle = {
        fontSize: "1.1rem",
        fontWeight: "800"
    };

    if (!playerStats) {
        return (
            <div style={cardStyle}>
                <h2 style={titleStyle}>Player Stats</h2>
                <p style={{ color: theme.subText }}>
                    📊 No player data loaded
                </p>
            </div>
        );
    }

    const xp = playerStats.xp || 0;
    const level = playerStats.level || 1;
    const xpNeeded = level * 100;
    const xpPercent = Math.min(100, (xp / xpNeeded) * 100);
    const isMaxXp = xpPercent >= 100;

    return (
        <div style={cardStyle}>
            {/* HEADER */}
            <h2 style={titleStyle}>Player Stats</h2>

            {/* GRID */}
            <div style={statsGrid}>

                {/* GOLD */}
                <motion.div
                    whileHover={{ scale: 1.05, y: -3 }}
                    transition={{ duration: 0.2 }}
                    style={{
                        ...baseStatCard,
                        background: "linear-gradient(135deg, #facc15, #fbbf24)",
                        color: "#111827",
                        boxShadow: "0 8px 20px rgba(250,204,21,0.25)"
                    }}
                >
                    <div style={labelStyle}>Gold</div>
                    <div style={valueStyle}>💰 {playerStats.gold}</div>
                </motion.div>

                {/* HP */}
                <motion.div
                    whileHover={{ scale: 1.05, y: -3 }}
                    transition={{ duration: 0.2 }}
                    style={{
                        ...baseStatCard,
                        background: "linear-gradient(135deg, #ef4444, #f87171)",
                        color: "white",
                        boxShadow: "0 8px 20px rgba(239,68,68,0.25)"
                    }}
                >
                    <div style={labelStyle}>Health</div>
                    <div style={valueStyle}>❤️ {playerStats.hp}</div>
                </motion.div>

                {/* LEVEL */}
                <motion.div
                    whileHover={{ scale: 1.05, y: -3 }}
                    transition={{ duration: 0.2 }}
                    style={{
                        ...baseStatCard,
                        background: "linear-gradient(135deg, #4f46e5, #6366f1)",
                        color: "white",
                        boxShadow: "0 8px 20px rgba(79,70,229,0.25)"
                    }}
                >
                    <div style={labelStyle}>Level</div>
                    <div style={valueStyle}>⭐ {playerStats.level}</div>
                </motion.div>

                {/* XP BAR */}
                <div style={{ marginTop: "18px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                        <span style={{ color: theme.subText, fontSize: "0.8rem", fontWeight: "600" }}>
                            XP
                        </span>

                        <motion.span
                            animate={isMaxXp ? { scale: [1, 1.2, 1] } : {}}
                            transition={{ repeat: isMaxXp ? Infinity : 0, duration: 0.8 }}
                            style={{
                                color: isMaxXp ? "#22c55e" : theme.subText,
                                fontSize: "0.8rem",
                                fontWeight: "700"
                            }}
                        >
                            {xp} / {xpNeeded}
                        </motion.span>
                    </div>

                    {/* BACK BAR */}
                    <div
                        style={{
                            width: "100%",
                            height: "12px",
                            background: "rgba(0,0,0,0.15)",
                            borderRadius: "999px",
                            overflow: "hidden",
                            position: "relative"
                        }}
                    >
                        {/* GLOW LAYER */}
                        <div
                            style={{
                                position: "absolute",
                                inset: 0,
                                background: isMaxXp
                                    ? "rgba(34,197,94,0.3)"
                                    : "rgba(79,70,229,0.2)",
                                filter: "blur(10px)"
                            }}
                        />

                        {/* FILL */}
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${xpPercent}%` }}
                            transition={{ duration: 0.6, ease: "easeOut" }}
                            style={{
                                height: "100%",
                                background: isMaxXp
                                    ? "linear-gradient(90deg, #22c55e, #a3e635)"
                                    : "linear-gradient(90deg, #4f46e5, #22c55e)",
                                borderRadius: "999px",
                                boxShadow: isMaxXp
                                    ? "0 0 15px rgba(34,197,94,0.7)"
                                    : "0 0 12px rgba(79,70,229,0.5)"
                            }}
                        />
                    </div>

                    {/* LEVEL UP TEXT */}
                    {isMaxXp && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.3 }}
                            style={{
                                marginTop: "8px",
                                color: "#22c55e",
                                fontWeight: "800",
                                fontSize: "0.85rem",
                                textShadow: "0 0 10px rgba(34,197,94,0.6)"
                            }}
                        >
                            ⚡ LEVEL UP READY!
                        </motion.div>
                    )}
                </div>

            </div>
        </div>
    );
}

export default PlayerStats;