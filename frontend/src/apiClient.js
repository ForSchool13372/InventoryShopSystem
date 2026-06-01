const API = import.meta.env.VITE_API_URL;

const TOKEN_KEY = "auth_token";

// =========================================================
// TOKEN STORAGE (single source of truth)
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
// CORE REQUEST WRAPPER (FIXED)
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

    // safe JSON parsing (prevents crashes)
    let data = null;
    const contentType = res.headers.get("content-type");

    if (contentType?.includes("application/json")) {
        try {
            data = await res.json();
        } catch {
            data = null;
        }
    }

    // =====================================================
    // GLOBAL ERROR HANDLING
    // =====================================================
    if (!res.ok) {
        const message =
            data?.detail ||
            data?.message ||
            `Request failed (${res.status})`;

        // IMPORTANT: handle expired/invalid token properly
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
    return apiRequest(`${API}/login`, {
        method: "POST",
        body: JSON.stringify({ playerId })
    });
};

// =========================================================
// PLAYER
// =========================================================
export const getPlayer = () => {
    return apiRequest(`${API}/player`);
};

// =========================================================
// INVENTORY
// =========================================================
export const getInventory = () => {
    return apiRequest(`${API}/inventory`);
};

// =========================================================
// SHOP
// =========================================================
export const getShop = () => {
    return apiRequest(`${API}/shop`);
};

// =========================================================
// BUY
// =========================================================
export const buyItem = (itemName, quantity = 1) => {
    return apiRequest(`${API}/buy`, {
        method: "POST",
        body: JSON.stringify({ itemName, quantity })
    });
};

// =========================================================
// SELL
// =========================================================
export const sellItem = (itemName, quantity = 1) => {
    return apiRequest(`${API}/sell`, {
        method: "POST",
        body: JSON.stringify({ itemName, quantity })
    });
};