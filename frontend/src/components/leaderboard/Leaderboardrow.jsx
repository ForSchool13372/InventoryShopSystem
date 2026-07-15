import { motion } from "framer-motion";

function LeaderboardRow({
    player,
    theme,
    currentPlayerId,
    rank,
    xpPercent,
    getRankIcon,
    rowStyle,
    onSelectPlayer
}) {
    return (
        <motion.div
            key={player.playerId}
            style={{
                ...rowStyle(player),
                cursor: "pointer"
            }}
            onClick={() => onSelectPlayer(player.playerId)}
            whileHover={{
                scale: 1.02,
                x: 5
            }}
            initial={{
                opacity: 0,
                y: 10
            }}
            animate={{
                opacity: 1,
                y: 0
            }}
        >

            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between"
                }}
            >

                <span
                    style={{
                        fontWeight: "800"
                    }}
                >
                    {getRankIcon(rank)} Player {player.playerId}
                    {player.playerId === currentPlayerId && " ⭐"}
                </span>


                <span
                    style={{
                        color: theme.subText
                    }}
                >
                    Lv {player.level}
                </span>

            </div>


            {/* XP BAR */}
            <div
                style={{
                    marginTop: "10px",
                    height: "8px",
                    background: "rgba(255,255,255,0.08)",
                    borderRadius: "10px",
                    overflow: "hidden"
                }}
            >
                <motion.div
                    initial={{ width: 0 }}
                    animate={{
                        width: `${xpPercent(player.xp)}%`
                    }}
                    style={{
                        height: "100%",
                        background:
                            "linear-gradient(90deg,#6366f1,#a855f7)",
                        borderRadius: "10px"
                    }}
                />
            </div>


            <div
                style={{
                    marginTop: "8px",
                    color: theme.subText,
                    fontSize: "0.9rem"
                }}
            >
                XP {player.xp}/100
                {" | "}
                💰 {player.gold}
            </div>

        </motion.div>
    );
}

export default LeaderboardRow;