import { useState } from "react";
import { getLoginStyles } from "./loginStyles";

function Login({ token, onLogin, onLogout, error, theme }) {
    const [inputPlayerId, setInputPlayerId] = useState("");
    const [loading, setLoading] = useState(false);

    const styles = getLoginStyles(theme);

    const handleSubmit = async () => {
        if (!inputPlayerId || loading) return;

        setLoading(true);

        try {
            const result = await onLogin(inputPlayerId);
            if (result) setInputPlayerId("");
        } catch {
            // handled globally
        } finally {
            setLoading(false);
        }
    };

    const handleLogoutClick = () => onLogout();

    const isDisabled = loading || !inputPlayerId;

    if (token) {
        return (
            <div style={styles.card}>
                <h2 style={styles.title}>Login</h2>

                <div style={styles.loggedInRow}>
                    <div style={styles.loggedInStatus}>
                        <span style={styles.statusDot} />
                        Logged in
                    </div>

                    <button
                        onClick={handleLogoutClick}
                        style={styles.button(true, "#ef4444")}
                        onMouseEnter={(e) => {
                            e.target.style.transform = "translateY(-1px)";
                        }}
                        onMouseLeave={(e) => {
                            e.target.style.transform = "translateY(0px)";
                        }}
                    >
                        Logout
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div style={styles.card}>
            <h2 style={styles.title}>Login</h2>

            <div style={styles.formRow}>
                <input
                    placeholder="Enter Player ID"
                    value={inputPlayerId}
                    onChange={(e) => setInputPlayerId(e.target.value)}
                    style={styles.input}
                    onFocus={(e) => {
                        e.target.style.border = "1px solid #4f46e5";
                        e.target.style.boxShadow =
                            "0 0 0 3px rgba(79,70,229,0.15)";
                    }}
                    onBlur={(e) => {
                        e.target.style.border =
                            `1px solid ${theme.subText}55`;
                        e.target.style.boxShadow = "none";
                    }}
                />

                <button
                    onClick={handleSubmit}
                    disabled={isDisabled}
                    style={styles.button(!isDisabled, "#4f46e5")}
                    onMouseEnter={(e) => {
                        if (!isDisabled) {
                            e.target.style.transform =
                                "translateY(-1px)";
                            e.target.style.boxShadow =
                                "0 8px 20px rgba(79,70,229,0.25)";
                        }
                    }}
                    onMouseLeave={(e) => {
                        e.target.style.transform =
                            "translateY(0px)";
                        e.target.style.boxShadow = "none";
                    }}
                >
                    {loading ? "Logging in..." : "Login"}
                </button>
            </div>

            {error && (
                <div style={styles.error}>
                    {error}
                </div>
            )}
        </div>
    );
}

export default Login;