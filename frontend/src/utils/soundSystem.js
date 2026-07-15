let currentAudio = null;

const sounds = {
    success: "/sounds/success.mp3",
    error: "/sounds/error.mp3",
    buy: "/sounds/buy.mp3",
    sell: "/sounds/sell.mp3",
    click: "/sounds/click.mp3",
    claim: "/sounds/claim.mp3",
    hover: "/sounds/hover.mp3"
};

const play = (type) => {
    if (!sounds[type]) return;

    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }

    const audio = new Audio(sounds[type]);
    audio.volume = 1;
    audio.play().catch(() => { });

    currentAudio = audio;
};

const soundSystem = {
    play
};

export default soundSystem;