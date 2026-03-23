import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys

# Ensure ui directory is in path so we can import engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import DigitizationEngine

class TkinterDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🛸 Manannán Digitization Lab - Tkinter Edition")
        self.root.geometry("1000x700")
        self.engine = DigitizationEngine()

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 10), padding=5)
        self.style.configure('TLabel', font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'))
        self.style.configure('Active.TLabel', foreground='#00ff7f', font=('Segoe UI', 10, 'bold'))

        self.selected_file = None
        self.ocr_completed = False
        self.modernization_completed = False
        self.current_step = 1

        self.setup_ui()

    def setup_ui(self):
        # Top Header
        self.header_frame = ttk.Frame(self.root, padding=20)
        self.header_frame.pack(fill='x')
        ttk.Label(self.header_frame, text="🛸 Manannán Digitization Lab", style='Header.TLabel').pack()

        # Notebook for Tabs (Pipeline vs Settings)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Tab 1: Pipeline
        self.pipeline_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.pipeline_tab, text="Workflow Pipeline")

        # Tab 2: Settings
        self.settings_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.settings_tab, text="⚙️ Settings")

        self.setup_settings_tab()
        self.setup_pipeline_tab()

    def setup_settings_tab(self):
        ttk.Label(self.settings_tab, text="Workspace Configuration", style='Header.TLabel').pack(pady=(0, 20), anchor='w')
        
        form_frame = ttk.Frame(self.settings_tab)
        form_frame.pack(fill='x')

        ttk.Label(form_frame, text="Data Root Directory:").grid(row=0, column=0, sticky='w', pady=5)
        
        self.data_root_var = tk.StringVar(value=self.engine.data_root)
        dr_entry = ttk.Entry(form_frame, textvariable=self.data_root_var, width=60)
        dr_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Button(form_frame, text="Browse...", command=self.browse_data_root).grid(row=0, column=2, pady=5)
        
        ttk.Button(self.settings_tab, text="Save Settings", command=self.save_settings).pack(pady=20, anchor='w')

    def browse_data_root(self):
        d = filedialog.askdirectory(initialdir=self.engine.data_root, title="Select Data Root")
        if d:
            self.data_root_var.set(d)

    def save_settings(self):
        self.engine.save_config(self.data_root_var.get())
        messagebox.showinfo("Settings", "Workspace settings saved successfully.")

    def setup_pipeline_tab(self):
        # Wizard Indicators
        self.wizard_frame = ttk.Frame(self.pipeline_tab, padding=(0, 0, 0, 20))
        self.wizard_frame.pack(fill='x')
        self.step_labels = []
        stages = ["📁 Selection", "✨ OCR Repair", "📖 Modernization", "✅ Verification"]
        for idx, stage in enumerate(stages):
            lbl = ttk.Label(self.wizard_frame, text=stage, width=20, anchor='center')
            lbl.grid(row=0, column=idx, padx=10, sticky='ew')
            self.step_labels.append(lbl)
            self.wizard_frame.columnconfigure(idx, weight=1)

        ttk.Separator(self.pipeline_tab, orient='horizontal').pack(fill='x', pady=(0, 20))

        # Main Content Area
        self.main_area = ttk.Frame(self.pipeline_tab)
        self.main_area.pack(fill='both', expand=True)

        self.render_step_1()

    def update_wizard(self, step):
        for idx, lbl in enumerate(self.step_labels):
            if idx + 1 == step:
                lbl.configure(style='Active.TLabel')
            else:
                lbl.configure(style='TLabel')

    def clear_main(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    # --- STEP 1: SELECTION ---
    def render_step_1(self):
        self.current_step = 1
        self.update_wizard(1)
        self.clear_main()

        ttk.Label(self.main_area, text="Step 1: Chapter Selection", style='Header.TLabel').pack(pady=(0, 20))
        ttk.Label(self.main_area, text="Select a raw OCR output file from the old-orthography directory.").pack()
        
        file_frame = ttk.Frame(self.main_area)
        file_frame.pack(fill='x', pady=20)
        
        self.file_path_var = tk.StringVar(value=self.selected_file or "")
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, font=('Segoe UI', 10))
        self.file_entry.config(state='readonly')
        self.file_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        ttk.Button(file_frame, text="📁 Browse Files", command=self.browse_file).pack(side='left')

        self.next_btn = ttk.Button(self.main_area, text="Proceed to OCR Repair ➡️", command=self.render_step_2)
        if not self.selected_file:
            self.next_btn.config(state='disabled')
        self.next_btn.pack(pady=40)

    def browse_file(self):
        path = filedialog.askopenfilename(
            initialdir=self.engine.get_default_directory(),
            title="Select Chapter for Processing",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if path:
            self.selected_file = path
            self.file_path_var.set(path)
            self.next_btn.config(state='normal')

    # --- STEP 2: OCR REPAIR ---
    def render_step_2(self):
        self.current_step = 2
        self.update_wizard(2)
        self.clear_main()

        ttk.Label(self.main_area, text="Step 2: OCR Heuristics & Repair", style='Header.TLabel').pack(pady=(0, 20))
        ttk.Label(self.main_area, text=f"File: {os.path.basename(self.selected_file)}").pack(pady=5)

        self.ocr_btn = ttk.Button(self.main_area, text="✨ Run OCR Fixer", command=self.run_ocr)
        self.ocr_btn.pack(pady=20)

        # Report Area
        rep_lbl = ttk.Label(self.main_area, text="Ambiguous Matches Report:")
        rep_lbl.pack(fill='x', pady=(10, 0))
        
        self.report_tree = ttk.Treeview(self.main_area, columns=('Line', 'Word', 'Context'), show='headings', height=8)
        self.report_tree.heading('Line', text='Line')
        self.report_tree.heading('Word', text='Word')
        self.report_tree.heading('Context', text='Context')
        self.report_tree.column('Line', width=50, anchor='center')
        self.report_tree.column('Word', width=150)
        self.report_tree.column('Context', width=500)
        self.report_tree.pack(fill='both', expand=True, pady=10)

        nav_frame = ttk.Frame(self.main_area)
        nav_frame.pack(fill='x', pady=20)
        ttk.Button(nav_frame, text="⬅️ Back", command=self.render_step_1).pack(side='left')
        self.ocr_next_btn = ttk.Button(nav_frame, text="Proceed ➡️", command=self.render_step_3)
        self.ocr_next_btn.pack(side='right')
        
        if not self.ocr_completed:
            self.ocr_next_btn.config(state='disabled')
        else:
            self.refresh_report_tree()

    def run_ocr(self):
        self.ocr_btn.config(state='disabled', text="Analyzing...")
        self.root.update()
        success, stdout, stderr = self.engine.run_ocr_fixer(self.selected_file)
        self.ocr_btn.config(state='normal', text="✨ Run OCR Fixer")
        
        if success:
            self.ocr_completed = True
            self.ocr_next_btn.config(state='normal')
            self.refresh_report_tree()
            messagebox.showinfo("Success", "OCR Fixer completed! Check the report table for ambiguous terms.")
        else:
            messagebox.showerror("Engine Failure", f"OCR Fixer failed to execute:\n{stderr}")

    def refresh_report_tree(self):
        for i in self.report_tree.get_children():
            self.report_tree.delete(i)
        matches = self.engine.load_report()
        for m in matches:
            self.report_tree.insert('', 'end', values=(m['line'], m['word'], m['context']))

    # --- STEP 3: MODERNIZATION ---
    def render_step_3(self):
        self.current_step = 3
        self.update_wizard(3)
        self.clear_main()

        ttk.Label(self.main_area, text="Step 3: Orthographic Modernization", style='Header.TLabel').pack(pady=(0, 20))
        ttk.Label(self.main_area, text="Converting Cló Gaelach characters to modern 'h' equivalents.").pack(pady=(0, 20))
        
        self.mod_btn = ttk.Button(self.main_area, text="🛠️ Run Modernizer", command=self.run_modernizer)
        self.mod_btn.pack(pady=20)

        nav_frame = ttk.Frame(self.main_area)
        nav_frame.pack(fill='x', pady=20)
        ttk.Button(nav_frame, text="⬅️ Back", command=self.render_step_2).pack(side='left')
        self.mod_next_btn = ttk.Button(nav_frame, text="Proceed to Verification ✅", command=self.render_step_4)
        self.mod_next_btn.pack(side='right')

        if not self.modernization_completed:
            self.mod_next_btn.config(state='disabled')

    def run_modernizer(self):
        self.mod_btn.config(state='disabled', text="Converting...")
        self.root.update()
        success, output_path, stderr = self.engine.run_modernizer(self.selected_file)
        self.mod_btn.config(state='normal', text="🛠️ Run Modernizer")
        
        if success:
            self.modernization_completed = True
            self.mod_next_btn.config(state='normal')
            messagebox.showinfo("Success", f"Modernization complete!\n\nSaved gracefully to:\n{output_path}")
        else:
            messagebox.showerror("Engine Failure", f"Modernizer failed:\n{stderr}")

    # --- STEP 4: VERIFICATION ---
    def render_step_4(self):
        self.current_step = 4
        self.update_wizard(4)
        self.clear_main()

        ttk.Label(self.main_area, text="Step 4: Verification", style='Header.TLabel').pack(pady=(0, 20))
        ttk.Label(self.main_area, text="Processing complete for this chapter.", font=('Segoe UI', 12)).pack(pady=10)
        
        ttk.Button(self.main_area, text="📂 Open Output Folder", command=self.engine.open_output_folder).pack(pady=10)
        ttk.Button(self.main_area, text="🔄 Restart Pipeline", command=self.reset).pack(pady=10)

    def reset(self):
        self.selected_file = None
        self.ocr_completed = False
        self.modernization_completed = False
        self.render_step_1()

if __name__ == "__main__":
    app_root = tk.Tk()
    app = TkinterDashboard(app_root)
    app_root.mainloop()
