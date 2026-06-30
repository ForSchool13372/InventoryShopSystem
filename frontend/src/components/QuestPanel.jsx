import { motion } from "framer-motion";
import { useQuests } from "../hooks/useQuests";
import soundSystem from "../utils/soundSystem";

export const QuestPanel = ({ theme, refreshGame }) => {
    const { quests, loading, error, refreshQuests, claimQuest } = useQuests(refreshGame);

    const getQuestState = (q) => {
        if (q.claimed) return "claimed";
        if (!q.unlocked) return "locked";
        if (q.completed) return "completed";
        return "progress";
    };

    return (
        <motion.div style={styles.card(theme)}>
            <div style={styles.title(theme)}>📜 QUESTS</div>

            <div style={styles.actions}>
                <button
                    style={styles.button}
                    onClick={() => {
                        soundSystem.play("click");
                        refreshQuests();
                    }}
                >
                    Refresh
                </button>

            </div>

            <div style={styles.list}>
                {loading && <div style={{ opacity: 0.6 }}>Loading quests...</div>}
                {error && <div style={{ color: "#ef4444" }}>Error: {error}</div>}
                {!loading && !error && quests.length === 0 && (
                    <div style={{ opacity: 0.6 }}>No quests available.</div>
                )}

                {!loading && !error && quests.map((q, i) => {
                    const state = getQuestState(q);
                    const isLocked = state === "locked";

                    return (
                        <div
                            key={i}
                            style={{
                                ...styles.questCard(theme),
                                opacity: isLocked ? 0.4 : 1,
                                filter: isLocked ? "grayscale(1)" : "none"
                            }}
                        >
                            {isLocked ? (
                                <div style={styles.lockedMessage}>
                                    🔒
                                    <div style={{ marginTop: "6px" }}>
                                        Complete the previous quest
                                    </div>
                                    <div>to unlock</div>
                                </div>
                            ) : (
                                <>
                                    {/* HEADER */}
                                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                        <div style={styles.questName}>{q.name}</div>

                                        <div style={{
                                            fontSize: "0.7rem",
                                            padding: "3px 8px",
                                            borderRadius: "999px",
                                            background:
                                                state === "completed"
                                                    ? "#22c55e"
                                                    : state === "progress"
                                                        ? "#f59e0b"
                                                        : "#6b7280",
                                            color: "black",
                                            fontWeight: 800
                                        }}>
                                            {state === "progress" && "IN PROGRESS"}
                                            {state === "completed" && "READY"}
                                            {state === "claimed" && "CLAIMED"}
                                        </div>
                                    </div>

                                    {/* OBJECTIVE BLOCK */}
                                    <div style={styles.sectionTitle(theme)}>Objective</div>

                                    <div style={{
                                        display: "flex",
                                        flexDirection: "column",
                                        gap: "4px",
                                        fontSize: "0.8rem"
                                    }}>
                                        <div>Enemy: <b>{q.targetenemy.charAt(0).toUpperCase() + q.targetenemy.slice(1)}</b></div>
                                        <div>🎯 Target: <b>{q.target}</b></div>

                                        <div>
                                            ⚔️ Progress: <b>{q.progress}/{q.target}</b>
                                        </div>

                                        <div style={{
                                            height: "6px",
                                            background: "#1f2937",
                                            borderRadius: "999px",
                                            overflow: "hidden",
                                            marginTop: "6px"
                                        }}>
                                            <div
                                                style={{
                                                    height: "100%",
                                                    width: `${(q.progress / q.target) * 100}%`,
                                                    background: "#22c55e"
                                                }}
                                            />
                                        </div>
                                    </div>

                                    {/* REWARDS */}
                                    <div style={styles.sectionTitle(theme)}>Rewards</div>

                                    <div style={{
                                        display: "flex",
                                        justifyContent: "space-between",
                                        fontSize: "0.8rem"
                                    }}>
                                        <div>✨ XP: <b>{q.rewardxp}</b></div>
                                        <div>💰 Gold: <b>{q.rewardgold}</b></div>
                                    </div>

                                        {/* ACTION */}
                                        <div style={{
                                            marginTop: "6px",
                                            display: "flex",
                                            justifyContent: "flex-end"
                                        }}>
                                            {state !== "claimed" && (
                                                <button
                                                    onClick={() => {
                                                        if (state === "completed") {
                                                            soundSystem.play("success");
                                                            claimQuest(q.name);
                                                        }
                                                    }}
                                                    disabled={state !== "completed"}
                                                    style={{
                                                        ...styles.claimButton,
                                                        opacity: state === "completed" ? 1 : 0.5,
                                                        cursor: state === "completed" ? "pointer" : "not-allowed",
                                                        background:
                                                            state === "completed"
                                                                ? "#22c55e"
                                                                : "#374151",
                                                        color: state === "completed" ? "black" : "#9ca3af",
                                                        width: "100%"
                                                    }}
                                                >
                                                    {state === "completed"
                                                        ? "Claim Reward"
                                                        : "Not Ready"}
                                                </button>
                                            )}
                                        </div>
                                </>
                            )}
                        </div>
                    );
                })}
            </div>
        </motion.div>
    );
};

const styles = {
    card: (t) => ({
        padding: "16px",
        borderRadius: "12px",
        border: `1px solid ${t.subText}33`,
        background: t.cardBg,
        color: t.text,
        display: "flex",
        flexDirection: "column",
        gap: "14px"
    }),

    title: (t) => ({
        fontWeight: 900,
        fontSize: "1rem",
        letterSpacing: "1px",
        color: t.text
    }),

    lockedMessage: {
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        minHeight: "220px",
        fontWeight: 900,
        fontSize: "1rem",
        lineHeight: "1.5"
    },

    actions: {
        display: "flex",
        gap: "8px",
        marginTop: "4px"
    },

    button: {
        flex: 1,
        padding: "10px",
        borderRadius: "8px",
        border: "none",
        cursor: "pointer",
        background: "#4f46e5",
        color: "white",
        fontWeight: 800
    },

    claimButton: {
        padding: "6px 10px",
        borderRadius: "6px",
        border: "none",
        cursor: "pointer",
        background: "#22c55e",
        color: "black",
        fontWeight: 800,
        fontSize: "0.75rem"
    },

    list: {
        marginTop: "6px",
        fontSize: "0.85rem",
        display: "flex",
        flexDirection: "column",
        gap: "12px",
        maxHeight: "40vh",
        overflowY: "auto",
        paddingRight: "4px"
    },

    questCard: (t) => ({
        padding: "16px",
        borderRadius: "10px",
        border: `1px solid ${t.subText}33`,
        background: "rgba(255,255,255,0.06)",
        display: "flex",
        flexDirection: "column",
        gap: "10px"
    }),

    questName: {
        fontWeight: 900,
        fontSize: "0.95rem",
        marginBottom: "4px"
    },

    sectionTitle: (t) => ({
        marginTop: "4px",
        fontWeight: 700,
        fontSize: "0.75rem",
        opacity: 0.8,
        borderBottom: `1px solid ${t.subText}33`,
        paddingBottom: "2px"
    }),

    row: {
        display: "flex",
        justifyContent: "space-between",
        fontSize: "0.8rem",
        opacity: 0.95
    }
};