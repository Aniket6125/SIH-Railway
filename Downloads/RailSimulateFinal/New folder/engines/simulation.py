# engines/simulation.py
import time

class Simulation:
    def __init__(self, schedule, network):
        self.schedule = schedule
        self.network = network
        self.events = []

    def run(self):
        # Placeholder: just record train movements
        for train in self.schedule.get_trains():
            self.events.append({
                "event": "depart",
                "train": train.train_id,
                "from": train.origin,
                "time": train.departure
            })
        return self.events

    def step(self):
        if self.events:
            return self.events.pop(0)
        return None
