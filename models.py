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
    def progress(self) -> str:
        if self.size == 0: return "Размер файла 0 Мб"
        return f"{self.downloaded/self.size*100}%"



