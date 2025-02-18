
import os
import shutil
import re
import subprocess


# Function to inject styles and scripts into config.toml
def run_chainlit_commands():
    """Runs the necessary PNPM commands in sequence."""
    try:
        subprocess.run(["pip", "install", "chainlit"], check=True)
        print("🚀 installing chainlit...")

        subprocess.run(["chainlit", "run", "demo.py", "-w"], check=True)
        print("🚀 Running install...")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running chainlit command: {e}")

run_chainlit_commands()
