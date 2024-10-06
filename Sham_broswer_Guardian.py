import os
import psutil
import tkinter as tk
from tkinter import messagebox

# Legitimate paths for the real browsers (can be extended as needed)
LEGITIMATE_PATHS = {
    'chrome.exe': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'firefox.exe': 'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
    'msedge.exe': 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
}

# Function to check if the browser is legitimate
def is_legit_browser(process_name, process_path):
    legit_path = LEGITIMATE_PATHS.get(process_name.lower(), None)
    if legit_path and os.path.abspath(process_path).lower() == os.path.abspath(legit_path).lower():
        return True
    return False

# Function to check all running processes and verify browser legitimacy
def check_browsers():
    sham_browsers = []
    legit_browsers = []

    # Iterate through all running processes
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            process_name = proc.info['name']
            process_path = proc.info['exe']
            if process_name in LEGITIMATE_PATHS:
                if is_legit_browser(process_name, process_path):
                    legit_browsers.append((process_name, process_path))
                else:
                    sham_browsers.append((process_name, process_path))
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

    return legit_browsers, sham_browsers

# Function to show the results in a message box
def show_results():
    legit_browsers, sham_browsers = check_browsers()
    
    if sham_browsers:
        message = "Warning: Sham browsers detected!\n"
        for browser, path in sham_browsers:
            message += f"Browser: {browser}, Path: {path}\n"
        messagebox.showwarning("Sham Browser Detected", message)
    else:
        message = "No sham browsers detected. All browsers are legitimate."
        messagebox.showinfo("Check Complete", message)

    if legit_browsers:
        message = "Legit browsers detected:\n"
        for browser, path in legit_browsers:
            message += f"Browser: {browser}, Path: {path}\n"
        messagebox.showinfo("Legitimate Browsers", message)

# Main tkinter GUI setup
def create_gui():
    window = tk.Tk()
    window.title("Browser Legitimacy Checker")
    window.geometry("400x200")
    
    # Label
    label = tk.Label(window, text="Click the button to check if browsers are legitimate or sham.", wraplength=350, justify="center")
    label.pack(pady=20)
    
    # Check button
    check_button = tk.Button(window, text="Check Browsers", command=show_results, width=20, height=2)
    check_button.pack(pady=20)
    
    # Run tkinter loop
    window.mainloop()

if __name__ == "__main__":
    create_gui()
