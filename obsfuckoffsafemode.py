import subprocess
import threading
import time
import psutil
import os
import tkinter as tk
from tkinter import scrolledtext

obs_exec = "obs64.exe"
obs_dir = r"C:\Program Files\obs-studio\bin\64bit"
safe_mode_file = os.path.expandvars(r"%APPDATA%\obs-studio\safe_mode")
obs_process_name = "obs64.exe"

class OBSWatcherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FuckOff Safemode")
        self.geometry("500x400")
        self.resizable(False, False)

        self.log_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, state='disabled', height=15)
        self.log_area.pack(expand=False, fill='both', padx=10, pady=(10, 5))

        self.force_close_button = tk.Button(self, text="Force Close OBS", command=self.force_close_obs)
        self.force_close_button.pack(side=tk.BOTTOM, pady=(0, 10))

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        if os.path.exists(safe_mode_file):
            try:
                os.remove(safe_mode_file)
                self.log(f"Deleted existing safe_mode file at start: {safe_mode_file}")
            except Exception as e:
                self.log(f"Failed to delete existing safe_mode file at start: {e}")
        else:
            self.log("No safe_mode file found at start — no action needed.")

        self.log("Launching OBS...")
        self.obs_process = self.launch_obs()
        self.watchdog_active = True  # Flag to control watchdog loop

        self.watchdog_thread = threading.Thread(target=self.watchdog, daemon=True)
        self.watchdog_thread.start()

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def launch_obs(self):
        try:
            obs_path = os.path.join(obs_dir, obs_exec)
            proc = subprocess.Popen([obs_path], cwd=obs_dir, shell=False)
            self.log(f"OBS launched from: {obs_path} (PID {proc.pid})")
            return proc
        except Exception as e:
            self.log(f"Failed to launch OBS: {e}")
            return None

    def is_obs_running(self):
        if self.obs_process is None:
            return False
        return psutil.pid_exists(self.obs_process.pid)

    def force_close_obs(self):
        found = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == obs_process_name.lower():
                    self.log(f"Attempting to terminate OBS process (PID {proc.pid})...")
                    proc.terminate()
                    found = True
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                self.log(f"Error terminating process: {e}")

        if not found:
            self.log("No running OBS process found to force close.")
            return

        gone, alive = psutil.wait_procs(
            [p for p in psutil.process_iter() if p.name().lower() == obs_process_name.lower()],
            timeout=3)
        for proc in alive:
            try:
                self.log(f"Force killing OBS process (PID {proc.pid})...")
                proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                self.log(f"Error killing process: {e}")

        self.log("OBS termination commands sent.")

    def watchdog(self):
        self.log("Watchdog started: waiting for OBS to start...")
        while self.watchdog_active and not self.is_obs_running():
            time.sleep(2)

        if not self.watchdog_active:
            self.log("Watchdog stopped before OBS started.")
            return

        self.log("OBS is running. Monitoring process...")
        while self.watchdog_active and self.is_obs_running():
            time.sleep(10)

        if not self.watchdog_active:
            self.log("Watchdog stopped while monitoring OBS.")
            return

        self.log("OBS has exited.")

        if os.path.exists(safe_mode_file):
            try:
                os.remove(safe_mode_file)
                self.log(f"Deleted safe_mode file: {safe_mode_file}")
            except Exception as e:
                self.log(f"Failed to delete safe_mode file '{safe_mode_file}': {e}")
        else:
            self.log(f"No safe_mode file found at: {safe_mode_file}")

        self.log("Watchdog finished, closing in 3 seconds...")
        self.watchdog_active = False
        self.after(3000, self.destroy)

    def on_close(self):
        # Stop watchdog thread gracefully if still running
        self.watchdog_active = False
        self.destroy()

if __name__ == "__main__":
    app = OBSWatcherApp()
    app.mainloop()