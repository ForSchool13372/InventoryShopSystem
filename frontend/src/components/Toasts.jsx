import { AnimatePresence, motion } from "framer-motion";

export default function Toasts({ toasts }) {
    return (
        <div
            style={{
                position: "fixed",
                top: "20px",
                right: "20px",
                display: "flex",
                flexDirection: "column",
                gap: "10px",
                zIndex: 9999
            }}
        >
            <AnimatePresence>
                {toasts.map((toast) => (
                    <motion.div
                        key={toast.id}
                        initial={{ opacity: 0, x: 20, scale: 0.95 }}
                        animate={{ opacity: 1, x: 0, scale: 1 }}
                        exit={{ opacity: 0, x: 20, scale: 0.95 }}
                        style={{
                            padding: "10px 14px",
                            borderRadius: "12px",
                            color: "white",
                            fontWeight: "600",
                            background:
                                toast.type === "success"
                                    ? "#22c55e"
                                    : toast.type === "error"
                                        ? "#ef4444"
                                        : "#4f46e5",
                            boxShadow: "0 10px 25px rgba(0,0,0,0.25)"
                        }}
                    >
                        {toast.message}
                    </motion.div>
                ))}
            </AnimatePresence>
        </div>
    );
}