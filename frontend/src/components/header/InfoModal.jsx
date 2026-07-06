import { motion } from "framer-motion";
import SectionCard from "./SectionCard";

export default function InfoModal({ showInfo, setShowInfo, theme }) {
    if (!showInfo) return null;

    return (
        <div
            onClick={() => setShowInfo(false)}
            style={{
                position: "fixed",
                inset: 0,

                // PoE-style darkness
                background: "rgba(0,0,0,0.75)",
                backdropFilter: "blur(8px)",

                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                zIndex: 9999
            }}
        >
            <motion.div
                initial={{ opacity: 0, scale: 0.96 }}
                animate={{ opacity: 1, scale: 1 }}
                onClick={(e) => e.stopPropagation()}
                style={{
                    width: "min(720px, 92%)",
                    borderRadius: "16px",

                    background:
                        "linear-gradient(180deg, rgba(20,20,25,0.95), rgba(10,10,12,0.98))",

                    border: `1px solid ${theme.subText}22`,
                    boxShadow: "0 30px 100px rgba(0,0,0,0.7)",

                    padding: "26px",
                    color: theme.text
                }}
            >
                <h2
                    style={{
                        marginTop: 0,
                        fontSize: "1.4rem",
                        fontWeight: 800,
                        letterSpacing: "0.5px",
                        color: "#c7d2fe",
                        textShadow: "0 0 20px rgba(79,70,229,0.35)"
                    }}
                >
                    Welcome, Wanderer
                </h2>

                <p style={{ color: "#f8fafc" }}>
                    A dark RPG-inspired system of combat, loot, and progression.
                </p>

                <div style={{ marginTop: "18px" }}>
                    <SectionCard title="⚔️ Combat" theme={theme}>
                        Fight enemies to earn XP and gold. Power grows with each victory.
                    </SectionCard>

                    <SectionCard title="🛒 Shop" theme={theme}>
                        Spend gold on upgrades and equipment to strengthen your build.
                    </SectionCard>

                    <SectionCard title="🎒 Inventory" theme={theme}>
                        Manage gear, optimize loadout, and sell unwanted items.
                    </SectionCard>

                    <SectionCard title="📜 Quests" theme={theme}>
                        Complete objectives for rewards, progression, and rare loot.
                    </SectionCard>

                    <SectionCard title="🏆 Goal" theme={theme}>
                        Survive, scale power, and dominate the leaderboard.
                    </SectionCard>
                </div>

                <div
                    style={{
                        display: "flex",
                        justifyContent: "flex-end",
                        marginTop: "18px"
                    }}
                >
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setShowInfo(false)}
                        style={{
                            padding: "10px 16px",
                            borderRadius: "10px",
                            border: "1px solid rgba(255,255,255,0.08)",
                            cursor: "pointer",
                            background:
                                "linear-gradient(180deg, #4f46e5, #3730a3)",
                            color: "#fff",
                            fontWeight: "700",
                            boxShadow:
                                "0 10px 25px rgba(79,70,229,0.25)"
                        }}
                    >
                        Close
                    </motion.button>
                </div>
            </motion.div>
        </div>
    );
}