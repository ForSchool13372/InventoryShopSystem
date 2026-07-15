import { motion } from "framer-motion";

function LeaderboardPodium({
    topThree,
    podiumStyle,
    podiumContainerStyle,
    podiumIconStyle,
    getRankIcon,
    onSelectPlayer
}) {
    return (
        <div
            style={podiumContainerStyle}
        >
            {[1, 0, 2].map((rank) => {
                const player = topThree[rank];

                if (!player) return null;

                return (
                    <motion.div
                        key={player.playerId}
                        style={podiumStyle(rank)}
                        onClick={() => onSelectPlayer(player.playerId)}
                        whileHover={{
                            y: -8,
                            scale: 1.03,
                            boxShadow: "0 15px 35px rgba(0,0,0,0.25)"
                        }}
                        transition={{
                            type: "spring",
                            stiffness: 300,
                            delay: rank * 0.1
                        }}
                        initial={{
                            opacity: 0,
                            y: 20
                        }}
                        animate={{
                            opacity: 1,
                            y: 0
                        }}
                    >

                        <div style={podiumIconStyle}>
                            {getRankIcon(rank)}
                        </div>


                        <h3>
                            Player {player.playerId}
                        </h3>


                        <p>
                            Level {player.level}
                        </p>


                        <p>
                            💰 {player.gold}
                        </p>


                    </motion.div>
                );
            })}
        </div>
    );
}

export default LeaderboardPodium;