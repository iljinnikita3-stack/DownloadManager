from models import Download, DownloadStatus
from manager import DownloadManager
import asyncio

d1 = Download(
    name="File.zip",
    size=1000,
    downloaded=0,
    status = DownloadStatus.WAITING
)
d2 = Download(
    name="pepe.pdf",
    size=500,
    downloaded=0,
    status = DownloadStatus.WAITING
)
d3 = Download(
    name="movie.mp3",
    size=700,
    downloaded=0,
    status = DownloadStatus.WAITING
)

async def main():
    manager = DownloadManager()
    ds = [d1, d2, d3]
    for d in ds:
        manager.add_download(d)
    downloads = asyncio.create_task(manager.parallel_downloads(ds))
    monitor = asyncio.create_task(manager.monitor(ds))
    await asyncio.sleep(3)
    manager.cancel_download(d2)
    await asyncio.gather(downloads, monitor)

asyncio.run(main())