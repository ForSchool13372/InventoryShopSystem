import { motion } from "framer-motion";

export default function CombatEnemy({
    enemy,
    displayEnemyHp
}) {
    if (!enemy) {
        return (
            <div
                style={{
                    padding: "14px",
                    borderRadius: "14px",
                    border: "1px solid rgba(239,68,68,0.35)",
                    background: "rgba(239,68,68,0.05)",
                    textAlign: "center",
                    color: "#d1d5db"
                }}
            >
                👹 No Enemy Encountered
            </div>
        );
    }

    const enemyHpPercent = Math.max(
        (displayEnemyHp / enemy.maxHp) * 100,
        0
    );

    const portraitMap = {
        Goblin: "👺",
        Slime: "🟢",
        Orc: "👹",
        "Training Dummy": "🎯"
    };

    const portrait = portraitMap[enemy.name] ?? "👹";

    const hpColor =
        enemyHpPercent > 60
            ? "#22c55e"
            : enemyHpPercent > 30
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
                border: "1px solid rgba(239,68,68,0.45)",
                borderRadius: "18px",
                padding: "16px",
                background:
                    "linear-gradient(180deg, rgba(239,68,68,0.08), rgba(239,68,68,0.03))",
                boxShadow:
                    "0 0 22px rgba(239,68,68,0.18)",
                position: "relative",
                overflow: "hidden"
            }}
        >

            {/* DEAD OVERLAY */}
            {displayEnemyHp <= 0 && (
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

            {/* HEADER */}
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
                            enemyHpPercent <= 30
                                ? [1, 1.08, 1]
                                : [1, 1.04, 1]
                    }}
                    transition={{
                        duration:
                            enemyHpPercent <= 30
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
                        background: "rgba(239,68,68,0.15)",
                        border: "2px solid rgba(239,68,68,0.55)",
                        boxShadow:
                            "0 0 18px rgba(239,68,68,0.4)"
                    }}
                >
                    {portrait}
                </motion.div>

                <div style={{ flex: 1 }}>
                    <div
                        style={{
                            fontSize: "1.1rem",
                            fontWeight: 900
                        }}
                    >
                        {enemy.name}
                    </div>

                    <div
                        style={{
                            fontSize: "0.75rem",
                            opacity: 0.7
                        }}
                    >
                        Hostile Creature
                    </div>
                </div>
            </div>

            {/* HP */}
            <div
                style={{
                    marginTop: "16px",
                    display: "flex",
                    justifyContent: "space-between",
                    fontSize: "0.82rem",
                    fontWeight: 700
                }}
            >
                <span>❤️ HP</span>

                <span>
                    {displayEnemyHp}/{enemy.maxHp}
                </span>
            </div>

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
                        width: `${enemyHpPercent}%`
                    }}
                    transition={{
                        duration: 0.45
                    }}
                    style={{
                        height: "100%",
                        background: `linear-gradient(90deg, ${hpColor}, #ef4444)`,
                        boxShadow: `0 0 14px ${hpColor}`
                    }}
                />
            </div>

            {/* STATS */}
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
                        ⚔️ DAMAGE
                    </div>

                    <div
                        style={{
                            fontWeight: 800,
                            marginTop: "2px"
                        }}
                    >
                        {enemy.minDamage}-{enemy.maxDamage}
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
                        ⭐ REWARD
                    </div>

                    <div
                        style={{
                            fontWeight: 800,
                            marginTop: "2px"
                        }}
                    >
                        {enemy.xp} XP
                    </div>
                </div>
            </div>

            {/* GOLD */}
            <div
                style={{
                    marginTop: "12px",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    gap: "6px",
                    fontWeight: 800,
                    color: "#fbbf24"
                }}
            >
                💰 {enemy.gold} Gold
            </div>

        </motion.div>
    );
}