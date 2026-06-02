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
// HEADERS
// =========================================================
const getAuthHeaders = () => {
    const token = getAuthToken();

    if (!token) return {};

    return {
        Authorization: `Bearer ${token}`
    };
};

// =========================================================
// CORE REQUEST WRAPPER
// =========================================================
export const apiRequest = async (url, options = {}) => {
    const res = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...getAuthHeaders(),
            ...(options.headers || {})
        }
    });

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
export const getPlayer = () => {
    return apiRequest(`${API}/api/player`);
};

// =========================================================
// INVENTORY
// =========================================================
export const getInventory = () => {
    return apiRequest(`${API}/api/inventory`);
};

// =========================================================
// SHOP
// =========================================================
export const getShop = () => {
    return apiRequest(`${API}/api/shop`);
};

// =========================================================
// BUY
// =========================================================
export const buyItem = (itemName, quantity = 1) => {
    return apiRequest(`${API}/api/buy`, {
        method: "POST",
        body: JSON.stringify({ itemName, quantity })
    });
};

// =========================================================
// SELL
// =========================================================
export const sellItem = (itemName, quantity = 1) => {
    return apiRequest(`${API}/api/sell`, {
        method: "POST",
        body: JSON.stringify({ itemName, quantity })
    });
};