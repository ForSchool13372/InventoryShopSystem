import { motion } from "framer-motion";

export default function HeaderActions({
    darkMode,
    toggleDarkMode,
    setShowInfo,
    setShowUpdateLog
}) {
    return (
        <div style={{ display: "flex", gap: "10px" }}>

            {/* Update Log */}
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setShowUpdateLog(true)}
                style={{
                    padding: "8px 12px",
                    borderRadius: "10px",
                    border: "1px solid rgba(255,255,255,0.08)",
                    cursor: "pointer",
                    background: "linear-gradient(180deg, #0ea5e9, #0284c7)",
                    color: "#fff",
                    fontWeight: "700",
                    boxShadow: "0 10px 25px rgba(14,165,233,0.25)"
                }}
            >
                📝 Update Log
            </motion.button>

            {/* Info */}
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setShowInfo(true)}
                style={{
                    padding: "8px 12px",
                    borderRadius: "10px",
                    border: "1px solid rgba(255,255,255,0.08)",
                    cursor: "pointer",
                    background: "linear-gradient(180deg, #4f46e5, #3730a3)",
                    color: "#fff",
                    fontWeight: "700",
                    boxShadow: "0 10px 25px rgba(79,70,229,0.25)"
                }}
            >
                ℹ️ Info
            </motion.button>

            {/* Light / Dark */}
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={toggleDarkMode}
                style={{
                    padding: "8px 12px",
                    borderRadius: "10px",
                    border: "1px solid rgba(255,255,255,0.08)",
                    cursor: "pointer",
                    background: darkMode
                        ? "linear-gradient(180deg, #e5e7eb, #cbd5e1)"
                        : "linear-gradient(180deg, #111827, #0b1220)",
                    color: darkMode ? "#111827" : "#fff",
                    fontWeight: "700"
                }}
            >
                {darkMode ? "Light ☀️" : "Dark 🌙"}
            </motion.button>
        </div>
    );
}
