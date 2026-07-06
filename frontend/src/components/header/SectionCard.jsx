import { motion } from "framer-motion";

export default function SectionCard({ title, children, theme }) {
    return (
        <motion.div
            whileHover={{ y: -3, scale: 1.01 }}
            style={{
                padding: "14px 16px",
                borderRadius: "12px",

                background:
                    "linear-gradient(180deg, rgba(255,255,255,0.04), rgba(0,0,0,0.15))",

                border: `1px solid ${theme.subText}22`,
                boxShadow: "0 10px 30px rgba(0,0,0,0.35)",
                marginBottom: "12px",
                position: "relative",
                overflow: "hidden"
            }}
        >
            <div
                style={{
                    position: "absolute",
                    inset: 0,
                    pointerEvents: "none",
                    background:
                        "radial-gradient(circle at top left, rgba(79,70,229,0.15), transparent 60%)"
                }}
            />

            <h3
                style={{
                    margin: "0 0 6px 0",
                    fontSize: "1rem",
                    fontWeight: 800,
                    color: "#f8fafc",
                    letterSpacing: "0.3px",
                }}
            >
                {title}
            </h3>

            {/* Children text now matches the title color exactly */}
            <div
                style={{
                    margin: 0,
                    fontSize: "0.9rem",
                    color: "#f8fafc",
                    lineHeight: "1.45"
                }}
            >
                {children}
            </div>
        </motion.div>
    );
}
