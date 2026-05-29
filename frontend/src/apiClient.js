const API = import.meta.env.VITE_API_URL;

// ----------------------------
// Generic request wrapper
// ----------------------------
export const apiRequest = async (url, options = {}) => {
    const res = await fetch(url, options);

    let data;
    try {
        data = await res.json();
    } catch {
        data = {};
    }

    if (!res.ok) {
        throw new Error(
            data.detail ||
            data.message ||
            JSON.stringify(data) ||
            "Request Failed"
        );
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
        headers: {
            Authorization: token
        }
    });
};

// ----------------------------
// INVENTORY
// ----------------------------
export const getInventory = (playerId, token) => {
    return apiRequest(`${API}/inventory/${playerId}`, {
        headers: {
            Authorization: token
        }
    });
};

// ----------------------------
// SHOP
// ----------------------------
export const getShop = () => {
    return apiRequest(`${API}/shop`);
};

// ----------------------------
// BUY
// ----------------------------
export const buyItem = (playerId, token, itemName, quantity = 1) => {
    return apiRequest(`${API}/buy/${playerId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: token
        },
        body: JSON.stringify({
            itemName,
            quantity
        })
    });
};

// ----------------------------
// SELL
// ----------------------------
export const sellItem = (playerId, token, itemName, quantity = 1) => {
    return apiRequest(`${API}/sell/${playerId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: token
        },
        body: JSON.stringify({
            itemName,
            quantity
        })
    });
};