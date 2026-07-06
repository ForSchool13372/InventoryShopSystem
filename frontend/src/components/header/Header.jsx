import { useState } from "react";
import InfoModal from "./InfoModal";
import UpdateLogModal from "./UpdateLogModal";
import HeaderActions from "./HeaderActions";
import HeaderBar from "./HeaderBar";

export default function Header({
    token,
    playerId,
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
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "24px"
                }}
            >
                <HeaderBar
                    theme={theme}
                    token={token}
                    playerId={playerId}
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
