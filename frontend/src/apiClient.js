const API = import.meta.env.VITE_API_URL;

// ----------------------------
// Generic request wrapper
// ----------------------------
export const apiRequest = async (url, options = {}) => {
    const res = await fetch(url, options);
    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || "Request Failed");
    }

    return data;
};

// ----------------------------
// AUTH
// ----------------------------
export const loginPlayer = (playerId) => {
    return apiRequest(`${API}/login/${playerId}`, {
        method: "POST"
    });
};

// ----------------------------
// PLAYER
// ----------------------------
export const getPlayer = (playerId, token) => {
    return apiRequest(`${API}/player/${playerId}`, {
        headers: { token }
    });
};

// ----------------------------
// INVENTORY
// ----------------------------
export const getInventory = (playerId, token) => {
    return apiRequest(`${API}/inventory/${playerId}`, {
        headers: { token }
    });
};

// ----------------------------
// SHOP
// ----------------------------
export const getShop = () => {
    return apiRequest(`${API}/shop`);
};

// ----------------------------
// BUY / SELL
// ----------------------------
export const buyItem = (playerId, token, itemName, quantity = 1) => {
    return apiRequest(`${API}/buy/${playerId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            token
        },
        body: JSON.stringify({
            itemName,
            quantity
        })
    });
};

export const sellItem = (playerId, token, itemName, quantity = 1) => {
    return apiRequest(`${API}/sell/${playerId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            token
        },
        body: JSON.stringify({
            itemName,
            quantity
        })
    });
};