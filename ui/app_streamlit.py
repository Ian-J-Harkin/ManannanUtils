import streamlit as st
import os
import sys
import glob

# Ensure ui directory is in path so we can import engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import DigitizationEngine

# Configuration - Initialized via engine
if 'engine' not in st.session_state:
    st.session_state.engine = DigitizationEngine()

st.set_page_config(
    page_title="Manannán Digitization Lab", 
    page_icon="🛸",
    layout="wide"
)

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🛸</h1>", unsafe_allow_html=True)
    st.title("⚙️ Workspace Settings")
    
    new_data_root = st.text_input("📊 Data Root", value=st.session_state.engine.data_root)
    new_old_folder = st.text_input("📁 Input Folder", value=st.session_state.engine.old_folder)
    new_new_folder = st.text_input("📦 Output Folder", value=st.session_state.engine.new_folder)
    
    if st.button("💾 Save Settings", use_container_width=True):
        st.session_state.engine.save_config(new_data_root, new_old_folder, new_new_folder)
        st.success("Settings saved to workspace config!")
        st.rerun()
    
    st.divider()
    st.markdown("### 🔍 System Info")
    st.write(f"Python: `{sys.version.split(' ')[0]}`")
    st.write(f"Environment: `{os.path.basename(sys.prefix)}`")

