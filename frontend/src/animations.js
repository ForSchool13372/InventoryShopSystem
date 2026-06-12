export const page = {
    hidden: { opacity: 0, y: 12 },
    show: { opacity: 1, y: 0, transition: { duration: 0.35 } }
};

export const fadeUp = (delay = 0) => ({
    hidden: { opacity: 0, y: 10 },
    show: { opacity: 1, y: 0, transition: { delay, duration: 0.3 } }
});