import configparser
import ctypes
import os
import sys
import threading
import hashlib
import requests
from io import BytesIO
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image
from duckduckgo_search import DDGS

if sys.platform == "win32":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Com.example.ImageDownloader")

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")
    full_path = os.path.join(base_path, relative_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Resource not found: {full_path}")
    return full_path
stop_download = False

def hash_image(img):
    hash_md5 = hashlib.md5()
    hash_md5.update(img.tobytes())
    return hash_md5.hexdigest()

def download_images(query, num_images, save_path, min_width, min_height, status_label, progress_bar):
    global stop_download
    stop_download = False
    seen_hashes = set()
    downloaded = 0

    try:

        with DDGS() as ddgs:
            results = ddgs.images(query, max_results=num_images * 3)
            for i, result in enumerate(results):

                if stop_download:
                    status_label.config(text="❌ Download canceled.")
                    return

                if downloaded >= num_images:
                    break
                url = result["image"]

                try:
                    response = requests.get(url, timeout=10)
                    img = Image.open(BytesIO(response.content))

                    if img.width < min_width or img.height < min_height:
                        continue
                    img_hash = hash_image(img)

                    if img_hash in seen_hashes:
                        continue
                    seen_hashes.add(img_hash)
                    img_format = img.format if img.format else "JPEG"
                    subfolder = os.path.join(save_path, query)
                    os.makedirs(subfolder, exist_ok=True)
                    filename = os.path.join(subfolder, f"{query}_{downloaded+1}.{img_format.lower()}")
                    img.save(filename)
                    downloaded += 1
                    progress = int((downloaded / num_images) * 100)
                    status_label.config(text=f"✅ Downloaded {downloaded}/{num_images} images")
                    progress_bar['value'] = progress

                except Exception as e:
                    print(f"Failed to download image {i+1}: {e}")

        if downloaded > 0:
            messagebox.showinfo("Download Complete", f"{downloaded} image(s) downloaded successfully.")
        else:
            messagebox.showwarning("No Images", "No suitable images were found.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        progress_bar['value'] = 0
        status_label.config(text="")
        cancel_btn.pack_forget()
        progress_bar.pack_forget()
        download_btn.pack(pady=15)

def check_internet():

    try:
        requests.get("https://www.google.com", timeout=5)
        return True

    except requests.RequestException:
        return False

def start_download():
    global stop_download
    stop_download = False

    if not check_internet():
        messagebox.showerror("No Internet", "No internet connection detected.")
        return
    query = entry.get().strip()

    try:
        num_images = int(spinbox.get())

    except:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return

    if not query:
        messagebox.showwarning("Warning", "Please enter an object name.")
        return
    folder_path = filedialog.askdirectory(title="Select folder to save images")

    if not folder_path:
        return
    status_label.config(text="⏳ Downloading...")
    download_btn.pack_forget()
    cancel_btn.pack(pady=10)
    progress_bar.pack(pady=10)
    threading.Thread(
        target=download_images,
        args=(query, num_images, folder_path, 300, 300, status_label, progress_bar),
        daemon=True
    ).start()

def cancel_download():
    global stop_download
    stop_download = True
    status_label.config(text="❌ Canceling...")
    cancel_btn.pack_forget()
    download_btn.pack(pady=15)
    progress_bar.pack_forget()

def load_window_geometry():

    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        if "Geometry" in config:
            geometry = config["Geometry"].get("size", "")
            state = config["Geometry"].get("state", "normal")

            if geometry:
                root.geometry(geometry)
                root.update_idletasks()
                root.update()

            if state == "zoomed":
                root.state("zoomed")
            elif state == "iconic":
                root.iconify()

def save_window_geometry():
    config = configparser.ConfigParser()
    config["Geometry"] = {
        "size": root.geometry(),
        "state": root.state()
    }

    with open(config_file, "w") as f:
        config.write(f)

def on_close():
    save_window_geometry()
    root.destroy()
    os._exit(0)
root = Tk()
root.title("⚡ Advanced Image Downloader - By Sourav Bhattacharya")
root.geometry("500x400")
root.resizable(False, False)

try:
    root.iconbitmap(resource_path(r"icons/icon.ico"))

except Exception as e:
    print("Icon load error:", e)
data_dir = os.path.join(os.path.expanduser("~"), ".ImageDownloader")
os.makedirs(data_dir, exist_ok=True)

if sys.platform == "win32":

    try:
        ctypes.windll.kernel32.SetFileAttributesW(data_dir, 2)

    except:
        pass
config_file = os.path.join(data_dir, "config.ini")
bg = Canvas(root, width=500, height=400)
bg.pack(fill="both", expand=True)
bg.create_rectangle(0, 0, 500, 400, fill="#1e1e2f", outline="")
frame = Frame(root, bg="#2c2f4a")
frame.place(relx=0.5, rely=0.5, anchor="center")
style = ttk.Style()
style.configure("TButton", font=("Arial", 11), padding=6)
style.configure("TProgressbar", thickness=15, troughcolor="#3a3f5c", background="#00d4ff", bordercolor="#000")
label1 = Label(frame, text="Enter Object Name:", font=("Arial", 12), bg="#2c2f4a", fg="white")
label1.pack(pady=5)
entry = Entry(frame, font=("Arial", 12), width=30, insertbackground="white"  ,bg="#616163",fg="white", relief=FLAT, bd=5, highlightbackground="#616163", highlightcolor="#1414FF", highlightthickness=3)
entry.pack(ipady=3, padx=10)
label2 = Label(frame, text="Number of Images:", font=("Arial", 12), bg="#2c2f4a", fg="white")
label2.pack(pady=10)
spinbox = Spinbox(frame, from_=1, to=100, font=("Arial", 12), width=5, bg="#e0e0e0", relief=FLAT, bd=3)
spinbox.pack()
download_btn = Button(frame, text="⬇ Download Images", font=("Arial", 12, "bold"), bg="#00d4ff", fg="black", relief=FLAT, command=start_download, cursor="hand2")
download_btn.pack(pady=15)
cancel_btn = Button(frame, text="❌ Cancel", font=("Arial", 12, "bold"), bg="#ff4d4d", fg="white", relief=FLAT, command=cancel_download, cursor="hand2")
progress_bar = ttk.Progressbar(frame, orient=HORIZONTAL, length=300, mode='determinate')
status_label = Label(frame, text="", font=("Arial", 10, "italic"), fg="#00ff99", bg="#2c2f4a")
status_label.pack(pady=10)
load_window_geometry()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
