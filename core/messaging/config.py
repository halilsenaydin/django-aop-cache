from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class ExchangeConfig:
    name: str
    type: Literal["fanout", "direct", "topic", "headers"] = "fanout"
    durable: bool = True
    auto_delete: bool = False
    routing_key: Optional[str] = None
    auto_ack: bool = False
    prefetch_count: int = 1

    def __post_init__(self):
        if self.type in {"direct", "topic"} and not self.routing_key:
            raise ValueError(f"routing_key is required for exchange type '{self.type}'")
