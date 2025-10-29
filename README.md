# DirOrganizer

A lightweight Python utility that automatically organizes files in your Downloads folder (or any directory) by categorizing them into subfolders based on file type.

## Overview & Key Features

DirOrganizer watches a specified directory and automatically moves incoming files into category-specific subfolders. It uses a polling observer from the `watchdog` library, making it compatible with all filesystems including those that don't support native file system events.

- ✅ **Automatic File Organization** - Categorizes files based on their extensions
- ✅ **Real-time Monitoring** - Watches for incoming files and organizes them on-the-fly
- ✅ **Batch Processing** - Organizes existing files on startup
- ✅ **Cross-platform Compatible** - Works on Windows, macOS, and Linux
- ✅ **Robust Polling** - Uses PollingObserver for maximum filesystem compatibility
- ✅ **Customizable Categories** - Easy to modify file categories and extensions

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [File Categories](#file-categories) | Supported file types and organization |
| [Installation](#installation) | Setup and requirements |
| [Usage](#usage) | How to run the organizer |
| [Project Structure](#project-structure) | Directory layout |
| [Configuration](#configuration) | Customization options |
| [How It Works](#how-it-works) | Technical overview |
| [Troubleshooting](#troubleshooting) | Common issues and solutions |
| [Future Enhancements](#possible-improvements-for-future-versions) | Planned improvements |

## File Categories

Files are automatically organized into the following categories based on their extensions:

| Category | Extensions |
|----------|-----------|
| **Images** | .jpg, .jpeg, .png, .gif, .webp, .tiff, .svg, .ico |
| **Documents** | .pdf, .doc, .docx, .txt, .xls, .xlsx, .ppt, .pptx, .odt, .rtf |
| **Archives** | .zip, .rar, .7z, .tar, .gz |
| **Videos** | .mp4, .mov, .avi, .mkv, .webm |
| **Audio** | .mp3, .wav, .flac, .aac |
| **Setup** | .exe, .msi, .dmg |
| **Code** | .py, .html, .css, .js, .php, .json |
| **Temp** | .tmp, .crdownload, .part, .download |
| **Others** | Any unrecognized extension |

> **Note:** The default watch directory is set to `/Downloads`. Modify the `watch_dir` class variable in `DirOrganizer` to change this.

---

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the repository:**

   ```bash
   git clone git@github.com:jaguar-ks/DirOrganizer.git
   cd DirOrganizer
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Organizer

Head to the [`dirOrganizer.py`](dirOrganizer.py) file and change the `watch_dir` variable in the **`DirOrganizer`** class with your targeted directory.

Start the organizer with:

```bash
python dirOrganizer.py
```

**What happens:**

1. The script first scans the watch directory for existing files
2. Organizes all existing files into their appropriate category folders
3. Displays: `✅ Organization complete!`
4. Starts monitoring the directory in the background
5. Automatically moves new files as they arrive
6. Continues running until interrupted (Ctrl+C)

### Example Output

```text
MOVED: [/Downloads/document.pdf] => [/Downloads/Documents/document.pdf]
MOVED: [/Downloads/image.png] => [/Downloads/Images/image.png]
MOVED: [/Downloads/archive.zip] => [/Downloads/Archives/archive.zip]
✅ Organization complete!
```

### Directory Structure: Before and After

#### Before Running the Script

```text
Downloads/
├── document.pdf
├── image.png
├── archive.zip
├── video.mp4
├── song.mp3
├── presentation.pptx
├── installer.exe
├── script.py
├── report.txt
└── game.rar
```

#### After Running the Script

```text
Downloads/
├── Documents/
│   ├── document.pdf
│   ├── presentation.pptx
│   └── report.txt
├── Images/
│   └── image.png
├── Archives/
│   ├── archive.zip
│   └── game.rar
├── Videos/
│   └── video.mp4
├── Audio/
│   └── song.mp3
├── Setup/
│   └── installer.exe
└── Code/
    └── script.py
```

All files are automatically categorized and moved into their respective folders, keeping your Downloads directory clean and organized! ✨

## Project Structure

```text
DirOrganizer/
├── dirOrganizer.py       # Main application file
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Configuration

### Modifying the Watch Directory

Edit the `watch_dir` class variable in `dirOrganizer.py`:

```python
class DirOrganizer:
    watch_dir = "/path/to/your/directory"  # Change this path
```

### Adding/Modifying File Categories

Edit the `FILE_CATEGORIES` dictionary at the top of `dirOrganizer.py`:

```python
FILE_CATEGORIES = {
    "Images": (".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".svg", ".ico"),
    "Documents": (".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".rtf"),
    # Add more categories as needed
}
```

## How It Works

1. **Initialization**: Creates a `PollingObserver` instance to monitor the filesystem
2. **Initial Scan**: Iterates through all files in the watch directory and organizes them
3. **Event Monitoring**: Watches for file move events (typically `.crdownload` → final filename)
4. **Classification**: Determines file category based on extension
5. **Organization**: Creates category folders (if needed) and moves files

### Event Flow

```text
Incoming File (e.g., document.pdf.crdownload)
    ↓
File Download Completes
    ↓
watchdog Detects 'moved' Event
    ↓
DirOrganizerHandler.on_any_event() Triggered
    ↓
Checks if Source Extension is in "Temp" Category
    ↓
Calls DirOrganizer.classify_and_move()
    ↓
File Extension Matched to Category
    ↓
Destination Folder Created (if missing)
    ↓
File Moved to Category Folder
```

## Stopping the Application

Press `Ctrl+C` in your terminal to gracefully stop the organizer:

```bash
Keyboard interrupt detected. Shutting down...
✅ Script completed!...
```

## Troubleshooting

### Issue: "Watch directory does not exist"

**Solution:**
> Verify the `watch_dir` path is correct and the directory exists.

### Issue: "Permission denied" errors

**Solution:**
> Ensure you have read/write permissions for the watch directory and all its subdirectories.

### Issue: Files not being organized

**Solution:**

> - Verify the file extensions are defined in `FILE_CATEGORIES`
> - Check that temporary file extensions (.crdownload, .part, etc.) are present for new downloads
> - Ensure the observer is running (check console output)

### Issue: Application crashes on startup

**Solution:**

> - Verify all dependencies are installed: `pip install -r requirements.txt`
> - Ensure the watch directory path is valid
> - Check that no files in the directory are locked by other applications## Future Enhancements

## Possible improvements for future versions

- [ ] Configuration file support (JSON/YAML)
- [ ] Scheduled cleanup of old files
- [ ] Duplicate file handling strategies
- [ ] File renaming rules based on date or content
- [ ] GUI interface for easier configuration
- [ ] Exclude patterns for specific files
- [ ] Multiple directory watching
- [ ] Statistics and reporting dashboard

## Author

Created by [jaguar-ks](https://github.com/jaguar-ks)

## Support

For issues or feature requests, please refer to the project repository or contact the author.

**Last Updated:** October 29, 2025
