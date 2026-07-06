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
                paddingBottom: "14px",
                borderBottom: `1px solid ${theme.isLight ? "rgba(0,0,0,0.08)" : "rgba(255,255,255,0.06)"
                    }`
            }}
        >
            {/* MAIN TITLE */}
            <h1
                style={{
                    fontSize: "2.2rem",
                    fontWeight: 800,
                    margin: 0,
                    letterSpacing: "-0.5px",
                    color: theme.text
                }}
            >
                Inventory Shop System
            </h1>

            {/* IDENTITY BAR */}
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "14px"
                }}
            >
                {/* STATUS PILL */}
                <div
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
                        fontSize: "0.8rem"
                    }}
                >
                    <span
                        style={{
                            width: "8px",
                            height: "8px",
                            borderRadius: "50%",
                            background: isLoggedIn ? "#22c55e" : theme.subText
                        }}
                    />
                    {isLoggedIn ? "Online" : "Offline"}
                </div>

                {/* PLAYER BADGE */}
                {isLoggedIn && (
                    <div
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "10px",
                            padding: "6px 14px",
                            borderRadius: "10px",
                            background: theme.cardBg,
                            border: `1px solid ${theme.subText}33`,
                            boxShadow: "0 4px 12px rgba(0,0,0,0.08)"
                        }}
                    >
                        {/* Avatar Circle */}
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


                        {/* Player Label */}
                        <span
                            style={{
                                fontSize: "1rem",
                                fontWeight: 600,
                                color: theme.text
                            }}
                        >
                            Player {playerId}
                        </span>
                    </div>
                )}

                {/* GUEST SUBTITLE */}
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
