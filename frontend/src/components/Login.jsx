import { useState } from "react";

function Login({ token, onLogin, onLogout, error, theme }) {
    const [inputPlayerId, setInputPlayerId] = useState("");
    const [loading, setLoading] = useState(false);

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

    // ----------------------------
    // STYLES
    // ----------------------------
    const cardStyle = {
        background: theme.cardBg,
        color: theme.text,
        padding: "22px",
        borderRadius: "16px",
        boxShadow: "0 12px 35px rgba(0,0,0,0.12)",
        border: "1px solid rgba(255,255,255,0.04)",
    };

    const titleStyle = {
        marginBottom: "12px",
        color: theme.text,
        fontWeight: "800",
        fontSize: "1.4rem",
        letterSpacing: "-0.02em"
    };

    const inputStyle = {
        flex: 1,
        padding: "11px 12px",
        borderRadius: "10px",
        border: `1px solid ${theme.subText}55`,
        outline: "none",
        background: theme.cardBg,
        color: theme.text,
        transition: "0.2s ease"
    };

    const buttonStyle = (active, color) => ({
        padding: "10px 14px",
        borderRadius: "10px",
        border: "none",
        fontWeight: "600",
        cursor: active ? "pointer" : "not-allowed",
        background: active ? color : "#9ca3af",
        color: "white",
        transition: "all 0.2s ease",
        transform: "translateY(0px)"
    });

    const isDisabled = loading || !inputPlayerId;

    // ----------------------------
    // LOGGED IN STATE
    // ----------------------------
    if (token) {
        return (
            <div style={cardStyle}>
                <h2 style={titleStyle}>Login</h2>

                <div style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center"
                }}>
                    <div style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                        fontWeight: "600",
                        color: "#22c55e"
                    }}>
                        <span style={{
                            width: "8px",
                            height: "8px",
                            borderRadius: "50%",
                            background: "#22c55e",
                            display: "inline-block"
                        }} />
                        Logged in
                    </div>

                    <button
                        onClick={handleLogoutClick}
                        style={buttonStyle(true, "#ef4444")}
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

    // ----------------------------
    // LOGIN FORM
    // ----------------------------
    return (
        <div style={cardStyle}>
            <h2 style={titleStyle}>Login</h2>

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
                    onFocus={(e) => {
                        e.target.style.border = "1px solid #4f46e5";
                        e.target.style.boxShadow = "0 0 0 3px rgba(79,70,229,0.15)";
                    }}
                    onBlur={(e) => {
                        e.target.style.border = `1px solid ${theme.subText}55`;
                        e.target.style.boxShadow = "none";
                    }}
                />

                <button
                    onClick={handleSubmit}
                    disabled={isDisabled}
                    style={buttonStyle(!isDisabled, "#4f46e5")}
                    onMouseEnter={(e) => {
                        if (!isDisabled) {
                            e.target.style.transform = "translateY(-1px)";
                            e.target.style.boxShadow = "0 8px 20px rgba(79,70,229,0.25)";
                        }
                    }}
                    onMouseLeave={(e) => {
                        e.target.style.transform = "translateY(0px)";
                        e.target.style.boxShadow = "none";
                    }}
                >
                    {loading ? "Logging in..." : "Login"}
                </button>
            </div>

            {error && (
                <div style={{
                    marginTop: "12px",
                    padding: "10px",
                    borderRadius: "10px",
                    background: "rgba(239,68,68,0.08)",
                    color: "#ef4444",
                    fontWeight: "500",
                    animation: "fadeIn 0.2s ease"
                }}>
                    {error}
                </div>
            )}
        </div>
    );
}

export default Login;