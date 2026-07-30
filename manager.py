from models import Download, DownloadStatus
from typing import Optional
import asyncio
from random import randint

class DownloadManager:
    def __init__(self) -> None:
        self.downloads: list[Download] = []
        self.tasks: dict[str, asyncio.Task[None]] = {}

    def add_download(self, download: Download) -> None:
        self.downloads.append(download)

    def show_downloads(self) -> None:
        if not self.downloads: 
            print("Нет загрузок")
            return
        for download in self.downloads:
            print(download.name)
            print(f"Размер: {download.size} Мб")
            print(f"Статус: {download.status.name}")
            print(f"Прогресс: {download.progress():.1f}%")
            
            
    def find_download(self, name: str) -> Optional[Download]:
        for download in self.downloads:
            if download.name == name:
                return download
        return None
        
        
    async def download_file(self, download: Download) -> None:
        try:
            print(f"Начинается загрузка {download.name}")
            download.status = DownloadStatus.DOWNLOADING
            while download.size != download.downloaded:
                await asyncio.sleep(1)
                download.downloaded += randint(0, download.size // 3)
                if download.downloaded > download.size:
                    download.downloaded = download.size
                print(f"{download.progress():.1f}%")
            download.status = DownloadStatus.COMPLETED
            print(f"Загрузка {download.name} завершена")
        except asyncio.CancelledError:
            print(f"Загрузка отменена, загружено {download.progress()} Мб из {download.size} Мб")
            download.status = DownloadStatus.CANCELLED
        
    async def parallel_downloads(self, active_downloads: list[Download]) -> None:
        keys = [download.name for download in active_downloads]
        values = [asyncio.create_task(self.download_file(file)) for file in active_downloads]
        self.tasks = dict(zip(keys, values))
        await asyncio.gather(*values)
        
    def cancel_download(self, download: Download) -> None:
        self.tasks[download.name].cancel()
        

      
    
    
