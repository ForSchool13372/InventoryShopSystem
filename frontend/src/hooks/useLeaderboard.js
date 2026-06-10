import { useEffect, useState, useRef } from "react";
import { createLeaderboardSocket } from "../apiClient";

export default function useLeaderboard(token) {
    const [data, setData] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const wsRef = useRef(null);

    useEffect(() => {
        if (!token) {
            if (wsRef.current) {
                wsRef.current.close();
                wsRef.current = null;
            }

            queueMicrotask(() => {
                setData([]);
                setError(null);
                setLoading(false);
            });

            return;
        }

        queueMicrotask(() => {
            setLoading(true);
            setError(null);
        });

        const ws = createLeaderboardSocket((newData) => {
            setData(newData || []);
            setLoading(false);
        });

        ws.onerror = () => {
            setError("Leaderboard connection error");
            setLoading(false);
        };

        wsRef.current = ws;

        return () => {
            if (wsRef.current) {
                wsRef.current.close();
                wsRef.current = null;
            }
        };
    }, [token]);

    return { data, error, loading };
}