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
        marginBottom: "12px"
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

            </div>
        </div>
    );
}

export default PlayerStats;