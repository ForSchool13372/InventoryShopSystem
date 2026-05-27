import { useState } from "react";
import { AuthContext } from "./AuthContext";

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(() => localStorage.getItem("token") || "");
    const [playerId, setPlayerId] = useState(() => localStorage.getItem("playerId") || "");

    const login = (jwt, id) => {
        setToken(jwt);
        setPlayerId(id);
        localStorage.setItem("token", jwt);
        localStorage.setItem("playerId", id);
    };

    const logout = () => {
        setToken("");
        setPlayerId("");
        localStorage.removeItem("token");
        localStorage.removeItem("playerId");
    };

    return (
        <AuthContext.Provider value={{ token, playerId, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};