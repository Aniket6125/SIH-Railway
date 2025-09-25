# models/schedule.py
import pandas as pd
from models.train import Train

class Schedule:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.trains = self._parse_trains(df)

    def _parse_trains(self, df):
        trains = []
        for _, row in df.iterrows():
            t = Train(
                train_id=row["train_id"],
                type=row["type"],
                origin=row["origin"],
                destination=row["destination"],
                departure=row["scheduled_departure"],
                priority=row["priority"],
                speed=row["speed"],
                dwell_time=row["dwell_time"],
                platform_preferred=row.get("platform_preferred", None)
            )
            trains.append(t)
        return trains

    def get_trains(self):
        return self.trains
