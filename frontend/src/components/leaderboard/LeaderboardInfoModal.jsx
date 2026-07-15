import { motion } from "framer-motion";
import SectionCard from "../header/SectionCard";

function LeaderboardInfoModal({
    onClose,
    theme
}) {
    return (
        <div
            onClick={onClose}
            style={{
                position: "fixed",
                inset: 0,

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
                    🏆 Leaderboard
                </h2>


                <p style={{ color: "#f8fafc" }}>
                    Compete against other players and climb the rankings.
                </p>


                <div style={{ marginTop: "18px" }}>

                    <SectionCard title="📈 Ranking" theme={theme}>
                        Players are ranked based on their progression, level,
                        and overall power.
                    </SectionCard>


                    <SectionCard title="⚔️ Progression" theme={theme}>
                        Fight enemies, earn XP, and level up to increase your
                        position on the leaderboard.
                    </SectionCard>


                    <SectionCard title="👤 Player Profiles" theme={theme}>
                        Click any player to view their stats, level, XP,
                        and progression details.
                    </SectionCard>


                    <SectionCard title="🏆 Goal" theme={theme}>
                        Grow stronger, compete with others, and reach the top
                        of the leaderboard.
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

                        onClick={onClose}

                        style={{
                            padding: "10px 16px",
                            borderRadius: "10px",

                            border:
                                "1px solid rgba(255,255,255,0.08)",

                            cursor: "pointer",

                            background:
                                "linear-gradient(180deg, #4f46e5, #3730a3)",

                            color: "#fff",
                            fontWeight: "700",

                            boxShadow:
                                "0 10px 25px rgba(79,70,indigo,0.25)"
                        }}
                    >
                        Close
                    </motion.button>
                </div>

            </motion.div>
        </div>
    );
}

export default LeaderboardInfoModal;