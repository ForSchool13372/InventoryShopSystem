import { motion } from "framer-motion";
import { playerStatsStyles as styles } from "./styles";

function Progression({ progression, theme }) {
    const xp = progression?.xp ?? 0;
    const level = progression?.level ?? 1;

    const xpNeeded = Math.floor(100 * Math.pow(1.15, level - 1));
    const xpPercentRaw = (xp / xpNeeded) * 100;
    const xpPercent = Math.min(100, xpPercentRaw);

    const isMaxXp = xpPercentRaw >= 100;
    const xpRemaining = Math.max(0, xpNeeded - xp);

    const isNearLevel = xpPercentRaw >= 75;

    return (
        <div style={styles.section(theme)}>

            {/* TITLE */}
            <h3
                style={{
                    marginBottom: "12px",
                    fontWeight: 900,
                    letterSpacing: "2px",
                    color: isMaxXp ? "#fbbf24" : theme.text,
                    fontSize: "0.9rem",
                    opacity: 0.95,
                    textShadow: isMaxXp
                        ? "0 0 10px rgba(251,191,36,0.4)"
                        : "0 0 10px rgba(255,255,255,0.03)"
                }}
            >
                PROGRESSION
            </h3>

            {/* HEADER */}
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "10px",
                    fontWeight: 800,
                    color: theme.text
                }}
            >
                <span style={{ letterSpacing: "1px" }}>XP</span>

                <span
                    style={{
                        fontSize: "0.75rem",
                        color: isNearLevel ? "#93c5fd" : theme.subText,
                        fontWeight: 700
                    }}
                >
                    {xp} / {xpNeeded} ({xpRemaining} left)
                </span>
            </div>

            {/* BAR BACKGROUND */}
            <div
                style={{
                    width: "100%",
                    height: "10px",
                    background: "rgba(0,0,0,0.35)",
                    borderRadius: "8px",
                    overflow: "hidden",
                    border: "1px solid rgba(255,255,255,0.08)",
                    boxShadow: "inset 0 0 10px rgba(0,0,0,0.6)"
                }}
            >
                <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${xpPercent}%` }}
                    transition={{
                        duration: 0.8,
                        ease: "easeOut"
                    }}
                    style={{
                        height: "100%",
                        background: isMaxXp
                            ? "linear-gradient(90deg, #fbbf24, #f59e0b)"
                            : isNearLevel
                                ? "linear-gradient(90deg, #60a5fa, #3b82f6)"
                                : "linear-gradient(90deg, #3b82f6, #2563eb)",

                        boxShadow: isMaxXp
                            ? "0 0 12px rgba(251,191,36,0.6)"
                            : isNearLevel
                                ? "0 0 10px rgba(59,130,246,0.4)"
                                : "none"
                    }}
                />
            </div>

            {/* SMALL STATUS FEEL (no spam text, subtle RPG feedback) */}
            {isMaxXp && (
                <div
                    style={{
                        marginTop: "8px",
                        fontSize: "0.75rem",
                        fontWeight: 800,
                        color: "#fbbf24",
                        letterSpacing: "1px",
                        textShadow: "0 0 8px rgba(251,191,36,0.3)"
                    }}
                >
                    READY FOR LEVEL UP
                </div>
            )}
        </div>
    );
}

export default Progression;