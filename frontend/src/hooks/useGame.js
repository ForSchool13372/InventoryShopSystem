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

    const shouldLoad = token && playerId;

    if (!shouldLoad && loading) {
        setLoading(false);
    }

    // =========================================================
    // INDIVIDUAL LOADERS
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

    // =========================================================
    // REFRESH STRATEGIES
    // =========================================================
    const refreshAll = useCallback(async () => {
        await Promise.all([
            loadShop(),
            loadInventory(),
            loadPlayerStats()
        ]);
    }, [loadShop, loadInventory, loadPlayerStats]);

    const refreshGameAfterTrade = useCallback(async () => {
        await Promise.all([
            loadShop(),        // stock changed
            loadInventory(),   // items changed
            loadPlayerStats()  // gold/XP changed
        ]);
    }, [loadShop, loadInventory, loadPlayerStats]);

    const refreshInventoryOnly = useCallback(async () => {
        await loadInventory();
    }, [loadInventory]);

    const refreshPlayerOnly = useCallback(async () => {
        await loadPlayerStats();
    }, [loadPlayerStats]);

    const resetGame = () => {
        setItems([]);
        setInventory([]);
        setPlayerStats(null);
    };

    // =========================================================
    // INITIAL LOAD
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

        // full
        refreshAll,

        // smarter UX ones
        refreshGameAfterTrade,
        refreshInventoryOnly,
        refreshPlayerOnly,

        // setters (optional keep)
        setItems,
        setInventory,
        setPlayerStats,

        resetGame
    };
}