from enum import Enum, auto
from dataclasses import dataclass

class DownloadStatus(Enum):
    WAITING = auto()
    DOWNLOADING = auto()
    COMPLETED = auto()
    CANCELLED = auto()

@dataclass
class Download:
    name: str
    size: int
    downloaded: int
    status: DownloadStatus
    def progress(self) -> int:
        if self.size == 0: return 0
        return self.downloaded/self.size*100



