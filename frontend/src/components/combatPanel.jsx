import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useMemo, useRef, useState } from "react";

export default function CombatPanel({
    theme,
    fightData,
    fightLoading,
    handleFight,
    clearFight
}) {
    const enemy = fightData?.enemy;

    const handleReset = () => {
        clearFight();
        setDisplayLog([]);
        setIsReplaying(false);
        prevLogRef.current = [];
    };

    const log = useMemo(() => fightData?.log ?? [], [fightData?.log]);

    const [displayLog, setDisplayLog] = useState([]);
    const [isReplaying, setIsReplaying] = useState(false);

    const prevLogRef = useRef([]);

    useEffect(() => {
        if (!fightData || fightLoading) return;
        if (!log.length) return;

        prevLogRef.current = [];
        setDisplayLog([]);
        setIsReplaying(true);

        let i = 0;
        const interval = setInterval(() => {
            setDisplayLog(prev => [...prev, log[i]]);
            i++;
            if (i >= log.length) {
                clearInterval(interval);
                setIsReplaying(false);
            }
        }, 400);

        return () => clearInterval(interval);
    }, [fightData, fightLoading, log]);


    const locked = fightLoading || isReplaying;

    return (
        <motion.div style={styles.card(theme)}>
            <div style={styles.title(theme)}>⚔️ BATTLE</div>

            <div style={styles.enemyBox}>
                👹 {enemy?.name ?? "Enemy Appears Here"}
            </div>

            <div style={styles.actions}>
                <button
                    style={{
                        ...styles.button,
                        opacity: locked ? 0.6 : 1,
                        cursor: locked ? "not-allowed" : "pointer"
                    }}
                    onClick={() => {
                        setDisplayLog([]);   // ← FIX: clear old logs instantly
                        setIsReplaying(true);   // immediately hide old loot
                        handleFight();       // then start the fight
                    }}
                    disabled={locked}
                >
                    {fightLoading
                        ? "Fighting..."
                        : isReplaying
                            ? "Battle in progress..."
                            : "⚔️ Attack"}
                </button>

                <button
                    style={{ ...styles.button, background: "#ef4444" }}
                    onClick={handleReset}
                    disabled={fightLoading || isReplaying}
                >
                    Reset
                </button>
            </div>

            <div style={styles.log}>
                {displayLog.length === 0 ? (
                    <div style={{ opacity: 0.6 }}>
                        No battle yet. Press Attack.
                    </div>
                ) : (
                    displayLog.map((line, i) => (
                        <div key={i}>{line}</div>
                    ))
                )}
            </div>

             
            <AnimatePresence>
                {!isReplaying && fightData?.items?.length > 0 && (
                    <motion.div
                        initial={{ opacity: 0, y: 6 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 6 }}
                        transition={{ duration: 0.25 }}
                        style={{
                            marginTop: "10px",
                            padding: "10px",
                            borderRadius: "8px",
                            background: "rgba(34,197,94,0.08)",
                            border: "1px solid rgba(34,197,94,0.25)",
                            fontSize: "0.8rem"
                        }}
                    >
                        <div style={{ fontWeight: 800, marginBottom: "6px" }}>
                            🎁 Loot Dropped
                        </div>

                        {fightData.items.map((item, i) => (
                            <div key={i}>
                                + {item.itemName.charAt(0).toUpperCase() + item.itemName.slice(1)} ×{item.qty}
                            </div>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}

// =========================
// STYLES (DEFINED PROPERLY)
// =========================
const styles = {
    card: (t) => ({
        padding: "14px",
        borderRadius: "12px",
        border: `1px solid ${t.subText}33`,
        background: t.cardBg,
        color: t.text,
        display: "flex",
        flexDirection: "column",
        gap: "12px"
    }),

    title: (t) => ({
        fontWeight: 900,
        fontSize: "0.95rem",
        letterSpacing: "1px",
        color: t.text
    }),

    enemyBox: {
        padding: "10px",
        borderRadius: "10px",
        background: "rgba(255,0,0,0.06)",
        border: "1px solid rgba(255,0,0,0.2)"
    },

    actions: {
        display: "flex",
        gap: "8px",
        marginTop: "6px"
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

    log: {
        marginTop: "6px",
        fontSize: "0.75rem",
        opacity: 0.9,
        padding: "10px",
        borderRadius: "8px",
        border: "1px solid rgba(255,255,255,0.08)",
        background: "rgba(0,0,0,0.15)",
        display: "flex",
        flexDirection: "column",
        gap: "6px",
        maxHeight: "220px",
        overflowY: "auto"
    }
};