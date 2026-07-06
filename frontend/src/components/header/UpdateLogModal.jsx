import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import SectionCard from "./SectionCard";

export default function UpdateLogModal({ showUpdateLog, setShowUpdateLog, theme }) {

    const [tab, setTab] = useState("current");

    if (!showUpdateLog) return null;


    const tabStyle = (active) => ({
        padding: "10px 16px",
        borderRadius: "10px",
        cursor: "pointer",
        fontWeight: 700,
        background: active
            ? "linear-gradient(180deg, #4f46e5, #3730a3)"
            : "linear-gradient(180deg, rgba(40,40,50,0.6), rgba(25,25,30,0.7))",
        color: active ? "#fff" : theme.subText,
        border: `1px solid ${active ? "#4f46e5" : theme.subText + "22"}`,
        boxShadow: active ? "0 10px 25px rgba(79,70,229,0.25)" : "none",
        transition: "0.15s"
    });

    const fadeAnim = {
        initial: { opacity: 0, y: 6 },
        animate: { opacity: 1, y: 0 },
        exit: { opacity: 0, y: -6 },
        transition: { duration: 0.22 }
    };

    return (
        <div
            onClick={() => setShowUpdateLog(false)}
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
                {/* Title */}
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
                    Update Log
                </h2>

                <p style={{ color: "#f8fafc" }}>
                    Current build notes, features, and upcoming plans.
                </p>

                {/* TABS */}
                <div
                    style={{
                        display: "flex",
                        gap: "10px",
                        marginTop: "20px",
                        marginBottom: "10px"
                    }}
                >
                    <div style={tabStyle(tab === "current")} onClick={() => setTab("current")}>
                        📦 Current
                    </div>
                    <div style={tabStyle(tab === "planned")} onClick={() => setTab("planned")}>
                        🛠 Planned
                    </div>
                    <div style={tabStyle(tab === "patches")} onClick={() => setTab("patches")}>
                        📜 Patch Notes
                    </div>
                </div>

                {/* TAB CONTENT */}
                <AnimatePresence mode="wait">
                    {tab === "current" && (
                        <motion.div key="current" {...fadeAnim}>
                            <SectionCard title="📦 Current Build — v0.1" theme={theme}>
                                <ul style={{ margin: 0, paddingLeft: "20px" }}>
                                    <li>Inventory system</li>
                                    <li>Shop system</li>
                                    <li>Player Stats panel</li>
                                    <li>Light/Dark mode</li>
                                    <li>Click sound (quiet)</li>
                                    <li>New HeaderBar UI</li>
                                    <li>Login card polish</li>
                                    <li>Info modal</li>
                                </ul>
                            </SectionCard>
                        </motion.div>
                    )}

                    {tab === "planned" && (
                        <motion.div key="planned" {...fadeAnim}>
                            <SectionCard title="🛠 Planned Features" theme={theme}>
                                <ul style={{ margin: 0, paddingLeft: "20px" }}>
                                    <li>Settings modal</li>
                                    <li>Volume slider</li>
                                    <li>UI scale options</li>
                                    <li>Animations</li>
                                    <li>Quests system</li>
                                </ul>
                            </SectionCard>
                        </motion.div>
                    )}

                    {tab === "patches" && (
                        <motion.div key="patches" {...fadeAnim}>
                            <SectionCard title="📜 Future Patch Notes" theme={theme}>
                                Patch notes will appear here as new updates roll out.
                            </SectionCard>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* CLOSE BUTTON */}
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
                        onClick={() => setShowUpdateLog(false)}
                        style={{
                            padding: "10px 16px",
                            borderRadius: "10px",
                            border: "1px solid rgba(255,255,255,0.08)",
                            cursor: "pointer",
                            background:
                                "linear-gradient(180deg, #0ea5e9, #0284c7)",
                            color: "#fff",
                            fontWeight: "700",
                            boxShadow: "0 10px 25px rgba(14,165,233,0.25)"
                        }}
                    >
                        Close
                    </motion.button>
                </div>
            </motion.div>
        </div>
    );
}
