# engines/optimizer.py
import pandas as pd
from datetime import timedelta

def optimize_timetable(df: pd.DataFrame, conflicts: pd.DataFrame):
    """
    Conflict resolution:
      - Delay lower-priority train by 5 minutes
    Returns:
      - optimized dataframe
      - list of changes made
    """
    df = df.copy()
    df["scheduled_departure"] = pd.to_datetime(df["scheduled_departure"], format="%H:%M")
    changes = []

    for _, conflict in conflicts.iterrows():
        train_a = conflict["train_a"]
        train_b = conflict["train_b"]

        prio_a = df.loc[df["train_id"] == train_a, "priority"].values[0]
        prio_b = df.loc[df["train_id"] == train_b, "priority"].values[0]

        if prio_a > prio_b:
            df.loc[df["train_id"] == train_a, "scheduled_departure"] += timedelta(minutes=5)
            changes.append({
                "Train": train_a,
                "ConflictWith": train_b,
                "Action": "Delayed by 5 min",
                "ConflictType": conflict["type"]
            })
        else:
            df.loc[df["train_id"] == train_b, "scheduled_departure"] += timedelta(minutes=5)
            changes.append({
                "Train": train_b,
                "ConflictWith": train_a,
                "Action": "Delayed by 5 min",
                "ConflictType": conflict["type"]
            })

    # Format back to HH:MM
    df["scheduled_departure"] = df["scheduled_departure"].dt.strftime("%H:%M")
    return df, changes
