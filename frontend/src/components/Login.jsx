import { useState } from "react";

function Login({ token, onLogin, onLogout, error }) {
    const [inputPlayerId, setInputPlayerId] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        if (!inputPlayerId || loading) return;

        try {
            setLoading(true);
            await onLogin(inputPlayerId);
            setInputPlayerId("");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{
            background: "#fff",
            padding: "20px",
            borderRadius: "14px",
            boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
            marginBottom: "20px",
            border: "1px solid rgba(0,0,0,0.05)"
        }}>
            <h2 style={{ marginBottom: "10px" }}>Login</h2>

            {!token ? (
                <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                    <input
                        placeholder="Player ID"
                        value={inputPlayerId}
                        onChange={(e) => setInputPlayerId(e.target.value)}
                        style={{
                            padding: "10px",
                            borderRadius: "8px",
                            border: "1px solid #ddd",
                            flex: 1,
                            outline: "none"
                        }}
                    />

                    <button
                        onClick={handleSubmit}
                        disabled={loading}
                        style={{
                            padding: "10px 14px",
                            borderRadius: "8px",
                            border: "none",
                            cursor: loading ? "not-allowed" : "pointer",
                            background: loading ? "#9ca3af" : "#4f46e5",
                            color: "white",
                            fontWeight: "600",
                            transition: "0.2s"
                        }}
                    >
                        {loading ? "Logging in..." : "Login"}
                    </button>
                </div>
            ) : (
                <div style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center"
                }}>
                    <p style={{ margin: 0 }}>Logged in ✔</p>

                    <button
                        onClick={onLogout}
                        style={{
                            padding: "8px 12px",
                            borderRadius: "8px",
                            border: "none",
                            cursor: "pointer",
                            background: "#ef4444",
                            color: "white",
                            fontWeight: "600"
                        }}
                    >
                        Logout
                    </button>
                </div>
            )}

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