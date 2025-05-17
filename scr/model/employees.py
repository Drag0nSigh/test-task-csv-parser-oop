from dataclasses import dataclass


@dataclass
class Employee:
    id: int
    name: str
    department: str
    email: str
    hours_worked: int
    hourly_rate: int
    payout: int
