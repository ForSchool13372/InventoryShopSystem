import { motion } from "framer-motion";

export default function HeaderHUD({ playerStats, theme }) {
    if (!playerStats) return null;

    const gold = playerStats?.core?.gold ?? 0;
    const hp = playerStats?.core?.hp ?? 0;
    const maxhp = playerStats?.core?.maxhp ?? 1;

    const level = playerStats?.progression?.level ?? 1;
    const xp = playerStats?.progression?.xp ?? 0;

    const xpNeeded = Math.floor(100 * Math.pow(1.15, level - 1));
    const xpPercent = Math.min(100, (xp / xpNeeded) * 100);
    const hpPercent = Math.min(100, (hp / maxhp) * 100);

    const hpColor =
        hpPercent <= 25 ? "#ef4444" :
            hpPercent <= 50 ? "#f59e0b" :
                "#22c55e";

    return (
        <motion.div
            whileHover={{ y: -2 }}
            style={{
                display: "flex",
                flexDirection: "row",
                alignItems: "center",
                gap: 24,
                padding: "12px 18px",
                borderRadius: 14,
                background: `
                    radial-gradient(circle at top left, rgba(99,102,241,0.28), transparent 45%),
                    linear-gradient(135deg, ${theme.cardBg}, rgba(99,102,241,0.12))
                `,
                border: "1px solid rgba(129,140,248,0.45)",
                boxShadow: `
                    0 0 25px rgba(99,102,241,0.22),
                    inset 0 0 20px rgba(99,102,241,0.08)
                `,
                backdropFilter: "blur(12px)",
                color: theme.text,
                flexWrap: "nowrap"
            }}
        >

            <div style={{ minWidth: 70 }}>
                <div style={{ fontSize: 12, color: theme.subText }}>Gold</div>
                <motion.div
                    key={gold}
                    initial={{ scale: 1.2 }}
                    animate={{ scale: 1 }}
                    style={{ fontWeight: "bold" }}
                >
                    💰 {gold}
                </motion.div>
            </div>

            <div style={{ minWidth: 130 }}>
                <div style={{ fontSize: 12, color: theme.subText }}>Health</div>
                <motion.div
                    key={hp}
                    initial={{ scale: 1.15 }}
                    animate={{ scale: 1 }}
                    style={{ fontWeight: "bold", color: hpColor }}
                >
                    ❤️ {hp} / {maxhp}
                </motion.div>
                <div
                    style={{
                        height: 6,
                        marginTop: 6,
                        borderRadius: 999,
                        background: theme.isLight ? "rgba(0,0,0,0.08)" : "rgba(255,255,255,0.08)",
                        overflow: "hidden"
                    }}
                >
                    <motion.div
                        animate={{ width: `${hpPercent}%` }}
                        transition={{ duration: 0.4 }}
                        style={{ height: "100%", background: hpColor }}
                    />
                </div>
            </div>

            <div style={{ minWidth: 70 }}>
                <div style={{ fontSize: 12, color: theme.subText }}>Level</div>
                <motion.div
                    key={level}
                    initial={{ scale: 1.3 }}
                    animate={{ scale: 1 }}
                    style={{ fontWeight: "bold", color: "#facc15" }}
                >
                    ⭐ {level}
                </motion.div>
            </div>

            <div style={{ minWidth: 160 }}>
                <div style={{ fontSize: 12, color: theme.subText }}>
                    Progress to Level {level + 1}
                </div>
                <div
                    style={{
                        height: 8,
                        borderRadius: 999,
                        background: theme.isLight ? "rgba(0,0,0,0.08)" : "rgba(255,255,255,0.08)",
                        overflow: "hidden"
                    }}
                >
                    <motion.div
                        animate={{ width: `${xpPercent}%` }}
                        transition={{ duration: 0.5, ease: "easeOut" }}
                        style={{
                            height: "100%",
                            background: "linear-gradient(90deg, #6366f1, #8b5cf6)"
                        }}
                    />
                </div>
                <div style={{ fontSize: 11, color: theme.subText, marginTop: 4 }}>
                    XP {xp} / {xpNeeded}
                </div>
            </div>

        </motion.div>
    );
}
