import useGame from "./useGame";
import useGameActions from "./useGameActions";
import useAuthActions from "./useAuthActions";
import useToast from "./useToast";
import { useAuth } from "./useAuth";
import { useState } from "react";

export default function useGamePage() {
    const { token, playerId, login, logout } = useAuth();

    const [darkMode, setDarkMode] = useState(false);
    const toggleDarkMode = () => setDarkMode(prev => !prev);

    const {
        items,
        inventory,
        playerStats,
        loading,
        refreshGame,
        resetGame
    } = useGame(token, playerId);

    const { toasts, addToast } = useToast();

    const [buyingItem, setBuyingItem] = useState(null);
    const [sellingItem, setSellingItem] = useState(null);

    const {
        handleBuy,
        handleSell,
        fightData,
        loading: fightLoading,
        handleFight,
        clearFight
    } = useGameActions({
        playerId,
        refreshGame,
        addToast,
        setBuyingItem,
        setSellingItem
    });

    const { handleLogin, handleLogout } = useAuthActions({
        login,
        logout,
        addToast,
        resetGame,
        clearFight
    });

    return {
        // auth
        token,
        playerId,
        handleLogin,
        handleLogout,

        // game data
        items,
        inventory,
        playerStats,
        loading,
        refreshGame,
        resetGame,

        // actions
        handleBuy,
        handleSell,

        // combat
        fightData,
        fightLoading,
        handleFight,
        clearFight,

        // ui state
        buyingItem,
        sellingItem,

        // ui
        darkMode,
        toggleDarkMode,

        // toast
        toasts,
        addToast
    };
}