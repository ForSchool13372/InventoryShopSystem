import { motion } from "framer-motion";
import { useQuests } from "../../hooks/useQuests";
import soundSystem from "../../utils/soundSystem";
import { styles } from "./questPanelStyles";
import QuestCard from "./QuestCard";

export const QuestPanel = ({ theme, refreshGame }) => {
    const { quests, loading, error, refreshQuests, claimQuest } = useQuests(refreshGame);

    return (
        <motion.div style={styles.card(theme)}>
            <div style={styles.title(theme)}>📜 QUESTS</div>

            <div style={styles.actions}>
                <motion.button
                    whileHover={{
                        scale: 1.03,
                        y: -2,
                        boxShadow: "0 0 28px rgba(99,102,241,0.45)"
                    }}
                    whileTap={{
                        scale: 0.97
                    }}
                    transition={{ duration: 0.18 }}
                    style={styles.button}
                    onClick={() => {
                        soundSystem.play("click");
                        refreshQuests();
                    }}
                >
                    🔄 Refresh Quests
                </motion.button>
            </div>

            <div style={styles.list}>
                {loading && (
                    <div style={{ opacity: 0.6 }}>
                        Loading quests...
                    </div>
                )}

                {error && (
                    <div style={{ color: "#ef4444" }}>
                        Error: {error}
                    </div>
                )}

                {!loading && !error && quests.length === 0 && (
                    <div style={{ opacity: 0.6 }}>
                        No quests available.
                    </div>
                )}

                {!loading && !error && quests.map((q, i) => (
                    <QuestCard
                        key={i}
                        quest={q}
                        theme={theme}
                        claimQuest={claimQuest}
                    />
                ))}
            </div>
        </motion.div>
    );
};