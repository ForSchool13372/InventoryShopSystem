const API = import.meta.env.VITE_API_URL;

const TOKEN_KEY = "auth_token";

// =========================================================
// TOKEN STORAGE
// =========================================================
export const setAuthToken = (token) => {
    if (!token) return;
    localStorage.setItem(TOKEN_KEY, token);
};

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