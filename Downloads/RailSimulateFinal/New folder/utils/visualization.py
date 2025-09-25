# utils/visualization.py
import matplotlib.pyplot as plt
import pandas as pd
import io

def plot_gantt(timetable_df: pd.DataFrame):
    """
    Plot simple Gantt chart for train schedule.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    for i, row in timetable_df.iterrows():
        start = pd.to_datetime(row["scheduled_departure"])
        end = start + pd.to_timedelta(row.get("dwell_time", 1), unit="m")
        ax.plot([start, end], [i, i], linewidth=6,
                label=row["train_id"] if i == 0 else "")

    ax.set_yticks(range(len(timetable_df)))
    ax.set_yticklabels(timetable_df["train_id"])
    ax.set_xlabel("Time")
    ax.set_title("Train Timetable Gantt Chart")
    ax.legend()
    return fig


def plot_conflicts(conflicts):
    """
    Show conflicts count by type.
    """
    if not conflicts:
        return None

    df = pd.DataFrame(conflicts)
    counts = df["type"].value_counts()

    fig, ax = plt.subplots()
    counts.plot(kind="bar", ax=ax)
    ax.set_title("Conflicts by Type")
    return fig


def fig_to_bytes(fig):
    """
    Convert Matplotlib figure to PNG bytes (for Streamlit download).
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf.getvalue()
