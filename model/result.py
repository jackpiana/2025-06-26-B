from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Result:
    resultId: int
    raceId: int
    driverId: int
    constructorId: int
    number: int
    grid: int
    position: int
    positionText: str
    positionOrder: int
    points: float
    laps: int
    time: str
    milliseconds: int
    fastestLap: int
    rank: int
    fastestLapTime: str
    fastestLapSpeed: str
    statusId: int

    def __str__(self):
        return f"result {self.resultId}"
