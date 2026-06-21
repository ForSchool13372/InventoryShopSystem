import soundSystem from "../utils/soundSystem";
import { useState } from "react";
import { buyItem, sellItem, startFight } from "../apiClient";

export default function useGameActions({
    playerId,
    refreshGame,
    addToast,
    setBuyingItem,
    setSellingItem
}) {
    const [fightData, setFightData] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleBuy = async (itemName, quantity = 1) => {
        setBuyingItem(itemName);

        try {
            const res = await buyItem(itemName, quantity);

            await refreshGame?.();

            const success = res?.success === true;

            if (success) {
                soundSystem.play("buy");
                addToast?.(`Bought ${itemName}`, "success");
            } else {
                soundSystem.play("error");
                addToast?.(res?.message || "Buy failed", "error");
            }

            return success;

        } catch (err) {
            soundSystem.play("error");
            addToast?.(err?.message || "Buy failed", "error");
            return false;

        } finally {
            setTimeout(() => setBuyingItem?.(null), 150);
        }
    };

    const handleSell = async (itemName, quantity = 1) => {
        setSellingItem(itemName);

        try {
            await sellItem(itemName, quantity);

            await refreshGame?.();

            soundSystem.play("sell");
            addToast?.(`Sold ${itemName}`, "success");

        } catch (err) {
            soundSystem.play("error");
            addToast?.(err?.message || "Sell failed", "error");

        } finally {
            setTimeout(() => setSellingItem?.(null), 150);
        }
    };

    const handleFight = async () => {
        if (!playerId || loading) return false;

        soundSystem.play("click");

        setLoading(true);

        try {
            const res = await startFight();

            setFightData(res);

            await refreshGame?.();

            return true;

        } catch (err) {
            soundSystem.play("error");
            addToast?.(err?.message || "Fight failed", "error");
            return false;

        } finally {
            setLoading(false);
        }
    };

    const clearFight = () => {
        setFightData(null);
    };

    return {
        handleBuy,
        handleSell,
        fightData,
        loading,
        handleFight,
        clearFight
    };
}