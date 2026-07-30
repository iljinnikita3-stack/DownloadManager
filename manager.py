from models import Download, DownloadStatus
from typing import Optional
import asyncio
from random import randint
from datetime import datetime

#ЦВЕТА
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[36m"
RESET = "\033[0m"
GREEN = "\033[32m"

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
            now = datetime.now()
            print(f"{GREEN}[{now.hour:02d}:{now.minute:02d}:{now.second:02d}]{RESET} {YELLOW}Начинается загрузка {download.name}{RESET}")
            
            download.status = DownloadStatus.DOWNLOADING
            while download.size != download.downloaded:
                await asyncio.sleep(1)
                download.downloaded += randint(0, download.size // 3)
                if download.downloaded > download.size:
                    download.downloaded = download.size
                print(f"{BLUE}{download.name} прогресс {download.progress():.1f}%{RESET}")
                
            download.status = DownloadStatus.COMPLETED
            now = datetime.now()
            print(f"{GREEN}[{now.hour:02d}:{now.minute:02d}:{now.second:02d}]{RESET} {YELLOW}Загрузка {download.name} завершена{RESET}")
            
        except asyncio.CancelledError:
            print(f"{RED}Загрузка отменена, загружено {download.downloaded} Мб из {download.size} Мб{RESET}")
            download.status = DownloadStatus.CANCELLED

      
    async def parallel_downloads(self, active_downloads: list[Download]) -> None:
        keys = [download.name for download in active_downloads]
        values = [asyncio.create_task(self.download_file(file)) for file in active_downloads]
        self.tasks = dict(zip(keys, values))
        await asyncio.gather(*values)
        
    def cancel_download(self, download: Download) -> None:
        self.tasks[download.name].cancel()
        
    async def monitor(self, active_downloads: list[Download]) -> None:
        while sum([download.status in [DownloadStatus.CANCELLED, DownloadStatus.COMPLETED] for download in active_downloads]) != len(active_downloads):
            print("="*40)
            for download in active_downloads:
                print(download.name.ljust(20), f"{download.progress():.1f}%".rjust(8), download.status.name)
            print("="*40)
            await asyncio.sleep(1)
    
