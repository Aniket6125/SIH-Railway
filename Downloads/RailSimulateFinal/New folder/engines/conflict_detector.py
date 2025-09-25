# engines/conflict_detector.py
import pandas as pd
from datetime import datetime, timedelta

TIME_FMT = "%H:%M"

def parse_time(t):
    """Convert HH:MM string to datetime object (today)."""
    return datetime.strptime(t, TIME_FMT)

def detect_conflicts(df: pd.DataFrame) -> pd.DataFrame:
    conflicts = []

    # Ensure times are datetime
    df = df.copy()
    df["scheduled_departure"] = df["scheduled_departure"].apply(parse_time)

    # Sort by departure
    df = df.sort_values("scheduled_departure").reset_index(drop=True)

    for i, t1 in df.iterrows():
        for j, t2 in df.iterrows():
            if j <= i:
                continue

            # --- 1) Block conflict ---
            # Same origin & overlapping departure within 5 min window
            if t1["origin"] == t2["origin"]:
                diff = abs((t1["scheduled_departure"] - t2["scheduled_departure"]).total_seconds()) / 60
                if diff < 5:  # < 5 min = conflict
                    conflicts.append({
                        "type": "BlockConflict",
                        "train_a": t1["train_id"],
                        "train_b": t2["train_id"],
                        "location": f"{t1['origin']} → {t1['destination']}",
                        "time": t1["scheduled_departure"].strftime(TIME_FMT)
                    })

            # --- 2) Platform conflict ---
            if t1["platform_preferred"] == t2["platform_preferred"] and t1["origin"] == t2["origin"]:
                # dwell time overlap check
                t1_arr = t1["scheduled_departure"]
                t1_dep = t1_arr + timedelta(minutes=int(t1["dwell_time"]))
                t2_arr = t2["scheduled_departure"]
                t2_dep = t2_arr + timedelta(minutes=int(t2["dwell_time"]))

                if (t1_arr <= t2_dep) and (t2_arr <= t1_dep):  # overlap
                    conflicts.append({
                        "type": "PlatformConflict",
                        "train_a": t1["train_id"],
                        "train_b": t2["train_id"],
                        "location": t1["platform_preferred"],
                        "time": t1["scheduled_departure"].strftime(TIME_FMT)
                    })

            # --- 3) Headway violation ---
            if t1["origin"] == t2["origin"] and t1["destination"] == t2["destination"]:
                gap = abs((t1["scheduled_departure"] - t2["scheduled_departure"]).total_seconds()) / 60
                if gap < 3:  # headway < 3 min
                    conflicts.append({
                        "type": "HeadwayViolation",
                        "train_a": t1["train_id"],
                        "train_b": t2["train_id"],
                        "location": f"{t1['origin']} → {t1['destination']}",
                        "time": t1["scheduled_departure"].strftime(TIME_FMT)
                    })

    return pd.DataFrame(conflicts)
