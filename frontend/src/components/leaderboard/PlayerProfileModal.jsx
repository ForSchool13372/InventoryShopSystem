import { motion } from "framer-motion";
import { getPlayerProfileStyles } from "./playerProfileStyles";

function PlayerProfileModal({
    player,
    playerId,
    loading,
    error,
    onClose,
    theme
}) {

    if (!player && !loading && !error) {
        return null;
    }

    const styles = getPlayerProfileStyles(theme);

    const {
        core = {},
        progression = {},
        combat = {}
    } = player || {};


    const xpPercent = Math.min(
        100,
        ((progression.xp ?? 0) / 100) * 100
    );

    const hpPercent = Math.min(
        100,
        ((core.hp ?? 0) / (core.maxhp || 1)) * 100
    );


    return (
        <div
            onClick={onClose}
            style={styles.overlay}
        >

            <motion.div
                onClick={(e) => e.stopPropagation()}
                initial={{
                    opacity: 0,
                    scale: 0.9,
                    y: 30
                }}
                animate={{
                    opacity: 1,
                    scale: 1,
                    y: 0
                }}
                transition={{
                    duration: 0.25
                }}
                style={styles.modal}
            >


                {/* TITLE */}
                <div style={styles.title}>

                    <h2
                        style={{
                            margin: 0,
                            fontSize: "1.8rem",
                            fontWeight: 950,
                            color: theme.text
                        }}
                    >
                        🧍 Player {playerId ?? ""}
                    </h2>


                    <p style={styles.subtitle}>
                        Adventurer Profile
                    </p>

                </div>



                {loading && (
                    <p style={{ color: theme.subText }}>
                        Loading profile...
                    </p>
                )}



                {error && (
                    <p style={{ color: "#ef4444" }}>
                        {error}
                    </p>
                )}



                {player && (

                    <>


                        {/* LEVEL */}
                        <div style={styles.section}>

                            <h3 style={{
                                marginTop: 0,
                                marginBottom: "14px"
                            }}>
                                ⭐ Level {progression.level ?? 1}
                            </h3>


                            <div style={styles.progressBackground}>

                                <div
                                    style={styles.xpBar(xpPercent)}
                                />

                            </div>


                            <p style={{
                                marginBottom: 0,
                                marginTop: "10px",
                                fontWeight: 700
                            }}>
                                XP {progression.xp ?? 0}/100
                            </p>


                        </div>




                        {/* CORE */}
                        <div style={styles.section}>

                            <h3 style={{
                                marginTop: 0
                            }}>
                                🛡️ Vital Stats
                            </h3>


                            <div style={styles.statRow}>
                                <span>❤️ Health</span>

                                <span>
                                    {core.hp ?? 0}/{core.maxhp ?? 0}
                                </span>
                            </div>



                            <div style={styles.progressBackground}>

                                <div
                                    style={styles.hpBar(hpPercent)}
                                />

                            </div>



                            <div style={{
                                ...styles.statRow,
                                marginTop: "12px"
                            }}>

                                <span>💰 Gold</span>

                                <span>
                                    {core.gold ?? 0}
                                </span>

                            </div>


                        </div>

                        {/* COMBAT */}
                        <div style={styles.section}>

                            <h3 style={{
                                marginTop: 0
                            }}>
                                ⚔ Combat Attributes
                            </h3>



                            <div style={styles.statRow}>
                                <span>Attack</span>
                                <span>
                                    {combat.attack ?? 0}
                                </span>
                            </div>


                            <div style={styles.statRow}>
                                <span>Defense</span>
                                <span>
                                    {combat.defense ?? 0}
                                </span>
                            </div>


                            <div style={styles.statRow}>
                                <span>Critical Chance</span>
                                <span>
                                    {((combat.critchance ?? 0) * 100).toFixed(0)}%
                                </span>
                            </div>


                            <div style={styles.statRow}>
                                <span>Critical Damage</span>
                                <span>
                                    x{combat.critmultiplier ?? 0}
                                </span>
                            </div>


                        </div>


                    </>

                )}

                <button
                    onClick={onClose}
                    style={styles.closeButton}
                >
                    Close
                </button>


            </motion.div>

        </div>
    );
}

export default PlayerProfileModal;