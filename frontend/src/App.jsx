//Use state = Store Data
//useEffect = run code when something happens like (load/update)
import { useEffect, useState } from "react";
import { useAuth } from "./useAuth";
function App() {
    const { token, playerId, login, logout } = useAuth();
    const [items, setItems] = useState([]);
    const [inventory, setInventory] = useState([]);
    const [error, setError] = useState(""); 
    const [playerStats, setPlayerStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [inputPlayerId, setInputPlayerId] = useState("");

    const API = "http://127.0.0.1:8000";

    // --------------------------------
    // HELPERS
    // --------------------------------
    const loadInventory = async (jwt, id) => {
        if (!jwt || !id) return;

        const res = await fetch(`${API}/inventory/${id}`, { 
            headers: {
                token: jwt
            }
        });

        const data = await res.json();
        setInventory(data.data.items);
    };

    const loadPlayerStats = async (jwt, id) => {
        if (!jwt || !id) return;

        const res = await fetch(`${API}/player/${id}`, {
            headers: { token: jwt }
        });

        const data = await res.json();
        setPlayerStats(data.data);
    }

    const refreshPlayerData = (jwt, id) => {
        loadInventory(jwt, id);
        loadPlayerStats(jwt, id);
    };

    const apiRequest = async (url, options = {}) => {
        const res = await fetch(url, options);
        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "Request Failed")
        }

        return data;
    };

    const refreshAll = async () => {
        if (!token || !playerId) return;

        refreshPlayerData(token, playerId);

        const shopData = await apiRequest(`${API}/shop`);
        setItems(shopData.data);
    };


    //useEffect = runs code automatically when something happens in React.
    //Async allows waiting code
    //Await = pauses until result comes
    // res = send result back to user
    //invRes inventory response
    //Headers extra info sent
    //Json way to send data between systems in clean text format
    //Try it, catch if it fails, finally always runs
    useEffect(() => {
        const init = async () => {
            setLoading(true);

            try {
                const data = await apiRequest(`${API}/shop`);
                setItems(data.data);

                if (token && playerId) {
                    const invData = await apiRequest(`${API}/inventory/${playerId}`, {
                        headers: { token }
                    });

                    setInventory(invData.data.items);

                    const statsData = await apiRequest(`${API}/player/${playerId}`, {
                        headers: { token }
                    });

                    setPlayerStats(statsData.data);
                }

            } catch (err) {
                console.error(err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        init();

    }, [token, playerId]);

    //Error handling
    useEffect(() => {
        if (!error) return;

        const timer = setTimeout(() => {
            setError("");
        }, 3000);

        return () => clearTimeout(timer);
    }, [error]);

    // --------------------------------
    // Login
    // --------------------------------
    const handleLogin = async (id) => {
        if (!id) return;

        try {
            setError(""); //Clear old errors immediately
            
            const data = await apiRequest(`${API}/login/${id}`, {
                method: "POST"
            });

            const jwt = data.data.token;

            login(jwt, id); //Context update

            setInputPlayerId(""); // Clear input after success

            refreshPlayerData(jwt, id);
        }
        catch (err) {
            setError(err.message);
        }
    };

    // --------------------------------
    // Logout Method
    // --------------------------------
    const handleLogout = () => {
        logout();
        setInventory([]);
        setPlayerStats(null);
        setItems([]);
        setError("");
    };

    // --------------------------------
    // Buy Item
    // --------------------------------
    const buyItem = async (itemName) => {
        if (!token || !playerId) return;

        try {
            const data = await apiRequest(`${API}/buy/${playerId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    token: token
                },
                body: JSON.stringify({
                    itemName,
                    quantity: 1
                })
            });

            setError("");

            if (data.success) {
                alert(`Bought ${itemName}`);
                refreshPlayerData(token, playerId);
                refreshAll();
            }
        } catch (err) {
            setError(err.message);
        }
    };

    // --------------------------------
    // Sell Item
    // --------------------------------
    const sellItem = async (itemName) => {
        if (!token || !playerId) return;

        try {
            const data = await apiRequest(`${API}/sell/${playerId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    token: token
                },
                body: JSON.stringify({
                    itemName,
                    quantity: 1
                })
            });

            setError("");

            if (data.success) {
                alert(`Sold ${itemName}`);
                refreshAll();
            }

        } catch (err) {
            setError(err.message);
        }
    };

    return (
        //Div is a container in HTML (HyperText Markup Language (The structure of a webpage))
        //Padding space inside the box and its border
        //h1 - Biggest title on a webpage
        //h2 - Second header title
        //JSX = JavaScript XML which is HTML-Style coding inside JavaScript for building UI (React)
        //? if this then do this the quesiton mark thing
        //e means event object so details of the event that just happened
        //onChange = do this when a value changes
        //Error UI under login UI
        // <p> paragraph of text
        <div style={{
            padding: "20px",
            minHeight: "100vh",
            background: "linear-gradient(180deg, #f5f7fb, #e9eef7)",
            fontFamily: "Arial",
            display: "flex",
            justifyContent: "center"
        }}>

            {/* CONTAINER CARD */}
            <div style={{
                width: "100%",
                maxWidth: "900px"
            }}>

                <h1 style={{
                    textAlign: "center",
                    color: "#111827",
                    marginBottom: "25px",
                    fontSize: "2.2rem",
                    fontWeight: "800",
                    letterSpacing: "0.5px"
                }}>
                    Inventory Shop System
                </h1>

                {loading && <p>Loading...</p>}

                {/* ---------------- LOGIN CARD ---------------- */}
                <div style={{
                    background: "#ffffff",
                    padding: "15px",
                    borderRadius: "10px",
                    boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
                    marginBottom: "20px"
                }}>
                    <h2>Login</h2>

                    {!token ? (
                        <div>
                            <input
                                placeholder="Player ID (1-3)"
                                value={inputPlayerId}
                                onChange={(e) => {
                                    setInputPlayerId(e.target.value);
                                    setError("");
                                }}
                                style={{
                                    padding: "8px",
                                    borderRadius: "6px",
                                    border: "1px solid #ddd",
                                    marginRight: "10px"
                                }}
                            />

                            <button
                                onClick={() => handleLogin(inputPlayerId)}
                                style={{
                                    padding: "8px 12px",
                                    background: "#4f46e5",
                                    color: "white",
                                    border: "none",
                                    borderRadius: "6px",
                                    cursor: "pointer"
                                }}
                            >
                                Login
                            </button>
                        </div>
                    ) : (
                        <>
                            <p>Logged In ✔</p>
                            <button
                                onClick={handleLogout}
                                style={{
                                    padding: "8px 12px",
                                    background: "#ef4444",
                                    color: "white",
                                    border: "none",
                                    borderRadius: "6px",
                                    cursor: "pointer"
                                }}
                            >
                                Logout
                            </button>
                        </>
                    )}

                    {error && (
                        <div style={{
                            marginTop: "10px",
                            padding: "10px",
                            background: "#fff1f2",
                            color: "#be123c",
                            border: "1px solid #fecdd3",
                            borderRadius: "8px"
                        }}>
                            ⚠ {error}
                        </div>
                    )}

                    {playerStats && (
                        <div style={{ marginTop: "10px" }}>
                            <h2>Stats</h2>
                            <p>Gold: {playerStats.gold}</p>
                            <p>HP: {playerStats.hp}</p>
                            <p>Level: {playerStats.level}</p>
                        </div>
                    )}
                </div>

                {/* ---------------- SHOP CARD ---------------- */}
                <div style={{
                    background: "#ffffff",
                    padding: "15px",
                    borderRadius: "10px",
                    boxShadow: "0 8px 20px rgba(0,0,0,0.08)",
                    marginBottom: "20px"
                }}>
                    <h2>Shop</h2>

                    <ul style={{ listStyle: "none", padding: 0 }}>
                        {items.map((item, index) => (
                            <li key={index} style={{
                                display: "flex",
                                justifyContent: "space-between",
                                padding: "8px 0",
                                borderBottom: "1px solid #eee"
                            }}>
                                <span>
                                    {item.itemName} - Stock: {item.stock}
                                </span>

                                {token && (
                                    <button
                                        onClick={() => buyItem(item.itemName)}
                                        style={{
                                            background: "#4f46e5",
                                            color: "white",
                                            border: "none",
                                            borderRadius: "6px",
                                            padding: "6px 10px",
                                            cursor: "pointer"
                                        }}
                                    >
                                        Buy
                                    </button>
                                )}
                            </li>
                        ))}
                    </ul>
                </div>

                {/* ---------------- INVENTORY CARD ---------------- */}
                {token && (
                    <div style={{
                        background: "#ffffff",
                        padding: "15px",
                        borderRadius: "10px",
                        boxShadow: "0 8px 20px rgba(0,0,0,0.08)"
                    }}>
                        <h2>Inventory</h2>

                        <button
                            onClick={() => loadInventory(token)}
                            style={{
                                marginBottom: "10px",
                                padding: "6px 10px",
                                borderRadius: "6px",
                                border: "none",
                                background: "#111827",
                                color: "white",
                                cursor: "pointer"
                            }}
                        >
                            Refresh Inventory
                        </button>

                        <ul>
                            {inventory.map((item, index) => (
                                <li key={index} style={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    marginBottom: "8px"
                                }}>
                                    <span>
                                        {item.itemName} x {item.quantity}
                                    </span>

                                    <button
                                        onClick={() => sellItem(item.itemName)}
                                        style={{
                                            background: "#ef4444",
                                            color: "white",
                                            border: "none",
                                            borderRadius: "6px",
                                            padding: "6px 10px",
                                            cursor: "pointer"
                                        }}
                                    >
                                        Sell
                                    </button>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

            </div>
        </div>
    );
}

export default App;