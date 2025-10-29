import os
import time
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler


# ----------------- CONFIGURATION -----------------
FILE_CATEGORIES = {
    "Images": (".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".svg", ".ico"),
    "Documents": (".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".rtf"),
    "Archives": (".zip", ".rar", ".7z", ".tar", ".gz"),
    "Videos": (".mp4", ".mov", ".avi", ".mkv", ".webm"),
    "Audio": (".mp3", ".wav", ".flac", ".aac"),
    "Setup": (".exe", ".msi", ".dmg"),
    "Code": (".py", ".html", ".css", ".js", ".php", ".json"),
    "Temp": ('.tmp', '.crdownload', '.part', '.download')
}
# -------------------------------------------------

class DirOrganizer:
    watch_dir = "/mnt/c/Users/ramo/Downloads"

    def __init__(self):
        self.observer = PollingObserver()
    
    def run(self):
        organization_handler = DirOrganizerHandler()
        self.observer.schedule(
            organization_handler,
            path=self.watch_dir,
            recursive=True
        )
        self.observer.start()
        try:
            while True:
                time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
            self.observer.stop()
        
        self.observer.join()

class DirOrganizerHandler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if not event.is_directory and event.event_type == 'moved':
            src_path = os.path.basename(event.src_path).lower()
            dest_path = os.path.basename(event.dest_path).lower()
            if src_path.endswith(FILE_CATEGORIES["Temp"]):
                print(f"File Dowloaded: [{dest_path}] is downloaded successfuly")
            # print(f"EVENT ACCURED: {event.event_type} [{event.src_path.split('/')[-1]}] -> [{event.dest_path.split('/')[-1]}]")


if __name__ == '__main__':
    organizer = DirOrganizer()
    print(organizer.watch_dir)
    organizer.run()
