import { useState } from "react";
import { getPlayerById } from "../apiClient";

export default function usePlayerProfile() {
    const [player, setPlayer] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchPlayer = async (playerId) => {
        try {
            setLoading(true);
            setError(null);

            const data = await getPlayerById(playerId);

            setPlayer(data);

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const clearPlayer = () => {
        setPlayer(null);
        setError(null);
        setLoading(false);
    };


    return {
        player,
        loading,
        error,
        fetchPlayer,
        clearPlayer
    };
}