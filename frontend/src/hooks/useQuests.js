import { useState, useEffect } from "react";
import { getQuests, claimQuest as claimQuestApi } from "../apiClient";

export const useQuests = (refreshGame) => {
    const [quests, setQuests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const refreshQuests = async () => {
        try {
            setLoading(true);
            const res = await getQuests();
            setQuests(res.quests || []);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const claimQuest = async (questName) => {
        await claimQuestApi(questName);
        await refreshQuests();
        await refreshGame?.();
    };

    useEffect(() => {
        // React 19 requires async work to be defined INSIDE the effect
        (async () => {
            try {
                setLoading(true);
                const res = await getQuests();
                setQuests(res.quests || []);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        })();
    }, []);

    return {
        quests,
        loading,
        error,
        refreshQuests,
        claimQuest
    };
};
