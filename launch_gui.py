"""
Launcher for the Manannán Digitization Lab.

Usage:
    python launch_gui.py              # Auto-detect best available UI
    python launch_gui.py --ui tkinter # Force lightweight Tkinter UI (zero dependencies)
    python launch_gui.py --ui streamlit # Force Streamlit web UI (requires: pip install streamlit)
"""
import argparse
import os
import sys
import subprocess

def is_streamlit_available():
    """Check whether streamlit is installed without importing it."""
    try:
        import importlib
        importlib.import_module("streamlit")
        return True
    except ImportError:
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Launch the Manannán Digitization Lab UI",
        epilog="The Tkinter UI has zero external dependencies. "
               "The Streamlit UI requires: pip install streamlit"
    )
    parser.add_argument(
        "--ui",
        choices=["streamlit", "tkinter", "auto"],
        default="auto",
        help="Choose the UI framework (default: auto-detect)"
    )
    args = parser.parse_args()

    ui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui")

    # Resolve 'auto' mode
    if args.ui == "auto":
        if is_streamlit_available():
            args.ui = "streamlit"
        else:
            args.ui = "tkinter"

    if args.ui == "tkinter":
        print("Launching Tkinter Dashboard (lightweight, no external dependencies)...")
        script = os.path.join(ui_dir, "app_tkinter.py")
        subprocess.run([sys.executable, script])

    elif args.ui == "streamlit":
        if not is_streamlit_available():
            print("ERROR: Streamlit is not installed.")
            print("       Install it with:  pip install streamlit")
            print("       Or use the Tkinter UI:  python launch_gui.py --ui tkinter")
            sys.exit(1)
        print("Launching Streamlit Dashboard (web UI)...")
        script = os.path.join(ui_dir, "app_streamlit.py")
        subprocess.run([sys.executable, "-m", "streamlit", "run", script])

if __name__ == "__main__":
    main()
