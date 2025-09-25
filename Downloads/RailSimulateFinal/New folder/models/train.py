# models/train.py
from dataclasses import dataclass

@dataclass
class Train:
    train_id: str
    type: str              # Express, Local, Freight
    origin: str
    destination: str
    departure: str         # Scheduled departure (HH:MM)
    priority: int          # 1 = High, 2 = Medium, 3 = Low
    speed: int             # Units: km/h (or block speed)
    dwell_time: int        # Minutes at stations
    platform_preferred: str = None

    def __repr__(self):
        return f"<Train {self.train_id} ({self.type}) {self.origin}->{self.destination}>"
