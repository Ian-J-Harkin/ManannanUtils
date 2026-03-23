import argparse
import os
import sys
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Launch the Manannán Digitization Lab UI")
    parser.add_argument("--ui", choices=["streamlit", "tkinter"], default="streamlit", help="Choose the UI framework to run (default: streamlit)")
    args = parser.parse_args()

    utils_root = os.path.dirname(os.path.abspath(__file__))
    ui_dir = os.path.join(utils_root, "ui")

    if args.ui == "tkinter":
        print("Launching Tkinter Dashboard...")
        script = os.path.join(ui_dir, "app_tkinter.py")
        subprocess.run([sys.executable, script])
    elif args.ui == "streamlit":
        print("Launching Streamlit Dashboard...")
        script = os.path.join(ui_dir, "app_streamlit.py")
        subprocess.run([sys.executable, "-m", "streamlit", "run", script])

if __name__ == "__main__":
    main()
