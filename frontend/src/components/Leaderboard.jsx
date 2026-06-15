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

    // ----------------------------
    // STYLES
    // ----------------------------
    const cardStyle = {
        background: theme.cardBg,
        color: theme.text,
        padding: "20px",
        borderRadius: "16px",
        marginTop: "20px",
        border: "1px solid rgba(255,255,255,0.04)",
        boxShadow: "0 10px 30px rgba(0,0,0,0.08)"
    };

    const titleStyle = {
        marginBottom: "12px",
        color: theme.text,
        fontWeight: "800",
        fontSize: "1.4rem"
    };

    const mutedText = {
        color: theme.subText
    };

    const rowStyle = (index) => ({
        display: "flex",
        justifyContent: "space-between",
        padding: "12px 10px",
        borderRadius: "10px",
        borderBottom: `1px solid ${theme.subText}22`,
        transition: "all 0.2s ease",
        background: index === 0 ? "rgba(234,179,8,0.06)" :
            index === 1 ? "rgba(148,163,184,0.06)" :
                index === 2 ? "rgba(180,83,9,0.06)" : "transparent"
    });

    const isLoggedIn = !!token;

    // ----------------------------
    // NOT LOGGED IN
    // ----------------------------
    if (!isLoggedIn) {
        return (
            <div style={cardStyle}>
                <h2 style={titleStyle}>Leaderboard</h2>
                <p style={mutedText}>🔒 Please login to view leaderboard</p>
            </div>
        );
    }

    // ----------------------------
    // LOADING STATE
    // ----------------------------
    if (loading) {
        return (
            <div style={cardStyle}>
                <h2 style={titleStyle}>Leaderboard</h2>
                <p style={mutedText}>Loading...</p>
            </div>
        );
    }

    // ----------------------------
    // ERROR STATE
    // ----------------------------
    if (error) {
        return (
            <div style={cardStyle}>
                <h2 style={titleStyle}>Leaderboard</h2>
                <p style={{ color: "#ef4444", fontWeight: "500" }}>
                    {error}
                </p>
            </div>
        );
    }

    // ----------------------------
    // MAIN UI
    // ----------------------------
    return (
        <div style={cardStyle}>
            <h2 style={titleStyle}>Leaderboard</h2>

            <div>
                {safeData.map((player, index) => (
                    <div
                        key={player.playerId}
                        style={rowStyle(index)}
                        onMouseEnter={(e) => {
                            e.currentTarget.style.transform = "translateX(3px)";
                            e.currentTarget.style.background = "rgba(99,102,241,0.08)";
                        }}
                        onMouseLeave={(e) => {
                            e.currentTarget.style.transform = "translateX(0px)";
                            e.currentTarget.style.background =
                                index === 0 ? "rgba(234,179,8,0.06)" :
                                    index === 1 ? "rgba(148,163,184,0.06)" :
                                        index === 2 ? "rgba(180,83,9,0.06)" : "transparent";
                        }}
                    >
                        <span style={{ fontWeight: "600" }}>
                            {getRankIcon(index)} Player {player.playerId}
                        </span>

                        <span style={{ color: theme.subText }}>
                            Level {player.level} | XP {player.xp} | 💰 {player.gold}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Leaderboard;