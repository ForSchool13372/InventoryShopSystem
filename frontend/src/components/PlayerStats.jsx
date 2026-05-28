function PlayerStats({ playerStats }) {
    if (!playerStats) {
        return (
            <div style={{
                background: "#fff",
                padding: "20px",
                borderRadius: "14px",
                boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
                marginBottom: "20px",
                border: "1px solid rgba(0,0,0,0.05)"
            }}>
                <h2>Player Stats</h2>
                <p style={{ color: "#6b7280", marginTop: "10px" }}>
                    No player data loaded
                </p>
            </div>
        );
    }

    return (
        <div style={{
            background: "#fff",
            padding: "20px",
            borderRadius: "14px",
            boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
            marginBottom: "20px",
            border: "1px solid rgba(0,0,0,0.05)"
        }}>
            <h2>Player Stats</h2>

            <div style={{
                display: "flex",
                gap: "15px",
                color: "#374151",
                fontWeight: "600",
                marginTop: "10px",
                flexWrap: "wrap"
            }}>
                <span>💰 {playerStats.gold}</span>
                <span>❤️ {playerStats.hp}</span>
                <span>⭐ Level {playerStats.level}</span>
            </div>
        </div>
    );
}

export default PlayerStats;