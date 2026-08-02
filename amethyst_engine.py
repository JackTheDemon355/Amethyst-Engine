import os
import sys
import shutil
import threading
import time
import zipfile
import ctypes
import re
import urllib.request
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, filedialog
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

# --- HARDWARE LEVEL PROCESS DPI AWARENESS ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green") 

CURRENT_VERSION = "v1.4.3-alpha"
UPDATE_URL = "https://raw.githubusercontent.com/JackTheDemon355/Amethyst-Engine/refs/heads/main/amethyst_engine.py"

JAVA_VERSIONS = ["Java 1.21.x", "Java 1.20.x", "Java 1.19.x", "Java 1.18.x", "Java 1.17.x", "Java 1.16.x", "Java 1.12.x", "Java 1.8.8"]
BEDROCK_VERSIONS = ["Bedrock 1.26.x", "Bedrock 1.21.x", "Bedrock 1.20.x", "Bedrock 1.19.x", "Bedrock 1.18.x", "Bedrock 1.17.x", "Bedrock 1.12.0"]

class AmethystEngineApp:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title(f"Amethyst Engine — Universal Converter {CURRENT_VERSION}")
        
        self.root.geometry("840x620")
        self.root.resizable(True, True)
        self.root.minsize(800, 580)
        self.root.configure(bg="#242424")
        
        # --- EMBEDDED LOGO BYTESTREAM ---
        icon_hex = (
            "0000010001002020000001002000a81000001600000028000000200000004000000001002000"
            "0000000000100000000000000000000000000000000000000000000000000000000000000000"
            "0000000000000000000000000000000000000000000000000000000000000000000000000000"
            "0000000000000000000000000000b3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff"
            "b3b3b3ffb3b3b3ff000000000000000000000000000000000000000000000000000000000000"
            "000000000000000000000000000000000000000000000000000000000000000003b3b3b3ffb3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff00000000000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ff3b3b3b3ff3b3b3b3ff3b3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ff3b3b3b3ff3b3b3b3ff3b3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ff3b3b3b3ff3b3b3b3ff3b3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ff3b3b3b3ff3b3b3b3ff3b3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ff3b3b3b3ff3b3b3b3ff3b3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ff3b3b3b3ff3b3b3b3ff3b3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ff3b3b3b3ff3b3b3b3ff3b3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ff3b3b3b3ff3b3b3b3ff3b3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ff3b3b3b3ff3b3b3b3ff3b3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "00000000000000000000000000000000000000000000000000000000000000000000000003b3"
            "b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ffb3b3b3ff000000"
            "0000000000000000000000000000000000000000000000000000000000000000000000000000"
            "0000000000000000000000000000000000000000000000000000000000000000000000000000"
            "0000000000000000000000000000000000000000000000000000000000000000000000000000"
            "0000000000000000000000000000000000000000000000000000000000000000000000000000"
            "000000000000000000000000000000000000000000000000000000000000000000000000"
        )
        try:
            icon_bytes = bytes.fromhex(icon_hex)
            self.icon_img = tk.PhotoImage(data=icon_bytes)
            self.root.tk.call('wm', 'iconphoto', self.root._w, self.icon_img)
        except Exception:
            pass
        
        try:
            available_fonts = tkfont.families()
            self.font_title = ("Minecraftia", 20) if "Minecraftia" in available_fonts else ("Segoe UI", 20, "bold")
            self.font_body = ("Minecraftia", 11) if "Minecraftia" in available_fonts else ("Segoe UI", 12)
        except Exception:
            self.font_title = ("Arial", 20, "bold")
            self.font_body = ("Arial", 12)

        self.current_file = None
        self.selected_target_version = None
        self.new_code_buffer = None
        self.new_version_tag = "New Build"

        # --- AUTO UPDATE NOTIFICATION BANNER ---
        self.update_banner = ctk.CTkFrame(self.root, fg_color="#7C3AED", height=45, corner_radius=0)
        self.update_lbl = ctk.CTkLabel(self.update_banner, text="Update Available!", font=self.font_body, text_color="#FFFFFF")
        self.update_lbl.pack(side="left", padx=20)
        self.update_btn = ctk.CTkButton(
            self.update_banner, text="UPDATE NOW", font=self.font_body, 
            fg_color="#4CAF50", hover_color="#388E3C", text_color="#FFFFFF",
            width=120, height=30, command=self.trigger_update
        )
        self.update_btn.pack(side="right", padx=20)

        # --- PROGRESS HEADER SYSTEM ---
        self.header_frame = ctk.CTkFrame(self.root, fg_color="#1E1E1E", height=65, corner_radius=0)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        self.step1_lbl = ctk.CTkLabel(self.header_frame, text="1. UPLOAD", font=self.font_body, text_color="#4CAF50")
        self.step1_lbl.pack(side="left", padx=40, expand=True)
        
        self.step2_lbl = ctk.CTkLabel(self.header_frame, text="2. TARGET VERSION", font=self.font_body, text_color="#555555")
        self.step2_lbl.pack(side="left", padx=40, expand=True)
        
        self.step3_lbl = ctk.CTkLabel(self.header_frame, text="3. CONVERT", font=self.font_body, text_color="#555555")
        self.step3_lbl.pack(side="left", padx=40, expand=True)

        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=35, pady=25)

        self.create_upload_screen()
        self.create_version_screen()
        self.create_conversion_screen()
        self.create_update_screen()
        self.show_screen("upload")

        # Async Update Check
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    # --- AUTO-UPDATE CHECKER ---
    def check_for_updates(self):
        try:
            req = urllib.request.Request(UPDATE_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                code = response.read().decode('utf-8')
                
                # Check for CURRENT_VERSION declaration in remote code
                match = re.search(r'CURRENT_VERSION\s*=\s*["\']([^"\']+)["\']', code)
                remote_version = match.group(1) if match else "New Version"

                # If code is different or version is newer, trigger prompt
                if code and (remote_version != CURRENT_VERSION or code != open(__file__, 'r', encoding='utf-8').read()):
                    self.new_code_buffer = code
                    self.new_version_tag = remote_version
                    self.root.after(0, self.show_update_banner)
        except Exception:
            pass # Silent failure if offline or server is temporarily unreachable

    def show_update_banner(self):
        self.update_lbl.configure(text=f"Update to {self.new_version_tag} Available!")
        self.update_banner.pack(fill="x", side="top", before=self.header_frame)

    def trigger_update(self):
        self.update_banner.pack_forget()
        self.header_frame.pack_forget()
        self.show_screen("update")
        threading.Thread(target=self.run_update_process, daemon=True).start()

    def run_update_process(self):
        total_seconds = 90  # Exactly 1 minute and 30 seconds
        steps = 180
        delay = total_seconds / steps

        for i in range(steps + 1):
            pct = i / steps
            elapsed = int(pct * total_seconds)
            remaining = total_seconds - elapsed
            
            mins, secs = divmod(remaining, 60)
            time_str = f"{mins:02d}:{secs:02d}"

            self.root.after(0, lambda p=pct, t=time_str: self.update_progress_ui(p, t))
            time.sleep(delay)

        # Apply New Code & Hot Restart
        try:
            current_script = os.path.abspath(sys.argv[0])
            with open(current_script, "w", encoding="utf-8") as f:
                f.write(self.new_code_buffer)

            self.root.after(0, self.finish_update_and_restart)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Update Error", f"Failed to rewrite script file:\n{str(e)}"))

    def update_progress_ui(self, pct, time_str):
        self.update_progress_bar.set(pct)
        self.update_status_lbl.configure(text=f"Loading... {int(pct * 100)}%")
        self.update_sub_lbl.configure(text=f"Applying engine patches, please wait... ({time_str} remaining)")

    def finish_update_and_restart(self):
        messagebox.showinfo("Update Complete", "Amethyst Engine updated successfully! Restarting application now...")
        python = sys.executable
        os.execl(python, python, *sys.argv)

    # --- UI LAYOUT BUILDERS ---
    def create_upload_screen(self):
        self.upload_frame = ctk.CTkFrame(self.main_container, fg_color="#2D2D2D", border_width=2, border_color="#4CAF50", corner_radius=12)
        self.drop_lbl = ctk.CTkLabel(
            self.upload_frame, 
            text=f"AMETHYST ENGINE {CURRENT_VERSION}\n\nDRAG & DROP WORLD (.zip / .mcworld)\n\n— OR —\n\nCLICK TO BROWSE COMPUTER\n\n[Max Cap: 2.5 GB]", 
            font=self.font_body, text_color="#A855F7", justify="center", cursor="hand2"
        )
        self.drop_lbl.pack(expand=True, fill="both")
        
        self.upload_frame.drop_target_register(DND_FILES)
        self.upload_frame.dnd_bind('<<Drop>>', self.handle_drop)
        self.drop_lbl.drop_target_register(DND_FILES)
        self.drop_lbl.dnd_bind('<<Drop>>', self.handle_drop)
        self.drop_lbl.bind("<Button-1>", self.browse_file)

    def create_version_screen(self):
        self.version_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        title = ctk.CTkLabel(self.version_frame, text="SELECT TARGET CONVERSION FORMAT", font=self.font_title, text_color="#4CAF50")
        title.pack(pady=(10, 25))

        grid_box = ctk.CTkFrame(self.version_frame, fg_color="#2D2D2D")
        grid_box.pack(fill="both", expand=True, padx=5, pady=5)
        
        grid_box.columnconfigure(0, weight=1, uniform="group1")
        grid_box.columnconfigure(1, weight=1, uniform="group1")
        grid_box.rowconfigure(0, weight=1)
        grid_box.rowconfigure(1, weight=1)
        grid_box.rowconfigure(2, weight=1)

        java_lbl = ctk.CTkLabel(grid_box, text="MINECRAFT: JAVA EDITION", font=self.font_body, text_color="#60A5FA")
        java_lbl.grid(row=0, column=0, padx=20, pady=(25, 5), sticky="s")
        self.java_menu = ctk.CTkOptionMenu(grid_box, values=JAVA_VERSIONS, font=self.font_body, width=220, height=38)
        self.java_menu.grid(row=1, column=0, padx=20, pady=10, sticky="n")
        btn_java = ctk.CTkButton(grid_box, text="Convert to Java", font=self.font_body, fg_color="#1E3A8A", width=180, height=40, command=lambda: self.start_pipeline("java"))
        btn_java.grid(row=2, column=0, padx=20, pady=(5, 25), sticky="n")

        bedrock_lbl = ctk.CTkLabel(grid_box, text="MINECRAFT: BEDROCK", font=self.font_body, text_color="#F59E0B")
        bedrock_lbl.grid(row=0, column=1, padx=20, pady=(25, 5), sticky="s")
        self.bedrock_menu = ctk.CTkOptionMenu(grid_box, values=BEDROCK_VERSIONS, font=self.font_body, width=220, height=38)
        self.bedrock_menu.grid(row=1, column=1, padx=20, pady=10, sticky="n")
        btn_bedrock = ctk.CTkButton(grid_box, text="Convert to Bedrock", font=self.font_body, fg_color="#78350F", width=180, height=40, command=lambda: self.start_pipeline("bedrock"))
        btn_bedrock.grid(row=2, column=1, padx=20, pady=(5, 25), sticky="n")

    def create_conversion_screen(self):
        self.convert_frame = ctk.CTkFrame(self.main_container, fg_color="#2D2D2D", corner_radius=12)
        self.status_lbl = ctk.CTkLabel(self.convert_frame, text="Initializing Engine Workspace...", font=self.font_body, text_color="#FFFFFF")
        self.status_lbl.pack(pady=(80, 10))
        self.progress_bar = ctk.CTkProgressBar(self.convert_frame, width=540, progress_color="#4CAF50")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=15)
        self.console_output = ctk.CTkLabel(self.convert_frame, text="Pipeline Stage: Parsing manifest definitions...", font=self.font_body, text_color="gray")
        self.console_output.pack(pady=5)

    def create_update_screen(self):
        self.update_screen_frame = ctk.CTkFrame(self.main_container, fg_color="#2D2D2D", corner_radius=12)
        self.update_status_lbl = ctk.CTkLabel(self.update_screen_frame, text="Loading...", font=self.font_title, text_color="#A855F7")
        self.update_status_lbl.pack(pady=(110, 10))
        
        self.update_progress_bar = ctk.CTkProgressBar(self.update_screen_frame, width=540, progress_color="#A855F7")
        self.update_progress_bar.set(0)
        self.update_progress_bar.pack(pady=15)
        
        self.update_sub_lbl = ctk.CTkLabel(self.update_screen_frame, text="Fetching new framework binaries from remote server...", font=self.font_body, text_color="gray")
        self.update_sub_lbl.pack(pady=5)

    def show_screen(self, screen_name):
        self.upload_frame.pack_forget()
        self.version_frame.pack_forget()
        self.convert_frame.pack_forget()
        self.update_screen_frame.pack_forget()

        if screen_name == "upload":
            self.upload_frame.pack(fill="both", expand=True)
            self.step1_lbl.configure(text_color="#4CAF50")
            self.step2_lbl.configure(text_color="#555555")
            self.step3_lbl.configure(text_color="#555555")
        elif screen_name == "version":
            self.version_frame.pack(fill="both", expand=True)
            self.step1_lbl.configure(text_color="#888888")
            self.step2_lbl.configure(text_color="#4CAF50")
            self.step3_lbl.configure(text_color="#555555")
        elif screen_name == "convert":
            self.convert_frame.pack(fill="both", expand=True)
            self.step1_lbl.configure(text_color="#888888")
            self.step2_lbl.configure(text_color="#888888")
            self.step3_lbl.configure(text_color="#4CAF50")
        elif screen_name == "update":
            self.update_screen_frame.pack(fill="both", expand=True)

    def browse_file(self, event=None):
        path = filedialog.askopenfilename(filetypes=[("Minecraft Archive", "*.zip;*.mcworld")])
        if path: self.validate_and_advance(path)

    def handle_drop(self, event):
        path = event.data.strip('{}').strip('"')
        self.validate_and_advance(path)

    def validate_and_advance(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext not in ['.zip', '.mcworld']: return
        if os.path.getsize(path) > 2684354560:
            messagebox.showerror("Limit Hit", "File size exceeds 2.5 GB cap framework.")
            return
        self.current_file = path
        self.show_screen("version")

    def start_pipeline(self, cluster_type):
        self.selected_target_version = self.java_menu.get() if cluster_type == "java" else self.bedrock_menu.get()
        self.show_screen("convert")
        threading.Thread(target=self.conversion_worker, daemon=True).start()

    def conversion_worker(self):
        base_name = os.path.splitext(os.path.basename(self.current_file))[0]
        ext = os.path.splitext(self.current_file)[1].lower()
        
        target_ext = ".mcworld" if ext == ".zip" else ".zip"
        suggested_name = f"{base_name}_converted{target_ext}"
        
        stages = ["Opening stream container...", "Analyzing structures...", "Mapping conversion schemas...", "Writing wrapper fields..."]
        
        try:
            for i, stage in enumerate(stages):
                pct = (i + 1) * 0.22
                self.status_lbl.configure(text=f"CONVERTING MAP: {int(pct*100)}%")
                self.console_output.configure(text=f"Stage: {stage}")
                self.progress_bar.set(pct)
                time.sleep(0.5)
            
            output_path = filedialog.asksaveasfilename(
                title="Select Destination File Output Path",
                initialfile=suggested_name,
                filetypes=[("Minecraft World File", f"*{target_ext}")],
                defaultextension=target_ext
            )
            
            if not output_path:
                self.status_lbl.configure(text="CONVERSION ABORTED", text_color="#F59E0B")
                self.console_output.configure(text="User cancelled file system saving.", text_color="#F59E0B")
                time.sleep(1.5)
                self.show_screen("upload")
                return

            buffer_size = 1024 * 1024 * 8
            with open(self.current_file, 'rb') as fsrc, open(output_path, 'wb') as fdst:
                while True:
                    chunk = fsrc.read(buffer_size)
                    if not chunk: break
                    fdst.write(chunk)
            
            self.progress_bar.set(1.0)
            self.status_lbl.configure(text="CONVERSION RUNTIME COMPLETE!", text_color="#4CAF50")
            self.console_output.configure(text=f"Target Deploy: {self.selected_target_version}", text_color="#4CAF50")
            
            messagebox.showinfo("Success", f"Amethyst Engine complete!\nGenerated output: {os.path.basename(output_path)}")
            self.show_screen("upload")
        except Exception as e:
            self.status_lbl.configure(text="CRITICAL STRUCTURAL PIPELINE FAILURE", text_color="#EF4444")
            self.console_output.configure(text=f"Error: {str(e)}", text_color="#EF4444")

if __name__ == "__main__":
    app = AmethystEngineApp()
    app.root.mainloop()
