import { motion } from "framer-motion";
import { fadeUp } from "../../animations";

export default function HeaderBar({ theme, token, playerId }) {
    const isLoggedIn = Boolean(token);

    return (
        <motion.div
            variants={fadeUp(0)}
            initial="hidden"
            animate="show"
            style={{
                display: "flex",
                flexDirection: "column",
                gap: "12px",
                padding: "0",
                margin: "0",
                border: "none",
                boxSizing: "border-box",
                width: "100%",
                transform: "translateZ(0)"
            }}

        >
            {/* MAIN TITLE */}
            <h1
                style={{
                    margin: 0,
                    fontSize: "1.75rem",
                    fontWeight: 900,
                    letterSpacing: "1px",
                    color: theme.text,
                    textTransform: "uppercase",
                    textShadow: `
            0 2px 6px rgba(0,0,0,0.35),
            0 0 10px rgba(79,70,229,0.35),
            0 0 20px rgba(79,70,229,0.18)
        `
                }}
            >
                Realmforge RPG
            </h1>


            {/* IDENTITY BAR UNDER TITLE */}
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "14px",
                    paddingLeft: "0"
                }}
            >
                {/* STATUS PILL */}
                <motion.div
                    whileHover={{
                        scale: 1.05,
                        y: -1,
                        boxShadow: isLoggedIn
                            ? "0 0 18px rgba(34,197,94,0.35)"
                            : "0 0 16px rgba(148,163,184,0.2)"
                    }}
                    transition={{ duration: 0.18 }}
                    style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "6px",
                        padding: "4px 10px",
                        borderRadius: "999px",
                        background: isLoggedIn
                            ? "rgba(34,197,94,0.12)"
                            : "rgba(148,163,184,0.12)",
                        border: isLoggedIn
                            ? "1px solid rgba(34,197,94,0.35)"
                            : "1px solid rgba(148,163,184,0.35)",
                        color: isLoggedIn ? "#22c55e" : theme.subText,
                        fontWeight: 700,
                        fontSize: "0.8rem",
                        cursor: "default"
                    }}
                >
                    <motion.span
                        animate={
                            isLoggedIn
                                ? {
                                    scale: [1, 1.3, 1],
                                    opacity: [1, 0.6, 1]
                                }
                                : {}
                        }
                        transition={{
                            duration: 1.8,
                            repeat: Infinity,
                            ease: "easeInOut"
                        }}
                        style={{
                            width: "8px",
                            height: "8px",
                            borderRadius: "50%",
                            background: isLoggedIn ? "#22c55e" : theme.subText
                        }}
                    />
                    {isLoggedIn ? "Online" : "Offline"}
                </motion.div>

                {/* PLAYER BADGE */}
                {isLoggedIn && (
                    <motion.div
                        whileHover={{
                            scale: 1.04,
                            y: -2,
                            boxShadow: theme.isLight
                                ? "0 10px 24px rgba(59,130,246,0.18)"
                                : "0 10px 28px rgba(96,165,250,0.25)"
                        }}
                        transition={{ duration: 0.18 }}
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "10px",
                            padding: "6px 14px",
                            borderRadius: "10px",
                            background: theme.cardBg,
                            border: `1px solid ${theme.subText}33`,
                            boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
                            cursor: "default"
                        }}
                    >
                        <div
                            style={{
                                width: "30px",
                                height: "30px",
                                borderRadius: "50%",
                                background: theme.isLight ? "#e2e8f0" : "#1e293b",
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                                fontWeight: 700,
                                color: theme.text,
                                fontSize: "0.85rem"
                            }}
                        >
                            {`P${playerId}`}
                        </div>

                        <span
                            style={{
                                fontSize: "0.5rem",
                                fontWeight: 600,
                                color: theme.text
                            }}
                        >
                            Player {playerId}
                        </span>
                    </motion.div>
                )}

                {!isLoggedIn && (
                    <span
                        style={{
                            fontSize: "1rem",
                            fontWeight: 500,
                            color: theme.subText,
                            opacity: 0.85
                        }}
                    >
                        Start your adventure
                    </span>
                )}
            </div>
        </motion.div>
    );
}
