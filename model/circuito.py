from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Circuit:
    circuitId: int
    circuitRef: str
    name: str
    location: str
    country: str
    lat: float
    lng: float
    alt: int
    url: str

    def __str__(self):
        return f"{self.name} - {self.country}"

    def __repr__(self):
        return f"{self.name} - {self.country}"
