import { useState } from "react";

function Login({ token, onLogin, onLogout, error, theme }) {
    const [inputPlayerId, setInputPlayerId] = useState("");
    const [loading, setLoading] = useState(false);

    // ----------------------------
    // LOGIN HANDLER
    // ----------------------------
    const handleSubmit = async () => {
        if (!inputPlayerId || loading) return;

        setLoading(true);

        try {
            const result = await onLogin(inputPlayerId);

            if (result) {
                setInputPlayerId("");
            }

        } catch {
            // no sound here — App handles it
        } finally {
            setLoading(false);
        }
    };

    // ----------------------------
    // LOGOUT (NO SOUND HERE)
    // ----------------------------
    const handleLogoutClick = () => {
        onLogout();
    };

    // ----------------------------
    // STYLES
    // ----------------------------
    const cardStyle = {
        background: theme.cardBg,
        color: theme.text,
        padding: "20px",
        borderRadius: "16px",
        boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
        border: "1px solid rgba(0,0,0,0.05)"
    };

    const inputStyle = {
        flex: 1,
        padding: "10px 12px",
        borderRadius: "10px",
        border: `1px solid ${theme.subText}55`,
        outline: "none",
        background: theme.cardBg,
        color: theme.text
    };

    const buttonBase = {
        padding: "10px 14px",
        borderRadius: "10px",
        border: "none",
        fontWeight: "600"
    };

    const mutedText = {
        color: theme.subText,
        margin: 0
    };

    // ----------------------------
    // LOGGED IN STATE
    // ----------------------------
    if (token) {
        return (
            <div style={cardStyle}>
                <h2 style={{ marginBottom: "10px", color: theme.text }}>
                    Login
                </h2>

                <div style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center"
                }}>
                    <p style={mutedText}>Logged in ✔</p>

                    <button
                        onClick={handleLogoutClick}
                        style={{
                            ...buttonBase,
                            cursor: "pointer",
                            background: "#ef4444",
                            color: "white"
                        }}
                    >
                        Logout
                    </button>
                </div>
            </div>
        );
    }

    // ----------------------------
    // LOGIN FORM
    // ----------------------------
    return (
        <div style={cardStyle}>
            <h2 style={{ marginBottom: "10px", color: theme.text, fontWeight: "800" }}>
                Login
            </h2>

            <div style={{
                display: "flex",
                gap: "10px",
                flexWrap: "wrap"
            }}>
                <input
                    placeholder="Enter Player ID"
                    value={inputPlayerId}
                    onChange={(e) => setInputPlayerId(e.target.value)}
                    style={inputStyle}
                />

                <button
                    onClick={handleSubmit}
                    disabled={loading || !inputPlayerId}
                    style={{
                        ...buttonBase,
                        cursor: loading || !inputPlayerId ? "not-allowed" : "pointer",
                        background: loading || !inputPlayerId ? "#9ca3af" : "#4f46e5",
                        color: "white"
                    }}
                >
                    {loading ? "Logging in..." : "Login"}
                </button>
            </div>

            {error && (
                <p style={{
                    color: "#ef4444",
                    marginTop: "10px",
                    fontWeight: "500"
                }}>
                    {error}
                </p>
            )}
        </div>
    );
}

export default Login;