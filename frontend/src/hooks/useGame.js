import { useEffect, useState, useCallback } from "react";
import {
    getShop,
    getInventory,
    getPlayer
} from "../apiClient";

export default function useGame(token, playerId) {

    const [items, setItems] = useState([]);
    const [inventory, setInventory] = useState([]);
    const [playerStats, setPlayerStats] = useState(null);
    const [loading, setLoading] = useState(false);

    // =========================================================
    // RESET LOADING DURING RENDER (React 19 safe)
    // =========================================================
    const shouldLoad = token && playerId;

    if (!shouldLoad && loading) {
        // React 19 requires synchronous state updates to happen in render
        setLoading(false);
    }

    // =========================================================
    // LOADERS
    // =========================================================
    const loadShop = useCallback(async () => {
        const data = await getShop();
        setItems(data?.data ?? []);
    }, []);

    const loadInventory = useCallback(async () => {
        if (!shouldLoad) return;
        const data = await getInventory();
        setInventory(data?.items ?? []);
    }, [shouldLoad]);

    const loadPlayerStats = useCallback(async () => {
        if (!shouldLoad) return;
        const data = await getPlayer();
        setPlayerStats(data ?? null);
    }, [shouldLoad]);

    const refreshAll = useCallback(async () => {
        await Promise.all([
            loadShop(),
            loadInventory(),
            loadPlayerStats()
        ]);
    }, [loadShop, loadInventory, loadPlayerStats]);

    const resetGame = () => {
        setItems([]);
        setInventory([]);
        setPlayerStats(null);
    };

    // =========================================================
    // EFFECT (only async work allowed)
    // =========================================================
    useEffect(() => {
        if (!shouldLoad) return;

        let cancelled = false;

        const syncData = async () => {
            setLoading(true);
            try {
                await refreshAll();
            } finally {
                if (!cancelled) setLoading(false);
            }
        };

        syncData();

        return () => {
            cancelled = true;
        };
    }, [shouldLoad, refreshAll]);

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
