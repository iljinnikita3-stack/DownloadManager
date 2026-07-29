from enum import Enum, auto

class DownloadStatus(Enum):
    WAITING = auto()
    DOWNLOADING = auto()
    COMPLETED = auto()
    CANCELLED = auto()

print(DownloadStatus.WAITING)
    
    
