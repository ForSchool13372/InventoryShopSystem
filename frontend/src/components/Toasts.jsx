import { AnimatePresence, motion } from "framer-motion";

export default function Toasts({ toasts }) {
    return (
        <div
            style={{
                position: "fixed",
                top: "24px",
                right: "24px",
                display: "flex",
                flexDirection: "column",
                gap: "12px",
                zIndex: 9999
            }}
        >
            <AnimatePresence>
                {toasts.map((toast) => {
                    const colors =
                        toast.type === "success"
                            ? {
                                bg: "linear-gradient(145deg, rgba(34,197,94,0.95), rgba(21,128,61,0.95))",
                                border: "rgba(134,239,172,0.5)",
                                glow: "rgba(34,197,94,0.35)"
                            }
                            : toast.type === "error"
                                ? {
                                    bg: "linear-gradient(145deg, rgba(239,68,68,0.95), rgba(153,27,27,0.95))",
                                    border: "rgba(252,165,165,0.5)",
                                    glow: "rgba(239,68,68,0.35)"
                                }
                                : {
                                    bg: "linear-gradient(145deg, rgba(99,102,241,0.95), rgba(55,48,163,0.95))",
                                    border: "rgba(165,180,252,0.5)",
                                    glow: "rgba(99,102,241,0.35)"
                                };

                    return (
                        <motion.div
                            key={toast.id}
                            initial={{
                                opacity: 0,
                                x: 60,
                                scale: 0.85
                            }}
                            animate={{
                                opacity: 1,
                                x: 0,
                                scale: 1
                            }}
                            exit={{
                                opacity: 0,
                                x: 60,
                                scale: 0.85
                            }}
                            transition={{
                                type: "spring",
                                stiffness: 300,
                                damping: 22
                            }}
                            style={{
                                minWidth: "260px",
                                padding: "14px 18px",
                                borderRadius: "14px",
                                color: "white",
                                fontWeight: 800,
                                letterSpacing: "0.3px",
                                background: colors.bg,
                                border: `1px solid ${colors.border}`,
                                backdropFilter: "blur(12px)",
                                boxShadow: `
                                    0 12px 35px rgba(0,0,0,0.45),
                                    0 0 25px ${colors.glow},
                                    inset 0 1px 0 rgba(255,255,255,0.25)
                                `,
                                display: "flex",
                                alignItems: "center",
                                gap: "10px"
                            }}
                        >
                            {toast.message}
                        </motion.div>
                    );
                })}
            </AnimatePresence>
        </div>
    );
}