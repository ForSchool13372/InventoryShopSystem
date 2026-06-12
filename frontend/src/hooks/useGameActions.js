import soundSystem from "../utils/soundSystem";
import { buyItem, sellItem } from "../apiClient";

export default function useGameActions({
    refreshGameAfterTrade,   //  CHANGE THIS (was refreshAll)
    addToast,
    setBuyingItem,
    setSellingItem
}) {

    const handleBuy = async (itemName, quantity = 1) => {
        setBuyingItem(itemName);

        try {
            const res = await buyItem(itemName, quantity);

            await refreshGameAfterTrade(); //  CHANGE HERE

            const success = res?.success === true;

            if (success) {
                soundSystem.play("buy");
                addToast(`Bought ${itemName}`, "success");
            } else {
                soundSystem.play("error");
                addToast(res?.message || "Buy failed", "error");
            }

            return success;

        } catch (err) {
            soundSystem.play("error");
            addToast(err?.message || "Buy failed", "error");
            return false;

        } finally {
            setTimeout(() => setBuyingItem(null), 150);
        }
    };

    const handleSell = async (itemName, quantity = 1) => {
        setSellingItem(itemName);

        try {
            await sellItem(itemName, quantity);

            await refreshGameAfterTrade(); //  CHANGE HERE

            soundSystem.play("sell");
            addToast(`Sold ${itemName}`, "success");

        } catch (err) {
            soundSystem.play("error");
            addToast(err?.message || "Sell failed", "error");

        } finally {
            setTimeout(() => setSellingItem(null), 150);
        }
    };

    return {
        handleBuy,
        handleSell
    };
}