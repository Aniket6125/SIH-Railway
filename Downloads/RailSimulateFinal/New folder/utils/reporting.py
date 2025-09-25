# utils/reporting.py
import pandas as pd
import datetime

def generate_conflict_report(conflicts):
    """
    Convert conflict list into a DataFrame for reporting.
    """
    if not conflicts:
        return pd.DataFrame(columns=["timestamp", "conflict_type", "details"])

    rows = []
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for c in conflicts:
        rows.append({
            "timestamp": now,
            "conflict_type": c.get("type", "Unknown"),
            "details": str(c)
        })
    return pd.DataFrame(rows)


def generate_kpi(before, after):
    """
    Compare KPIs (delay, conflicts) before vs after optimization.
    """
    return {
        "total_delay_before": before.get("delay", 0),
        "total_delay_after": after.get("delay", 0),
        "conflicts_resolved": before.get("conflicts", 0) - after.get("conflicts", 0)
    }


def export_excel(dfs: dict, filename: str):
    """
    Export multiple DataFrames into one Excel file (tabs).
    """
    with pd.ExcelWriter(filename) as writer:
        for sheet, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet, index=False)
    return filename
