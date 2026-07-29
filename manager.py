from models import Download
from typing import Optional

class DownloadManager:
    def __init__(self):
        self.downloads: list = []
        def add_download(self, download: Download):
            self.downloads.append(download)
        def show_downloads(self):
            if len(self.downloads) == 0: 
                print("Нет загрузок")
                return
            for download in self.downloads:
                print(download.name)
                print(f"Размер: {download.size} Мб")
                print(f"Статус: {download.status}")
                print(f"Прогресс: {download.progress():.1f}%")
        def find_download(self, name) -> Optional[Download]:
            for download in self.downloads:
                if download.name == name:
                    return download
                return None
        
      
    
    
