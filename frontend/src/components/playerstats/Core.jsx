import { motion } from "framer-motion";
import { playerStatsStyles as styles } from "./styles";

function Core({ core, progression, theme }) {
    const hp = core.hp ?? 0;
    const maxHp = Math.max(1, core.maxhp ?? 1);

    const hpPercentRaw = (hp / maxHp) * 100;
    const hpPercent = Math.min(100, hpPercentRaw);

    const isLowHp = hpPercentRaw < 25;

    return (
        <div style={styles.section(theme)}>

            {/* TITLE */}
            <h3
                style={{
                    marginBottom: "12px",
                    fontWeight: 900,
                    letterSpacing: "2px",
                    color: isLowHp ? "#ff4d4d" : theme.text,
                    fontSize: "0.9rem",
                    opacity: isLowHp ? 1 : 0.9,
                    textShadow: isLowHp ? "0 0 10px rgba(255,0,0,0.5)" : "none"
                }}
            >
                CORE
            </h3>

            <div style={styles.statList()}>

                <Stat
                    label="Health"
                    value={`${hp} / ${maxHp}`}
                    theme={theme}
                />

                {/* HP BAR (AAA STYLE) */}
                <div style={{ marginTop: "6px", marginBottom: "10px" }}>
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
                            animate={{ width: `${hpPercent}%` }}
                            transition={{
                                duration: 0.8,
                                ease: "easeOut"
                            }}
                            style={{
                                height: "100%",
                                background: isLowHp
                                    ? "linear-gradient(90deg, #ff3b3b, #ff6b6b)"
                                    : "linear-gradient(90deg, #22c55e, #4ade80)",
                                boxShadow: isLowHp
                                    ? "0 0 12px rgba(255,0,0,0.6)"
                                    : "0 0 10px rgba(34,197,94,0.4)"
                            }}
                        />
                    </div>
                </div>

                <Stat
                    label="Level"
                    value={`⭐ ${progression.level ?? 1}`}
                    theme={theme}
                />

            </div>
        </div>
    );
}

function Stat({ label, value, theme }) {
    return (
        <div style={styles.diabloRow(theme)}>
            <div style={styles.leftLabel(theme)}>{label}</div>
            <div style={styles.rightValue(theme)}>{value}</div>
        </div>
    );
}

export default Core;