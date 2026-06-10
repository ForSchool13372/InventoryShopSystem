import { useState } from "react";
import { AuthContext } from "./AuthContext";

const TOKEN_KEY = "auth_token";
const PLAYER_ID_KEY = "playerId";

const getInitialToken = () => {
    const t = localStorage.getItem(TOKEN_KEY);
    return t && t !== "null" && t !== "undefined" ? t : null;
};

const getInitialPlayerId = () => {
    const id = localStorage.getItem(PLAYER_ID_KEY);
    return id && id !== "null" && id !== "undefined" ? id : null;
};


export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(getInitialToken);
    const [playerId, setPlayerId] = useState(getInitialPlayerId);

    const login = (jwt, id) => {
        setToken(jwt);
        setPlayerId(id);

        localStorage.setItem(TOKEN_KEY, jwt);
        localStorage.setItem(PLAYER_ID_KEY, id);
    };

    const logout = () => {
        setToken(null);
        setPlayerId(null);

        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(PLAYER_ID_KEY);
    };

    return (
        <AuthContext.Provider
            value={{
                token,
                playerId,
                login,
                logout,
                isAuthenticated: !!token
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};
