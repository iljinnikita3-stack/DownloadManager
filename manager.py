from models import Download, DownloadStatus
from typing import Optional
import asyncio
from random import randint

class DownloadManager:
    def __init__(self) -> None:
        self.downloads: list[Download] = []
        
    def add_download(self, download: Download) -> None:
        self.downloads.append(download)

    def show_downloads(self) -> str:
        if not self.downloads: 
            print("Нет загрузок")
            return
        for download in self.downloads:
            print(download.name)
            print(f"Размер: {download.size} Мб")
            print(f"Статус: {download.status}")
            print(f"Прогресс: {download.progress():.1f}%")
            
            
    def find_download(self, name: str) -> Optional[Download]:
        for download in self.downloads:
            if download.name == name:
                return download
            return None
        
        
    async def download_file(self, download: Download) -> str:
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
    
    async def parallel_downloads(self, active_downloads: list[Download]):
        tasks = [self.download_file(file) for file in active_downloads]
        await asyncio.gather(*tasks)
        
        
    

      
    
    