# Custom Styling for Premium Wizard Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #e0e0e0; }
    .stButton>button { border-radius: 8px; height: 3em; transition: all 0.3s ease; font-weight: bold; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,255,127,0.3); border-color: #00ff7f; }
    
    /* Wizard Steps styling */
    .step-container { display: flex; justify-content: space-between; margin-bottom: 2rem; padding: 1rem; background: #1a1c24; border-radius: 12px; }
    .step { flex: 1; text-align: center; padding: 10px; border-bottom: 4px solid #333; color: #888; transition: all 0.5s; position: relative;}
    .step-active { border-bottom: 4px solid #00ff7f; color: #00ff7f; font-weight: bold; }
    .step-complete { border-bottom: 4px solid #4a90e2; color: #4a90e2; }
    .step-icon { font-size: 1.2rem; margin-bottom: 5px; }
    
    /* Report Table */
    .report-table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
    .report-table th { background: #1a1c24; color: #00ff7f; padding: 10px; text-align: left; }
    .report-table td { padding: 10px; border-bottom: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛸 Manannán Digitization Lab")

# --- Session State Persistence ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None
if 'ocr_completed' not in st.session_state:
    st.session_state.ocr_completed = False
if 'modernization_completed' not in st.session_state:
    st.session_state.modernization_completed = False

# --- Wizard Logic ---
def go_to_step(n):
    st.session_state.step = n

def get_available_files():
    """List .md files from the configured input directory."""
    input_dir = st.session_state.engine.get_default_directory()
    if os.path.isdir(input_dir):
        files = sorted(glob.glob(os.path.join(input_dir, "*.md")))
        return files
    return []

# --- Wizard UI Component ---
stages = [("📁 Selection", 1), ("✨ OCR Repair", 2), ("📖 Modernize", 3), ("✅ Verification", 4)]

def render_wizard_header():
    cols = st.columns(len(stages))
    for i, (label, step_val) in enumerate(stages):
        status_class = ""
        if st.session_state.step == step_val: status_class = "step-active"
        elif st.session_state.step > step_val: status_class = "step-complete"
        
        with cols[i]:
            st.markdown(f"""
                <div class="step {status_class}">
                    <div class="step-icon">{label.split(' ')[0]}</div>
                    <div>{label.split(' ')[1]}</div>
                </div>
            """, unsafe_allow_html=True)

render_wizard_header()
st.divider()

# --- STAGE 1: Selection ---
if st.session_state.step == 1:
    st.subheader("Stage 1: Chapter Source Selection")
    st.info(f"Select a raw OCR output file from the `{st.session_state.engine.old_folder}` directory.")
    
    available_files = get_available_files()
    
    if available_files:
        display_names = [os.path.basename(f) for f in available_files]
        selected_idx = st.selectbox(
            "Available Chapters",
            range(len(display_names)),
            format_func=lambda i: display_names[i],
            index=None,
            placeholder="Select a chapter..."
        )
        if selected_idx is not None:
            st.session_state.selected_file = available_files[selected_idx]
    else:
        st.warning(f"No `.md` files found in `{st.session_state.engine.get_default_directory()}`. Check your Workspace Settings or enter a path manually below.")
    
    manual_path = st.text_input("Or enter a file path manually:", value=st.session_state.selected_file or "")
    if manual_path and os.path.isfile(manual_path):
        st.session_state.selected_file = manual_path

    if st.session_state.selected_file:
        st.success(f"Ready: `{os.path.basename(st.session_state.selected_file)}`")
        if st.button("Proceed to OCR Repair ➡️", type="primary"):
            st.session_state.ocr_completed = False
            st.session_state.modernization_completed = False
            go_to_step(2)
            st.rerun()

# --- STAGE 2: OCR Repair ---
elif st.session_state.step == 2:
    st.subheader("Stage 2: OCR Heuristics & Repair")
    st.write(f"Working on: `{os.path.basename(st.session_state.selected_file)}`")
    
    if st.button("✨ Run OCR Fixer", type="primary", use_container_width=True):
        with st.spinner("Executing linguistic repair engine..."):
            success, stdout, stderr = st.session_state.engine.run_ocr_fixer(st.session_state.selected_file)
            if success:
                st.session_state.ocr_completed = True
                st.success("OCR Fixer successful! Review the report below.")
                if stderr:
                    with st.expander("Technical Logs"):
                        st.code(stderr)
            else:
                st.error("Engine failure:")
                st.code(stderr)

    if st.session_state.ocr_completed:
        matches = st.session_state.engine.load_report()
        if matches:
            st.warning(f"Found {len(matches)} items requiring human attention.")
            st.table([{"Line": m['line'], "Word": m['word'], "Context": m['context']} for m in matches])
        else:
            st.success("No ambiguous patterns detected.")
        
        st.divider()
        if st.button("Proceed to Modernization ➡️", type="primary"):
            go_to_step(3)
            st.rerun()

    if st.button("⬅️ Back to Selection"):
        go_to_step(1)
        st.rerun()

# --- STAGE 3: Modernization ---
elif st.session_state.step == 3:
    st.subheader("Stage 3: Orthographic Modernization")
    st.write("Converting Cló Gaelach (dotted) characters to modern 'h' equivalents.")
    
    if st.button("🛠️ Run Modernizer", type="primary", use_container_width=True):
        with st.spinner("Performing character mapping..."):
            success, output_path, stderr = st.session_state.engine.run_modernizer(st.session_state.selected_file)
            if success:
                st.session_state.modernization_completed = True
                st.success(f"Modernization complete! Saved to:\n`{output_path}`")
            else:
                st.error("Modernizer failed:")
                st.code(stderr)

    if st.session_state.modernization_completed:
        if st.button("Proceed to Verification ➡️", type="primary"):
            go_to_step(4)
            st.rerun()

    if st.button("⬅️ Back to OCR Repair"):
        go_to_step(2)
        st.rerun()

# --- STAGE 4: Verification ---
elif st.session_state.step == 4:
    st.subheader("Stage 4: Final Verification")
    st.balloons()
    st.success("Processing complete for this chapter.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📂 Open Output Folder", use_container_width=True):
            if not st.session_state.engine.open_output_folder():
                st.error("Folder not found.")
    
    with col2:
        if st.button("🔄 Restart Pipeline", use_container_width=True):
            st.session_state.step = 1
            st.session_state.selected_file = None
            st.session_state.ocr_completed = False
            st.session_state.modernization_completed = False
            st.rerun()

    st.divider()
    st.markdown("### Next Steps")
    st.markdown("- Perform manual proofreading of the output file.")
    st.markdown("- Add any recurring errors to `corrections_dict.json` using the Fine-Tuning utility.")
