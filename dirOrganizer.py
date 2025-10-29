"""dirOrganizer

Small utility that watches a Downloads folder and organizes files into
category subfolders (Images, Documents, Archives, etc.).

This module uses a polling observer from watchdog so it works on filesystems
that don't support native file events.

Usage: run the module directly. It will first classify existing files in the
watch directory and then start a background observer to move incoming files.
"""

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
    """Watcher/organizer controller.

    Attributes:
        watch_dir (str): Absolute path to the directory to watch (default
            points to the user's Downloads folder in the original project).

    The class provides a thin wrapper over a polling observer to schedule
    a `DirOrganizerHandler` and a convenience classmethod `classify_and_move`
    that computes the destination category and moves files.
    """

    watch_dir = "/Downloads"   # Change this path

    def __init__(self):
        """Create the observer and handler instances.

        The observer used is a PollingObserver (more robust across
        filesystems).
        No parameters. The handler is an instance of `DirOrganizerHandler`.
        """
        self.observer = PollingObserver()
        self.organization_handler = DirOrganizerHandler()

    def run(self):
        """Start the observer and keep the program running.

        The method schedules the handler on `self.watch_dir` recursively,
        starts the observer, and then blocks in an infinite loop until an
        exception occurs (typically a KeyboardInterrupt or other error), at
        which point it stops and joins the observer thread.
        """
        self.observer.schedule(
            self.organization_handler,
            path=self.watch_dir,
            recursive=True
        )
        self.observer.start()
        try:
            while True:
                time.sleep(2)

        except KeyboardInterrupt:
            print("✅ Script completed!...")
            self.observer.stop()
        except Exception as e:
            print(f"Error: {e}")
        self.observer.join()

    @classmethod
    def classify_and_move(cls, file_path: str):
        """Classify a single file and move it into the corresponding folder.

        Parameters:
            file_path (str): Absolute path to the file to classify. If the path
                points to a directory, this function does nothing.

        Behavior:
            - Determines the file extension (case-sensitive as implemented)
            - Looks up the destination category in `FILE_CATEGORIES`
            - Creates the destination directory if missing
            - Moves the file into the destination directory using
              `shutil.move`
            - Prints a success or error message

        Errors are caught and printed; no exception is propagated.
        """
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
    """Filesystem event handler used by the observer.

    Implements a minimal `on_any_event` handler that reacts to moved files.
    If a file was moved and its source extension is classified as a temporary
    download extension (e.g. .crdownload, .part), the handler calls
    `DirOrganizer.classify_and_move` on the destination path.
    """

    @staticmethod
    def on_any_event(event):
        """Handle filesystem events from watchdog.

        Parameters:
            event (FileSystemEvent): Event object provided by watchdog.

        Behavior:
            - If the event represents a moved file (not a directory) and the
              source file had a temporary download extension, the destination
              path will be classified and moved into its final folder.
        """
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
    print("✅ Organization complete!")
    organizer.run()
