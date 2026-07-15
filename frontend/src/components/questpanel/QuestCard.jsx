import soundSystem from "../../utils/soundSystem";
import { styles } from "./questPanelStyles";

export default function QuestCard({
    quest,
    theme,
    claimQuest
}) {
    const getQuestState = (q) => {
        if (q.claimed) return "claimed";
        if (!q.unlocked) return "locked";
        if (q.completed) return "completed";
        return "progress";
    };

    const state = getQuestState(quest);
    const isLocked = state === "locked";

    return (
        <div
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
                    <div style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center"
                    }}>
                        <div style={styles.questName}>
                            {quest.name}
                        </div>

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

                    {/* OBJECTIVE */}
                    <div style={styles.sectionTitle(theme)}>
                        Objective
                    </div>

                    <div style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: "4px",
                        fontSize: "0.8rem"
                    }}>
                        <div>
                            Enemy: <b>
                                {quest.targetenemy.charAt(0).toUpperCase() + quest.targetenemy.slice(1)}
                            </b>
                        </div>

                        <div>
                            🎯 Target: <b>{quest.target}</b>
                        </div>

                        <div>
                            ⚔️ Progress: <b>{quest.progress}/{quest.target}</b>
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
                                    width: `${(quest.progress / quest.target) * 100}%`,
                                    background: "#22c55e"
                                }}
                            />
                        </div>
                    </div>

                    {/* REWARDS */}
                    <div style={styles.sectionTitle(theme)}>
                        Rewards
                    </div>

                    <div style={{
                        display: "flex",
                        justifyContent: "space-between",
                        fontSize: "0.8rem"
                    }}>
                        <div>
                            ✨ XP: <b>{quest.rewardxp}</b>
                        </div>

                        <div>
                            💰 Gold: <b>{quest.rewardgold}</b>
                        </div>
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
                                        claimQuest(quest.name);
                                    }
                                }}
                                disabled={state !== "completed"}
                                style={{
                                    ...styles.claimButton,
                                    opacity: state === "completed" ? 1 : 0.5,
                                    cursor: state === "completed"
                                        ? "pointer"
                                        : "not-allowed",
                                    background:
                                        state === "completed"
                                            ? "#22c55e"
                                            : "#374151",
                                    color:
                                        state === "completed"
                                            ? "black"
                                            : "#9ca3af",
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
}