import useLeaderboard from "../hooks/useLeaderboard";

function Leaderboard({ theme, token }) {
    const { data, loading, error } = useLeaderboard(token);

    const safeData = Array.isArray(data?.data) ? data.data : [];

    const getRankIcon = (index) => {
        if (index === 0) return "🥇";
        if (index === 1) return "🥈";
        if (index === 2) return "🥉";
        return `#${index + 1}`;
    };

    const cardStyle = {
        background: theme.cardBg,
        color: theme.text,
        padding: "20px",
        borderRadius: "16px",
        marginTop: "20px",
        border: "1px solid rgba(0,0,0,0.05)"
    };

    const mutedText = {
        color: theme.subText
    };

    if (!token) {
        return (
            <div style={cardStyle}>
                <h2 style={{ marginBottom: "10px", color: theme.text }}>
                    Leaderboard
                </h2>
                <p style={mutedText}>🔒 Please login to view leaderboard</p>
            </div>
        );
    }

    return (
        <div style={cardStyle}>
            <h2 style={{ marginBottom: "12px", color: theme.text, fontWeight: "800" }}>
                Leaderboard
            </h2>

            {loading && <p style={mutedText}>Loading...</p>}
            {error && <p style={{ color: "#ef4444" }}>{error}</p>}

            {!loading && !error && (
                <div>
                    {safeData.map((player, index) => (
                        <div
                            key={player.playerId}
                            style={{
                                display: "flex",
                                justifyContent: "space-between",
                                padding: "10px 0",
                                borderBottom: `1px solid ${theme.subText}33`
                            }}
                        >
                            <span>
                                {getRankIcon(index)} Player {player.playerId}
                            </span>

                            <span style={{ color: theme.subText }}>
                                Level {player.level} | XP {player.xp} | 💰 {player.gold}
                            </span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default Leaderboard;