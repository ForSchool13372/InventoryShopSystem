import { AnimatePresence, motion } from "framer-motion";

export default function CombatLoot({
    isReplaying,
    items
}) {

    const getItemIcon = (name) => {
        const item = name.toLowerCase();

        if (item.includes("sword")) return "⚔️";
        if (item.includes("potion")) return "🧪";
        if (item.includes("armor")) return "🛡️";

        return "✨";
    };


    return (
        <AnimatePresence>
            {!isReplaying &&
                items?.length > 0 && (

                    <motion.div
                        initial={{
                            opacity: 0,
                            y: 15,
                            scale: 0.97
                        }}
                        animate={{
                            opacity: 1,
                            y: 0,
                            scale: 1
                        }}
                        exit={{
                            opacity: 0,
                            y: 15
                        }}
                        transition={{
                            duration: 0.35
                        }}
                        style={{
                            marginTop: "14px",
                            padding: "14px",
                            borderRadius: "16px",
                            background:
                                "linear-gradient(180deg, rgba(34,197,94,0.12), rgba(34,197,94,0.04))",
                            border:
                                "1px solid rgba(34,197,94,0.35)",
                            boxShadow:
                                "0 0 18px rgba(34,197,94,0.15)"
                        }}
                    >

                        <div
                            style={{
                                fontWeight: 900,
                                fontSize: "1rem",
                                marginBottom: "10px",
                                display: "flex",
                                alignItems: "center",
                                gap: "8px"
                            }}
                        >
                            🎁 Loot Dropped
                        </div>


                        <div
                            style={{
                                display: "flex",
                                flexDirection: "column",
                                gap: "8px"
                            }}
                        >

                            {items.map((item, i) => (

                                <motion.div
                                    key={i}
                                    initial={{
                                        opacity: 0,
                                        x: -10
                                    }}
                                    animate={{
                                        opacity: 1,
                                        x: 0
                                    }}
                                    transition={{
                                        delay: i * 0.1
                                    }}
                                    whileHover={{
                                        scale: 1.01,
                                        boxShadow: "0 0 12px rgba(34,197,94,0.25)"
                                    }}
                                    style={{
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "space-between",
                                        padding: "10px",
                                        borderRadius: "10px",
                                        background:
                                            "rgba(255,255,255,0.05)",
                                        border:
                                            "1px solid rgba(255,255,255,0.08)"
                                    }}
                                >

                                    <div
                                        style={{
                                            display: "flex",
                                            alignItems: "center",
                                            gap: "8px",
                                            fontWeight: 700
                                        }}
                                    >
                                        <span>
                                            {getItemIcon(item.itemName)}
                                        </span>

                                        <span>
                                            {
                                                item.itemName
                                                    .charAt(0)
                                                    .toUpperCase() +
                                                item.itemName.slice(1)
                                            }
                                        </span>
                                    </div>


                                    <div
                                        style={{
                                            fontWeight: 900,
                                            color: "#22c55e"
                                        }}
                                    >
                                        ×{item.qty}
                                    </div>

                                </motion.div>

                            ))}

                        </div>

                    </motion.div>

                )}
        </AnimatePresence>
    );
}