import { playerStatsStyles as styles } from "./styles";

function Combat({ combat, theme }) {
    const critChance = (combat.critchance ?? 0) * 100;
    const critMult = combat.critmultiplier ?? 1;

    return (
        <div style={styles.section(theme)}>

            {/* TITLE */}
            <h3
                style={{
                    marginBottom: "12px",
                    fontWeight: 900,
                    letterSpacing: "2px",
                    color: theme.text,
                    fontSize: "0.9rem",
                    opacity: 0.95,
                    textShadow: "0 0 10px rgba(255,255,255,0.05)"
                }}
            >
                COMBAT
            </h3>

            <div style={styles.statList()}>

                <Stat
                    label="Attack Power"
                    value={combat.attack ?? 0}
                    theme={theme}
                />

                <Stat
                    label="Defense Rating"
                    value={combat.defense ?? 0}
                    theme={theme}
                />

                {/* SEPARATOR (Diablo-style grouping) */}
                <div
                    style={{
                        height: "1px",
                        margin: "6px 0",
                        background:
                            "linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent)"
                    }}
                />

                <Stat
                    label="Critical Chance"
                    value={`${critChance.toFixed(1)}%`}
                    theme={theme}
                />

                <Stat
                    label="Critical Damage"
                    value={`${critMult.toFixed(2)}x`}
                    theme={theme}
                />
            </div>
        </div>
    );
}

function Stat({ label, value, theme }) {
    return (
        <div
            style={{
                ...styles.diabloRow(theme),
                transition: "all 0.2s ease",
                cursor: "default"
            }}
        >
            <div
                style={{
                    ...styles.leftLabel(theme),
                    letterSpacing: "1.2px"
                }}
            >
                {label}
            </div>

            <div
                style={{
                    ...styles.rightValue(theme),
                    fontWeight: 900,
                    textShadow: "0 0 6px rgba(255,255,255,0.05)"
                }}
            >
                {value}
            </div>
        </div>
    );
}

export default Combat;