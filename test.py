
import os
import shutil
import re
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
config_toml_path = os.path.join(BASE_DIR, '.chainlit/config.toml')


# Function to inject styles and scripts into config.toml
def inject_themeing():

    # Update config.toml
    print("HI.", config_toml_path)
    if os.path.exists(config_toml_path):
        with open(config_toml_path, 'r') as f:
            config_data = f.read()

        # Update or insert custom_css and custom_js
        config_data = re.sub(r'# custom_css\s*=\s*".*?"', 'custom_css = "public/custom_style.css"', config_data)
        config_data = re.sub(r'# custom_js\s*=\s*".*?"', 'custom_js = "public/custom.js"', config_data)

        # Ensure the [UI] section exists
        if "[UI]" not in config_data:
            config_data += "\n[UI]\n"

        # If keys didn't exist, add them
        if '# custom_css =' not in config_data:
            config_data += '\ncustom_css = "public/custom.css"\n'
        if '# custom_js =' not in config_data:
            config_data += 'custom_js = "public/custom.js"\n'

        # Save back the updated config file
        with open(config_toml_path, 'w') as f:
            f.write(config_data)

        print("✅ Updated config.toml: Injected/Updated custom.js and custom.css.")

inject_themeing()
