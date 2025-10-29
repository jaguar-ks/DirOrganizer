import os
import time
import shutil
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler


# ----------------- CONFIGURATION -----------------
FILE_CATEGORIES = {
    "Images": (".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".svg",
               ".ico"),
    "Documents": (".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt",
                  ".pptx", ".odt", ".rtf"),
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
        self.organization_handler = DirOrganizerHandler()

    def run(self):
        self.observer.schedule(
            self.organization_handler,
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

    @classmethod
    def classify_and_move(cls, file_path: str):
        if not os.path.isdir(file_path):
            file_name = os.path.basename(file_path)
            _, extansion = os.path.splitext(file_name)
            destination_dir = 'Others'
            for directory, extansions in FILE_CATEGORIES.items():
                if extansion in extansions:
                    destination_dir = directory
                    break
            destination_dir = os.path.join(cls.watch_dir, destination_dir)
            file_final_dest = os.path.join(destination_dir, file_name)
            try:
                os.makedirs(destination_dir, exist_ok=True)
                shutil.move(file_path, file_final_dest)
                print(f"MOVED: [{file_path}] => [{file_final_dest}]")
            except Exception as e:
                print(f"ERROR [Failed to move file]: {e}")


class DirOrganizerHandler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if not event.is_directory and event.event_type == 'moved':
            src_path = os.path.basename(event.src_path).lower()
            _, src_extansion = os.path.splitext(src_path)
            if src_extansion in FILE_CATEGORIES["Temp"]:
                DirOrganizer.classify_and_move(event.dest_path)

if __name__ == '__main__':
    organizer = DirOrganizer()
    for file in os.listdir(organizer.watch_dir):
        file_path = os.path.join(organizer.watch_dir, file)
        DirOrganizer.classify_and_move(file_path)
    print("\n✅ Organization complete!")
    organizer.run()
