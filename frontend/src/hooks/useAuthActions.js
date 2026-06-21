import soundSystem from "../utils/soundSystem";
import { loginPlayer } from "../apiClient";

export default function useAuthActions({ login, logout, addToast, resetGame, clearFight }) {

    const handleLogin = async (id) => {
        try {
            if (!id) throw new Error("Missing ID");

            const res = await loginPlayer(id);

            const newToken = res?.token || res?.data?.token;

            if (!newToken) throw new Error("No token returned from server");

            login(newToken, id);

            soundSystem.play("success");
            addToast("Welcome back", "success");

            return true;

        } catch (err) {
            soundSystem.play("error");
            addToast(err?.message || "Invalid ID", "error");
            return false;
        }
    };

    const handleLogout = () => {
        logout();
        resetGame();
        clearFight();

        soundSystem.play("click");
        addToast("Logged out", "info");
    };

    return {
        handleLogin,
        handleLogout
    };
}