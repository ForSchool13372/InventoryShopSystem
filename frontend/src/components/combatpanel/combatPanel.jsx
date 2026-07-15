import { motion } from "framer-motion";
import { useEffect, useMemo, useRef, useState } from "react";

import { getCombatPanelStyles } from "./combatPanelStyles";

import CombatEnemy from "./CombatEnemy";
import CombatLog from "./CombatLog";
import CombatLoot from "./CombatLoot";
import CombatPlayer from "./CombatPlayer";


export default function CombatPanel({
    theme,
    fightData,
    fightLoading,
    handleFight,
    clearFight,
    playerStats
}) {
    const enemy = fightData?.enemy;

    const [displayLog, setDisplayLog] = useState([]);
    const [isReplaying, setIsReplaying] = useState(false);
    const [hitEffect, setHitEffect] = useState(false);
    const [displayEnemyHp, setDisplayEnemyHp] = useState(0);
    const [displayPlayerHp, setDisplayPlayerHp] = useState(0);

    const lastFightIdRef = useRef(null);

    const log = useMemo(
        () => fightData?.log ?? [],
        [fightData?.log]
    );

    const styles = getCombatPanelStyles(theme);

    const enemyHpPercent = enemy
        ? Math.max((displayEnemyHp / enemy.maxHp) * 100, 0)
        : 0;


    const handleReset = () => {
        clearFight();
        setDisplayLog([]);
        setDisplayEnemyHp(0);
        setDisplayPlayerHp(0);
        setIsReplaying(false);
        lastFightIdRef.current = null;
    };


    useEffect(() => {
        if (!fightData) return;

        const fightId =
            fightData.enemy?.name +
            "-" +
            (fightData.log?.length ?? 0);

        if (lastFightIdRef.current === fightId) return;

        lastFightIdRef.current = fightId;

        setDisplayEnemyHp(fightData.enemy.startingHp);
        setDisplayPlayerHp(fightData.startingPlayerHp);
        setDisplayLog([]);
        setIsReplaying(true);

        let i = 0;

        const interval = setInterval(() => {
            const current = log[i];

            if (!current) return;


            // Add log line
            setDisplayLog(prev => [
                ...prev,
                current
            ]);


            // Player damages enemy
            if (current.includes("You deal")) {
                const damage = parseInt(
                    current.match(/deal (\d+)/)?.[1] ?? 0
                );

                setDisplayEnemyHp(prev =>
                    Math.max(prev - damage, 0)
                );

                setHitEffect(true);
            }


            // Enemy damages player
            if (current.includes("hits you")) {
                const damage = parseInt(
                    current.match(/for (\d+) damage/)?.[1] ?? 0
                );

                setDisplayPlayerHp(prev =>
                    Math.max(prev - damage, 0)
                );

                setHitEffect(true);
            }


            // Critical hit = stronger impact
            if (current.includes("CRITICAL")) {
                setHitEffect(true);
            }


            // Remove shake after impact
            if (
                current.includes("deal") ||
                current.includes("hits you") ||
                current.includes("CRITICAL")
            ) {
                setTimeout(() => {
                    setHitEffect(false);
                }, 250);
            }


            i++;


            if (i >= log.length) {
                clearInterval(interval);

                setTimeout(() => {
                    setIsReplaying(false);
                }, 300);
            }

        }, 700);


        return () => clearInterval(interval);

    }, [fightData, log]);

    const locked = fightLoading || isReplaying;


    const getLogStyle = (line) => {
        if (line.includes("CRITICAL")) {
            return {
                color: "#fbbf24",
                fontWeight: 900
            };
        }

        if (line.includes("You deal")) {
            return {
                color: "#60a5fa",
                fontWeight: 700
            };
        }

        if (line.includes("hits")) {
            return {
                color: "#f87171"
            };
        }

        if (line.includes("defeated")) {
            return {
                color: "#22c55e",
                fontWeight: 900
            };
        }

        return {};
    };


    return (
        <motion.div
            style={styles.card}
            animate={
                hitEffect
                    ? {
                        x: [-4, 4, -4, 0]
                    }
                    : {}
            }
            transition={{
                duration: 0.2
            }}
        >

            <div style={styles.title}>
                ⚔️ BATTLE
            </div>


            <CombatEnemy
                enemy={enemy}
                displayEnemyHp={displayEnemyHp}
                enemyHpPercent={enemyHpPercent}
            />

            <CombatPlayer
                displayPlayerHp={displayPlayerHp}
                maxPlayerHp={fightData?.startingPlayerHp}
                playerStats={playerStats}
            />


            <div style={styles.actions}>

                <button
                    style={{
                        ...styles.button,
                        opacity: locked ? 0.6 : 1,
                        cursor: locked
                            ? "not-allowed"
                            : "pointer"
                    }}
                    onClick={() => {
                        setDisplayLog([]);
                        setIsReplaying(true);
                        handleFight();
                    }}
                    disabled={locked}
                >
                    {
                        fightLoading
                            ? "Fighting..."
                            : isReplaying
                                ? "Battle in progress..."
                                : "⚔️ Attack"
                    }
                </button>


                <button
                    style={{
                        ...styles.button,
                        background: "#ef4444"
                    }}
                    onClick={handleReset}
                    disabled={locked}
                >
                    Reset
                </button>

            </div>


            <CombatLog
                displayLog={displayLog}
                getLogStyle={getLogStyle}
                styles={styles}
            />


            <CombatLoot
                isReplaying={isReplaying}
                items={fightData?.items}
            />

        </motion.div>
    );
}