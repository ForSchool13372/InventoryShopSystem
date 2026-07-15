import { useState } from "react";
import { motion } from "framer-motion";

import useLeaderboard from "../../hooks/useLeaderboard";
import usePlayerProfile from "../../hooks/usePlayerProfile";

import LeaderboardInfoModal from "./LeaderboardInfoModal";
import LeaderboardRow from "./LeaderboardRow";
import LeaderboardPodium from "./LeaderboardPodium";
import PlayerProfileModal from "./PlayerProfileModal";

import { getLeaderboardStyles } from "./leaderboardStyles";
import soundSystem from "@/utils/soundSystem";

function Leaderboard({ theme, token }) {
    const { data, loading, error } = useLeaderboard(token);

    const {
        player: selectedPlayer,
        loading: profileLoading,
        error: profileError,
        fetchPlayer,
        clearPlayer
    } = usePlayerProfile();

    const [selectedPlayerId, setSelectedPlayerId] = useState(null);
    const [showInfo, setShowInfo] = useState(false);

    const safeData = Array.isArray(data?.data) ? data.data : [];
    const currentPlayerId = Number(localStorage.getItem("playerId"));

    const {
        cardStyle,
        titleStyle,
        titleContainerStyle,
        podiumStyle,
        podiumContainerStyle,
        podiumIconStyle,
        rowStyle,
        infoButtonStyle
    } = getLeaderboardStyles(theme, currentPlayerId);


    const playClick = () => soundSystem.play("click");


    const getRankIcon = (index) => {
        if (index === 0) return "🥇";
        if (index === 1) return "🥈";
        if (index === 2) return "🥉";
        return `#${index + 1}`;
    };


    const xpPercent = (xp) => {
        return Math.min(100, (xp / 100) * 100);
    };


    const handleOpenInfo = () => {
        playClick();
        setShowInfo(true);
    };


    const handleSelectPlayer = (playerId) => {
        playClick();
        setSelectedPlayerId(playerId);
        fetchPlayer(playerId);
    };


    const handleCloseProfile = () => {
        clearPlayer();
        setSelectedPlayerId(null);
    };


    if (loading) {
        return (
            <div style={cardStyle}>
                <h2 style={titleStyle}>
                    🏆 Leaderboard
                </h2>

                <p style={{ color: theme.subText }}>
                    Loading...
                </p>
            </div>
        );
    }


    if (error) {
        return (
            <div style={cardStyle}>
                <h2 style={titleStyle}>
                    🏆 Leaderboard
                </h2>

                <p style={{ color: "#ef4444" }}>
                    {error}
                </p>
            </div>
        );
    }


    const topThree = safeData.slice(0, 3);
    const rest = safeData.slice(3);


    return (
        <>
            <div style={cardStyle}>
                <h2 style={{ ...titleStyle, ...titleContainerStyle }}>
                    🏆 Leaderboard

                    <motion.button
                        whileHover={{ scale: 1.08 }}
                        whileTap={{ scale: 0.96 }}
                        onClick={handleOpenInfo}
                        style={infoButtonStyle}
                    >
                        ℹ️ Info
                    </motion.button>
                </h2>


                <LeaderboardPodium
                    topThree={topThree}
                    podiumStyle={podiumStyle}
                    podiumContainerStyle={podiumContainerStyle}
                    podiumIconStyle={podiumIconStyle}
                    getRankIcon={getRankIcon}
                    onSelectPlayer={handleSelectPlayer}
                />


                {rest.map((player) => (
                    <LeaderboardRow
                        key={player.playerId}
                        player={player}
                        theme={theme}
                        currentPlayerId={currentPlayerId}
                        rank={safeData.indexOf(player)}
                        xpPercent={xpPercent}
                        getRankIcon={getRankIcon}
                        rowStyle={rowStyle}
                        onSelectPlayer={handleSelectPlayer}
                    />
                ))}
            </div>


            <PlayerProfileModal
                player={selectedPlayer}
                playerId={selectedPlayerId}
                loading={profileLoading}
                error={profileError}
                onClose={handleCloseProfile}
                theme={theme}
            />


            {showInfo && (
                <LeaderboardInfoModal
                    theme={theme}
                    onClose={() => setShowInfo(false)}
                />
            )}
        </>
    );
}

export default Leaderboard;