### Advanced Image Downloader Application

This Python application provides a GUI-based tool for downloading images from DuckDuckGo search results. Below is a comprehensive description of its features and functionality:

---

### **Key Features**
1. **Intuitive GUI Interface**
   - Dark-themed modern interface with intuitive controls
   - Responsive layout with centered elements
   - Custom styling for buttons and progress bars

2. **Image Download Capabilities**
   - Search and download images by keyword query
   - Specify number of images to download (1-100)
   - Automatic folder creation for organized storage
   - Configurable minimum image dimensions (300x300 pixels)

3. **Smart Image Handling**
   - Duplicate detection using MD5 image hashing
   - Automatic format detection (JPEG, PNG, etc.)
   - Size filtering to exclude small images
   - Sequential naming (e.g., "dogs_1.jpg")

4. **Progress Monitoring**
   - Real-time progress bar
   - Download status indicators (✅/❌/⏳)
   - Completion notifications

5. **Threaded Operations**
   - Background downloading to prevent UI freezing
   - Safe thread management with daemon threads

6. **Persistence Features**
   - Remembers window size and state (normal/zoomed)
   - Configuration saved in user's home directory
   - Cross-platform compatibility (Windows, Linux, macOS)

7. **Error Handling**
   - Internet connection checks
   - Input validation
   - Comprehensive exception handling
   - User-friendly error messages

8. **Windows-Specific Enhancements**
   - Taskbar grouping support (AppUserModelID)
   - Hidden configuration folder attributes
   - Custom application icon

---

### **Technical Components**
1. **Core Libraries**
   - `tkinter`: GUI framework
   - `PIL/Pillow`: Image processing
   - `duckduckgo_search`: Image search API
   - `requests`: HTTP handling
   - `hashlib`: Image deduplication

2. **Key Functions**
   - `download_images()`: Main download logic
   - `hash_image()`: MD5-based duplicate detection
   - `check_internet()`: Connectivity verification
   - `start_download()`/`cancel_download()`: Control flow
   - `load/save_window_geometry()`: UI state persistence

3. **UI Elements**
   - Search query entry field
   - Image count spinner (1-100)
   - Download/Cancel buttons
   - Progress bar with percentage
   - Status label with emoji indicators

---

### **Workflow**
1. User enters search query and image count
2. Application verifies internet connection
3. User selects output directory
4. Background thread:
   - Searches DuckDuckGo images
   - Filters by size and duplicates
   - Downloads valid images
   - Updates UI progress
5. Completion notification shows results
6. Window state saved on exit

---

### **System Requirements**
- Python 3.6+
- Required packages: 
  ```bash
  pillow requests duckduckgo-search configparser
  ```
- Internet connection for image downloads

---

### **Usage Notes**
- Configuration stored in `~/.ImageDownloader/config.ini`
- Downloaded images organized in query-named subfolders
- Windows: Appears as grouped taskbar item with custom icon
- Cancel button instantly stops active downloads
- Handles 3x requested images to account for filters

This application provides a robust solution for batch image downloading with careful attention to usability, performance, and error handling. The dark-themed interface and progress feedback create a pleasant user experience while the technical implementation ensures efficient and reliable operation.


<!-- AUTO UPDATE -->
Last maintenance: 2026-08-06 06:34 UTC
