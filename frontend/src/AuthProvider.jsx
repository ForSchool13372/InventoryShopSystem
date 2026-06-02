import { useState } from "react";
import { AuthContext } from "./AuthContext";

const TOKEN_KEY = "auth_token";
const PLAYER_ID_KEY = "playerId";

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY) || "");
    const [playerId, setPlayerId] = useState(() => localStorage.getItem(PLAYER_ID_KEY) || "");

    const login = (jwt, id) => {
        setToken(jwt);
        setPlayerId(id);

        localStorage.setItem(TOKEN_KEY, jwt);
        localStorage.setItem(PLAYER_ID_KEY, id);
    };

    const logout = () => {
        setToken("");
        setPlayerId("");

        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(PLAYER_ID_KEY);
    };

    return (
        <AuthContext.Provider value={{ token, playerId, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};