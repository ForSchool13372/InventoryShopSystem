import { useState } from "react";

import InfoModal from "./InfoModal";
import UpdateLogModal from "./UpdateLogModal";
import HeaderActions from "./HeaderActions";
import HeaderBar from "./HeaderBar";
import HeaderHUD from "./HeaderHUD";

export default function Header({
    token,
    playerId,
    playerStats,
    darkMode,
    toggleDarkMode,
    theme
}) {
    const [showInfo, setShowInfo] = useState(false);
    const [showUpdateLog, setShowUpdateLog] = useState(false);

    return (
        <>
            {/* HEADER BAR */}
            <div
                style={{
                    display: "flex",
                    flexDirection: "row",
                    alignItems: "flex-start",

                    /* FIX: remove space-between (major cause of fractional pixels) */
                    justifyContent: "flex-start",

                    /* FIX: use integer-safe spacing */
                    gap: "24px",

                    /* FIX: snap to pixel grid */
                    width: "100%",
                    boxSizing: "border-box",
                    padding: "12px",

                    /* FIX: prevent flex rounding */
                    transform: "translateZ(0)"
                }}
            >

                <HeaderBar
                    theme={theme}
                    token={token}
                    playerId={playerId}
                />

                <HeaderHUD
                    playerStats={playerStats}
                    theme={theme}
                />

                <HeaderActions
                    darkMode={darkMode}
                    toggleDarkMode={toggleDarkMode}
                    setShowInfo={setShowInfo}
                    setShowUpdateLog={setShowUpdateLog}
                />
            </div>

            {/* INFO MODAL */}
            <InfoModal
                showInfo={showInfo}
                setShowInfo={setShowInfo}
                theme={theme}
            />

            {/* UPDATE LOG MODAL */}
            <UpdateLogModal
                showUpdateLog={showUpdateLog}
                setShowUpdateLog={setShowUpdateLog}
                theme={theme}
            />
        </>
    );
}