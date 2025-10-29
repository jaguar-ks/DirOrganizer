import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ----------------- CONFIGURATION -----------------
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".svg", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".rtf"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Setup": [".exe", ".msi", ".dmg"],
    "Code": [".py", ".html", ".css", ".js", ".php", ".json"],
}
# -------------------------------------------------

class DirOrganizer:
    watch_dir = "/mnt/c/Users/ramo/Downloads"

    def __init__(self):
        self.observer = Observer()
    
    def run(self):
        organization_handler = DirOrganizerHandler()
        self.observer.schedule(
            organization_handler,
            path=self.watch_dir,
            recursive=False
        )
        self.observer.start()
        try:
            while True:
                time.slep(2)
        except:
            self.observer.stop()
        
        self.observer.join()

class DirOrganizerHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"Created: [{event.src_path}]")
        print('_'*30, event.__doc__, sep='\n')


if __name__ == '__main__':
    organizer = DirOrganizer()
    organizer.run()
