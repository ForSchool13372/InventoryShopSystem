import { useEffect, useState, useCallback } from "react";
import {
    getShop,
    getInventory,
    getPlayer
} from "../apiClient";

export default function useGame(token, playerId) {

    // =========================================================
    // STATE
    // =========================================================
    const [items, setItems] = useState([]);
    const [inventory, setInventory] = useState([]);
    const [playerStats, setPlayerStats] = useState(null);
    const [loading, setLoading] = useState(true);

    // =========================================================
    // LOADERS
    // =========================================================
    const loadShop = useCallback(async () => {
        const data = await getShop();
        setItems(data?.data ?? []);
    }, []);

    const loadInventory = useCallback(async () => {
        if (!token || !playerId) return;
        const data = await getInventory();
        setInventory(data?.items ?? []);
    }, [token, playerId]);

    const loadPlayerStats = useCallback(async () => {
        if (!token || !playerId) return;
        const data = await getPlayer();
        setPlayerStats(data ?? null);
    }, [token, playerId]);

    // =========================================================
    // GAME OPERATIONS
    // =========================================================
    const refreshAll = useCallback(async () => {
        if (!token || !playerId) return;

        await Promise.all([
            loadShop(),
            loadInventory(),
            loadPlayerStats()
        ]);
    }, [token, playerId, loadShop, loadInventory, loadPlayerStats]);

    const resetGame = () => {
        setItems([]);
        setInventory([]);
        setPlayerStats(null);
    };

    // =========================================================
    // INIT (SYNC ON LOGIN)
    // =========================================================
    useEffect(() => {
        if (!token) return;

        const syncData = async () => {
            setLoading(true);
            try {
                await refreshAll();
            } finally {
                setLoading(false);
            }
        };

        syncData();
    }, [token, refreshAll]);

    // =========================================================
    // RETURN
    // =========================================================
    return {
        items,
        inventory,
        playerStats,
        loading,
        refreshAll,
        setItems,
        setInventory,
        setPlayerStats,
        resetGame
    };
}