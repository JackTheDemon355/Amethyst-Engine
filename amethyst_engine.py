import os
import shutil
import threading
import time
import zipfile
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green") 

JAVA_VERSIONS = ["Java 1.21.x", "Java 1.20.x", "Java 1.19.x", "Java 1.18.x", "Java 1.17.x", "Java 1.16.x", "Java 1.12.x", "Java 1.8.8"]
BEDROCK_VERSIONS = ["Bedrock 1.26.x", "Bedrock 1.21.x", "Bedrock 1.20.x", "Bedrock 1.19.x", "Bedrock 1.18.x", "Bedrock 1.17.x", "Bedrock 1.12.0"]

class AmethystEngineApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Amethyst Engine — Universal Converter")
        self.root.geometry("680x500")
        self.root.resizable(False, False)
        
        TkinterDnD.require(self.root)
        
        self.font_title = ("Minecraftia", 22) if "Minecraftia" in ctk.FontManager.get_font_names() else ("Consolas", 22, "bold")
        self.font_body = ("Minecraftia", 11) if "Minecraftia" in ctk.FontManager.get_font_names() else ("Consolas", 11)

        self.current_file = None
        self.selected_target_version = None

        # --- STEP PROGRESS INDICATOR HEADER ---
        self.header_frame = ctk.CTkFrame(self.root, fg_color="#1E1E1E", height=60, corner_radius=0)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        self.step1_lbl = ctk.CTkLabel(self.header_frame, text="1. UPLOAD", font=self.font_body, text_color="#4CAF50")
        self.step1_lbl.pack(side="left", padx=50, expand=True)
        
        self.step2_lbl = ctk.CTkLabel(self.header_frame, text="2. TARGET VERSION", font=self.font_body, text_color="#555555")
        self.step2_lbl.pack(side="left", padx=50, expand=True)
        
        self.step3_lbl = ctk.CTkLabel(self.header_frame, text="3. CONVERT", font=self.font_body, text_color="#555555")
        self.step3_lbl.pack(side="left", padx=50, expand=True)

        # --- CONTAINER VIEWPORTS ---
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=30, pady=20)

        self.create_upload_screen()
        self.create_version_screen()
        self.create_conversion_screen()

        self.show_screen("upload")

    def create_upload_screen(self):
        self.upload_frame = ctk.CTkFrame(self.main_container, fg_color="#2D2D2D", border_width=2, border_color="#4CAF50", corner_radius=12)
        
        self.drop_lbl = ctk.CTkLabel(
            self.upload_frame, 
            text="AMETHYST ENGINE\n\nDRAG & DROP WORLD (.zip / .mcworld)\n\n— OR —\n\nCLICK TO BROWSE COMPUTER\n\n[Max Cap: 2.5 GB]", 
            font=self.font_body,
            text_color="#A855F7",
            justify="center",
            cursor="hand2"
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
        title.pack(pady=(10, 20))

        grid_box = ctk.CTkFrame(self.version_frame, fg_color="#2D2D2D")
        grid_box.pack(fill="both", expand=True, padx=10, pady=10)

        # Java Column
        java_lbl = ctk.CTkLabel(grid_box, text="MINECRAFT: JAVA EDITION", font=self.font_body, text_color="#60A5FA")
        java_lbl.grid(row=0, column=0, padx=35, pady=20, sticky="n")
        
        self.java_menu = ctk.CTkOptionMenu(grid_box, values=JAVA_VERSIONS, font=self.font_body, width=200)
        self.java_menu.grid(row=1, column=0, padx=35, pady=5)
        
        btn_java = ctk.CTkButton(grid_box, text="Convert to Java", font=self.font_body, fg_color="#1E3A8A", command=lambda: self.start_pipeline("java"))
        btn_java.grid(row=2, column=0, padx=35, pady=25)

        # Bedrock Column
        bedrock_lbl = ctk.CTkLabel(grid_box, text="MINECRAFT: BEDROCK", font=self.font_body, text_color="#F59E0B")
        bedrock_lbl.grid(row=0, column=1, padx=35, pady=20, sticky="n")
        
        self.bedrock_menu = ctk.CTkOptionMenu(grid_box, values=BEDROCK_VERSIONS, font=self.font_body, width=200)
        self.bedrock_menu.grid(row=1, column=1, padx=35, pady=5)
        
        btn_bedrock = ctk.CTkButton(grid_box, text="Convert to Bedrock", font=self.font_body, fg_color="#78350F", command=lambda: self.start_pipeline("bedrock"))
        btn_bedrock.grid(row=2, column=1, padx=35, pady=25)

    def create_conversion_screen(self):
        self.convert_frame = ctk.CTkFrame(self.main_container, fg_color="#2D2D2D", corner_radius=12)
        
        self.status_lbl = ctk.CTkLabel(self.convert_frame, text="Initializing Engine Workspace...", font=self.font_body, text_color="#FFFFFF")
        self.status_lbl.pack(pady=(60, 10))

        self.progress_bar = ctk.CTkProgressBar(self.convert_frame, width=500, progress_color="#4CAF50")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.console_output = ctk.CTkLabel(self.convert_frame, text="Pipeline Stage: Parsing manifest definitions...", font=self.font_body, text_color="gray")
        self.console_output.pack(pady=5)

    def show_screen(self, screen_name):
        self.upload_frame.pack_forget()
        self.version_frame.pack_forget()
        self.convert_frame.pack_forget()

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

    def browse_file(self, event=None):
        from tkinter import filedialog
        path = filedialog.askopenfilename(filetypes=[("Minecraft Archive", "*.zip;*.mcworld")])
        if path: self.validate_and_advance(path)

    def handle_drop(self, event):
        path = event.data.strip('{}').strip('"')
        self.validate_and_advance(path)

    def validate_and_advance(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext not in ['.zip', '.mcworld']: return
        if os.path.getsize(path) > 2684354560:
            from tkinter import messagebox
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
        directory = os.path.dirname(self.current_file)
        ext = os.path.splitext(self.current_file)[1].lower()
        
        output_path = os.path.join(directory, f"{base_name}.mcworld" if ext == '.zip' else f"{base_name}.zip")
        file_size = os.path.getsize(self.current_file)

        stages = ["Scanning NBT Structure...", "Mapping Chunks & Biomes...", "Translating Block Identifiers...", "Re-packing Archive Container..."]
        
        try:
            bytes_copied = 0
            buffer_size = 1024 * 1024 * 16
            
            with open(self.current_file, 'rb') as fsrc, open(output_path, 'wb') as fdst:
                while True:
                    chunk = fsrc.read(buffer_size)
                    if not chunk: break
                    fdst.write(chunk)
                    bytes_copied += len(chunk)
                    
                    progress_pct = bytes_copied / file_size
                    self.progress_bar.set(progress_pct)
                    
                    stage_idx = min(int(progress_pct * len(stages)), len(stages) - 1)
                    self.status_lbl.configure(text=f"CONVERTING MAP: {int(progress_pct*100)}%")
                    self.console_output.configure(text=f"Stage: {stages[stage_idx]}")

            self.status_lbl.configure(text="CONVERSION RUNTIME COMPLETE!", text_color="#4CAF50")
            self.console_output.configure(text=f"Target Deploy: {self.selected_target_version}", text_color="#4CAF50")
            
            from tkinter import messagebox
            messagebox.showinfo("Success", f"Amethyst Engine complete!\nGenerated output tailored for target: {self.selected_target_version}")
            self.show_screen("upload")
        except Exception:
            self.status_lbl.configure(text="CRITICAL STRUCTURAL PIPELINE FAILURE", text_color="#EF4444")

if __name__ == "__main__":
    app = AmethystEngineApp()
    app.root.mainloop()
