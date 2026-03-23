# 📖 User Guide: Manannán Digitization Lab

Welcome to the **Manannán Digitization Lab**. This tool is designed to simplify the complex task of modernizing 1940s Irish-language science fiction through an automated, intelligent pipeline.

---

## 🚀 Getting Started

To launch the dashboard, open your terminal and run:

```powershell
# Navigate to the Data root
cd C:\github\Manannan

# Run the app
streamlit run python-utils/streamlit_app.py
```

*Note: Ensure you are using the correct Python environment where Streamlit is installed.*

---

## ⚙️ Workspace Configuration (Sidebar)

Before processing, ensure your project paths are set correctly in the **Sidebar**:
- **📊 Data Root**: The directory containing your chapters (`caibidlí`).
- **🛠️ Toolkit Root**: The directory containing the Python scripts (`ManannanUtils`).

Use the **📁 button** next to each path to browse your local file system natively.

---

## 🧙‍♂️ The Wizard Workflow

The application uses a guided **Wizard Interface** at the top. Active stages are highlighted in green, while future stages are greyed out until unlocked.

### Stage 1: Chapter Selection
Click the **📁 Browse Local Files** button in the main panel.
- Select a Markdown file from `caibidlí/old-orthography`.
- Once selected, the wizard will automatically advance to the next stage.

### Stage 2: OCR Repair
Click **🚀 Run OCR Fixer**.
- **What it does:** It applies linguistic heuristics and repairs common OCR hallucinations.
- **Results:** Review the **Ambiguous Matches Report** at the bottom of the page to catch edge cases like `ar` vs `ár`.

### Stage 3: Modernization
Click **🛠️ Modernize Text**.
- **What it does:** Replaces dotted *Cló Gaelach* characters with modern "h" sequences.
- **Output:** The file is saved to the `new-orthography` folder automatically.

### Stage 4: Verification
Click **🔍 Open Folder** to view the results in Windows Explorer.
- You can click **🔄 Restart Pipeline** to clear the session and process a new chapter.

---

## 🔍 Understanding the Reports

The **Ambiguous Matches Report** table remains visible throughout the pipeline:
- **Line:** Location in the original file.
- **Word:** The specific term flagged (ambiguous or potential new error).
- **Context:** Surrounding phrase for quick linguistic review.

---

## ❓ Troubleshooting
- **NameError / Definition Issues:** Ensure you have the latest `streamlit_app.py` where functions are defined at the top.
- **File Dialog Hidden:** If the "Browse" button doesn't seem to work, check if the Windows Explorer dialog opened behind your browser window.
- **Missing Config:** The toolkit expects a `config` folder within your `python-utils` directory.
