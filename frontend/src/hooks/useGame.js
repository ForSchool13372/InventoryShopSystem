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

    // =========================================================
    // SINGLE SOURCE OF TRUTH FETCH
    // =========================================================
    const fetchGameState = useCallback(async () => {
        if (!shouldLoad) return;

        const [shop, inventoryData, player] = await Promise.all([
            getShop(),
            getInventory(),
            getPlayer()
        ]);

        setItems(
            (shop?.data ?? []).map(item => ({
                itemName: item.itemname,
                itemType: item.itemtype,
                rarity: item.rarity,
                description: item.description,
                stock: item.stock,
                price: item.price
            }))
        );

        setInventory(
            (inventoryData?.items ?? []).map(item => ({
                itemName: item.itemName ?? item.itemname,
                quantity: item.quantity ?? 0,
                itemType: item.itemType ?? item.itemtype,
                rarity: item.rarity,
                description: item.description,
                price: item.price
            }))
        );

        // SAFE PLAYER UPDATE
        if (player?.core) setPlayerStats(player);

    }, [shouldLoad]);

    // =========================================================
    // REFRESH (ONLY ONE)
    // =========================================================
    const refreshGame = useCallback(async () => {
        if (!shouldLoad) return;

        setLoading(true);
        try {
            await fetchGameState();
        } finally {
            setLoading(false);
        }
    }, [fetchGameState, shouldLoad]);

    // =========================================================
    // INITIAL LOAD
    // =========================================================
    useEffect(() => {
        if (!shouldLoad) return;

        let cancelled = false;

        const syncData = async () => {
            setLoading(true);
            try {
                await fetchGameState();
            } finally {
                if (!cancelled) setLoading(false);
            }
        };

        syncData();

        return () => {
            cancelled = true;
        };
    }, [shouldLoad, fetchGameState]);

    // =========================================================
    // RESET
    // =========================================================
    const resetGame = () => {
        setItems([]);
        setInventory([]);
        setPlayerStats(null);
    };

    // =========================================================
    // RETURN
    // =========================================================
    return {
        items,
        inventory,
        playerStats,
        loading,

        refreshGame,

        setItems,
        setInventory,
        setPlayerStats,

        resetGame
    };
}