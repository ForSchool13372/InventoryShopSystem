import { AnimatePresence, motion } from "framer-motion";

export default function CombatLog({
    displayLog,
    getLogStyle,
    styles
}) {

    const getIcon = (line) => {
        if (line.includes("CRITICAL")) {
            return "💥";
        }

        if (line.includes("You deal")) {
            return "⚔️";
        }

        if (line.includes("hits you")) {
            return "🩸";
        }

        if (line.includes("defeated")) {
            return "🏆";
        }

        if (line.includes("XP") || line.includes("gold")) {
            return "✨";
        }

        return "📜";
    };


    return (
        <div
            style={{
                ...styles.log,
                maxHeight: "260px",
                overflowY: "auto",
                padding: "14px",
                borderRadius: "14px",
                background:
                    "rgba(0,0,0,0.18)",
                border:
                    "1px solid rgba(255,255,255,0.08)",
                boxShadow:
                    "inset 0 0 20px rgba(0,0,0,0.25)"
            }}
        >

            {displayLog.length === 0 ? (

                <motion.div
                    initial={{
                        opacity: 0
                    }}
                    animate={{
                        opacity: 0.6
                    }}
                >
                    📜 No battle yet. Press Attack.
                </motion.div>

            ) : (

                <AnimatePresence initial={false}>

                    {displayLog.map((line, i) => (

                        <motion.div
                            key={i}
                            initial={{
                                opacity: 0,
                                x: -12,
                                scale: 0.98
                            }}
                            animate={{
                                opacity: 1,
                                x: 0,
                                scale: 1
                            }}
                            exit={{
                                opacity: 0
                            }}
                            transition={{
                                duration: 0.25
                            }}
                            whileHover={{
                                x: 4
                            }}
                            style={{
                                display: "flex",
                                alignItems: "center",
                                gap: "8px",
                                marginBottom: "8px",
                                padding:
                                    "6px 8px",
                                borderRadius:
                                    "8px",
                                background:
                                    "rgba(255,255,255,0.025)",
                                fontSize:
                                    "0.9rem",
                                ...getLogStyle(line)
                            }}
                        >

                            <span>
                                {getIcon(line)}
                            </span>

                            <span>
                                {line}
                            </span>

                        </motion.div>

                    ))}

                </AnimatePresence>

            )}

        </div>
    );
}