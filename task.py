from dataclasses import dataclass, asdict


@dataclass
class Task:
    id: int
    text: str
    completed: bool = False
    priority: str = 'low'  # 'low', 'medium', 'high'

    def to_dict(self):
        return asdict(self)
