const API = import.meta.env.VITE_API_URL;

const TOKEN_KEY = "auth_token";

// =========================================================
// TOKEN STORAGE
// =========================================================
export const clearAuthToken = () => {
    localStorage.removeItem(TOKEN_KEY);
};

const getAuthToken = () => {
    return localStorage.getItem(TOKEN_KEY);
};

// =========================================================
// AUTH STATE
// =========================================================
export const isAuthenticated = () => {
    return !!getAuthToken();
};

// =========================================================
// CORE REQUEST WRAPPER
// =========================================================
export const apiRequest = async (url, options = {}) => {
    const token = getAuthToken();

    const headers = {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(options.headers || {})
    };

    let res;

    try {
        res = await fetch(url, {
            ...options,
            headers
        });
    } catch {
        throw new Error("Network error");
    }

    let data = null;

    const contentType = res.headers.get("content-type");
    if (contentType?.includes("application/json")) {
        try {
            data = await res.json();
        } catch {
            data = null;
        }
    }

    if (!res.ok) {
        const message =
            data?.detail ||
            data?.message ||
            `Request failed (${res.status})`;

        if (res.status === 401) {
            clearAuthToken();
        }

        throw new Error(message);
    }

    return data;
};

// =========================================================
// AUTH
// =========================================================
export const loginPlayer = (playerId) => {
    return apiRequest(`${API}/api/login`, {
        method: "POST",
        body: JSON.stringify({ playerId })
    });
};

// =========================================================
// PLAYER
// =========================================================
export const getPlayer = () => apiRequest(`${API}/api/player`);

export const getInventory = () => apiRequest(`${API}/api/inventory`);

export const getShop = () => apiRequest(`${API}/api/shop`);

// =========================================================
// GAME ACTIONS
// =========================================================
export const buyItem = (itemName, quantity = 1) =>
    apiRequest(`${API}/api/buy`, {
        method: "POST",
        body: JSON.stringify({ itemName, quantity })
    });

export const sellItem = (itemName, quantity = 1) =>
    apiRequest(`${API}/api/sell`, {
        method: "POST",
        body: JSON.stringify({ itemName, quantity })
    });

export const createLeaderboardSocket = (onMessage) => {
    const wsUrl = API.startsWith("https")
        ? API.replace("https", "wss") + "/api/ws/leaderboard"
        : API.replace("http", "ws") + "/api/ws/leaderboard";

    const ws = new WebSocket(wsUrl);

    ws.onmessage = (event) => {
        let data;
        try {
            data = JSON.parse(event.data);
        } catch {
            return;
        }

        onMessage({
            type: data.type,
            data: Array.isArray(data.data) ? data.data : []
        });
    };

    return ws;
};

export const startFight = () =>
    apiRequest(`${API}/api/fight`, {
        method: "POST"
    });