import { motion } from "framer-motion";
import { fadeUp } from "../animations";

export default function Header({
    token,
    playerId,
    darkMode,
    toggleDarkMode,
    theme
}) {
    return (
        <motion.div
            variants={fadeUp(0)}
            initial="hidden"
            animate="show"
            style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "24px"
            }}
        >
            <div>
                <h1
                    style={{
                        fontSize: "2rem",
                        fontWeight: "650",
                        margin: 0,
                        color: theme.text
                    }}
                >
                    Inventory Shop System
                </h1>

                <p
                    style={{
                        margin: "4px 0 0 0",
                        fontSize: "0.9rem",
                        color: theme.subText
                    }}
                >
                    {token ? `Logged in as ${playerId}` : "Start your journey today!"}
                </p>
            </div>

            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={toggleDarkMode}
                style={{
                    padding: "8px 12px",
                    borderRadius: "10px",
                    border: "none",
                    cursor: "pointer",
                    background: darkMode ? "#e5e7eb" : "#111827",
                    color: darkMode ? "#111827" : "#fff",
                    fontWeight: "600"
                }}
            >
                {darkMode ? "Light ☀️" : "Dark 🌙"}
            </motion.button>
        </motion.div>
    );
}