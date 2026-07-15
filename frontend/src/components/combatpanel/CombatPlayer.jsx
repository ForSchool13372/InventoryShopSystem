import { motion } from "framer-motion";

export default function CombatPlayer({
    displayPlayerHp,
    maxPlayerHp,
    playerStats
}) {

    if (!maxPlayerHp) {
        return (
            <div
                style={{
                    padding: "12px",
                    borderRadius: "12px",
                    border: "1px solid rgba(96,165,250,0.35)"
                }}
            >
                🧙 Awaiting Battle...
            </div>
        );
    }

    const playerHpPercent = Math.max(
        (displayPlayerHp / maxPlayerHp) * 100,
        0
    );

    const hpColor =
        playerHpPercent > 60
            ? "#22c55e"
            : playerHpPercent > 30
                ? "#f59e0b"
                : "#ef4444";

    return (
        <motion.div
            whileHover={{
                scale: 1.015
            }}
            transition={{
                duration: 0.2
            }}
            style={{
                border: "1px solid rgba(96,165,250,0.45)",
                borderRadius: "18px",
                padding: "16px",
                background:
                    "linear-gradient(180deg, rgba(96,165,250,0.10), rgba(96,165,250,0.03))",
                boxShadow:
                    "0 0 22px rgba(96,165,250,0.18)",
                position: "relative",
                overflow: "hidden"
            }}
        >

            {/* DEFEATED OVERLAY */}
            {displayPlayerHp <= 0 && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    style={{
                        position: "absolute",
                        inset: 0,
                        background: "rgba(0,0,0,0.45)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: "2rem",
                        fontWeight: 900,
                        zIndex: 5
                    }}
                >
                    💀
                </motion.div>
            )}


            {/* PORTRAIT + NAME */}
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "14px"
                }}
            >

                <motion.div
                    animate={{
                        scale:
                            playerHpPercent <= 30
                                ? [1, 1.08, 1]
                                : [1, 1.04, 1]
                    }}
                    transition={{
                        duration:
                            playerHpPercent <= 30
                                ? 0.6
                                : 0.8,
                        repeat: Infinity,
                        repeatDelay: 2
                    }}
                    style={{
                        width: "58px",
                        height: "58px",
                        borderRadius: "50%",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: "2rem",
                        background:
                            "rgba(96,165,250,0.15)",
                        border:
                            "2px solid rgba(96,165,250,0.55)",
                        boxShadow:
                            "0 0 18px rgba(96,165,250,0.4)"
                    }}
                >
                    🧙
                </motion.div>


                <div>
                    <div
                        style={{
                            fontSize: "1.1rem",
                            fontWeight: 900
                        }}
                    >
                        Hero
                    </div>

                    <div
                        style={{
                            fontSize: "0.75rem",
                            opacity: 0.7
                        }}
                    >
                        Adventurer
                    </div>
                </div>

            </div>


            {/* HP TEXT */}
            <div
                style={{
                    marginTop: "16px",
                    display: "flex",
                    justifyContent: "space-between",
                    fontSize: "0.82rem",
                    fontWeight: 700
                }}
            >
                <span>
                    ❤️ HP
                </span>

                <span>
                    {displayPlayerHp}/{maxPlayerHp}
                </span>
            </div>


            {/* HP BAR */}
            <div
                style={{
                    height: "10px",
                    background: "#1f2937",
                    borderRadius: "999px",
                    overflow: "hidden",
                    marginTop: "6px"
                }}
            >
                <motion.div
                    animate={{
                        width: `${playerHpPercent}%`
                    }}
                    transition={{
                        duration: 0.45
                    }}
                    style={{
                        height: "100%",
                        background:
                            `linear-gradient(90deg, ${hpColor}, #60a5fa)`,
                        boxShadow:
                            `0 0 14px ${hpColor}`
                    }}
                />
            </div>


            {/* PLAYER INFO */}
            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: "10px",
                    marginTop: "16px"
                }}
            >

                <div
                    style={{
                        padding: "10px",
                        borderRadius: "10px",
                        background: "rgba(255,255,255,0.04)",
                        textAlign: "center"
                    }}
                >
                    <div
                        style={{
                            fontSize: "0.7rem",
                            opacity: 0.65
                        }}
                    >
                        ⚔️ ATTACK
                    </div>

                    <div
                        style={{
                            fontWeight: 800,
                            marginTop: "2px"
                        }}
                    >
                        {playerStats?.combat?.attack ?? 0}
                    </div>
                </div>


                <div
                    style={{
                        padding: "10px",
                        borderRadius: "10px",
                        background: "rgba(255,255,255,0.04)",
                        textAlign: "center"
                    }}
                >
                    <div
                        style={{
                            fontSize: "0.7rem",
                            opacity: 0.65
                        }}
                    >
                        🛡️ DEFENSE
                    </div>

                    <div
                        style={{
                            fontWeight: 800,
                            marginTop: "2px"
                        }}
                    >
                        {playerStats?.combat?.defense ?? 0}
                    </div>
                </div>


                <div
                    style={{
                        padding: "10px",
                        borderRadius: "10px",
                        background: "rgba(255,255,255,0.04)",
                        textAlign: "center"
                    }}
                >
                    <div
                        style={{
                            fontSize: "0.7rem",
                            opacity: 0.65
                        }}
                    >
                        💥 CRIT
                    </div>

                    <div
                        style={{
                            fontWeight: 800,
                            marginTop: "2px"
                        }}
                    >
                        {playerStats?.combat?.critchance
                            ? `${Math.round(playerStats.combat.critchance * 100)}%`
                            : "0%"}
                    </div>
                </div>


                <div
                    style={{
                        padding: "10px",
                        borderRadius: "10px",
                        background: "rgba(255,255,255,0.04)",
                        textAlign: "center"
                    }}
                >
                    <div
                        style={{
                            fontSize: "0.7rem",
                            opacity: 0.65
                        }}
                    >
                        ❤️ HEALTH
                    </div>

                    <div
                        style={{
                            fontWeight: 800,
                            marginTop: "2px"
                        }}
                    >
                        {Math.round(playerHpPercent)}%
                    </div>
                </div>

            </div>

        </motion.div>
    );
}