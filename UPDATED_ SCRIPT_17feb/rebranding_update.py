""" updates/notes
inject_themeing() we can add variables for the custom.css/custom.js
".chainlit" will add to the project after "pnpm run preinstall" & "pnpm run install" & "pnpm run dev"
"""


import json
import os
import shutil
import re
import subprocess



# Define paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the path to main.tsx
main_tsx_path = os.path.join(BASE_DIR, 'frontend/src/main.tsx')

# Paths for colors
theme_json_path = os.path.join(BASE_DIR, 'public/theme.json')
css_file_path = os.path.join(BASE_DIR, 'frontend/src/index.css')

# Paths for logos
public_dir = os.path.join(BASE_DIR, 'public')
our_logo_dark = os.path.join(BASE_DIR, 'rebranding_assets/logo_dark.png')
our_logo_light = os.path.join(BASE_DIR, 'rebranding_assets/logo_light.png')
our_favicon = os.path.join(BASE_DIR, 'rebranding_assets/favicon.png')

# Paths for footer updates
our_logo_light_svg = os.path.join(BASE_DIR, 'rebranding_assets/logo_light.svg')
our_logo_dark_svg  = os.path.join(BASE_DIR, 'rebranding_assets/logo_dark.svg')
watermark_tsx  = os.path.join(BASE_DIR, 'frontend/src/components/WaterMark.tsx')

# Paths for theming (config.toml)
config_toml_path = os.path.join(BASE_DIR, '.chainlit/config.toml')

# Paths for localization
translations_dir = os.path.join(BASE_DIR, '.chainlit/translations')
new_translations_dir = os.path.join(BASE_DIR, 'rebranding_assets/translations')

lang_toggle_tsx = os.path.join(BASE_DIR, 'frontend/src/components/i18n/langToggle.tsx')

# Paths for RTL updates
header_index_tsx = os.path.join(BASE_DIR, 'frontend/src/components/header/index.tsx')
dialog_tsx = os.path.join(BASE_DIR, 'frontend/src/components/ui/dialog.tsx')
mixins_scss = os.path.join(BASE_DIR, 'frontend/src/styles/_mixins.scss')
custom_styles_scss = os.path.join(BASE_DIR, 'frontend/src/styles/_custom_stylesheets.scss')



def run_pnpm_commands():
    """Runs the necessary PNPM commands in sequence."""
    try:
        subprocess.run(["cd", "frontend"], check=True)

        print("🚀 Running preinstall...")
        subprocess.run(["pnpm", "run", "preinstall"], check=True)
        # subprocess.run(["npx", "pnpm", "run", "preinstall"], check=True)

        print("🚀 Running install...")
        subprocess.run(["pnpm", "install"], check=True)

        print("🚀 Starting dev server...")
        subprocess.run(["pnpm", "run", "dev"], check=True)

        print("✅ PNPM commands executed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running PNPM command: {e}")


def run_chainlit_commands():
    """Runs the necessary Chainlit commands in sequence."""
    try:
        subprocess.run(["pip", "install", "chainlit"], check=True)
        print("🚀 installing chainlit...")
        # subprocess.run(["chainlit", "run", "demo.py", "-w"], check=True)
        # print("🚀 Running install...")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running chainlit command: {e}")


def pre_tasks():
    """Ensure /public folder exists, copy theme.json, and move demo.py to BASE_DIR."""
    public_dir = os.path.join(BASE_DIR, 'public')
    theme_json_source = os.path.join(BASE_DIR, 'rebranding_assets/theme.json')
    theme_json_dest = os.path.join(public_dir, 'theme.json')
    demo_py_source = os.path.join(BASE_DIR, 'rebranding_assets/demo.py')
    demo_py_dest = os.path.join(BASE_DIR, 'demo.py')

    # Create /public folder if it doesn't exist
    os.makedirs(public_dir, exist_ok=True)

    # Copy theme.json to /public
    if os.path.exists(theme_json_source):
        shutil.copy(theme_json_source, theme_json_dest)
        print("✅ Copied theme.json to /public folder.")
    else:
        print("⚠️ theme.json not found in rebranding_assets. Skipping copy.")

    # Move demo.py to BASE_DIR - to test the rebranding
    if os.path.exists(demo_py_source):
        shutil.copy(demo_py_source, demo_py_dest)
        print("✅ Moved demo.py to BASE_DIR, You can run ⭐ `pip install chainlit` ==> `chainlit run demo.py -w`.")
    else:
        print("⚠️ demo.py not found in assets, You can run ⭐ `pip install chainlit` ==> `chainlit hello`.")



def replace_text_safely( search_text, replace_text, file_extensions=None, backup=True):
    EXCLUDED_FILES = ["rebranding_update.py"]  # List of files to exclude from modifications

    """
    Safely searches and replaces text in project files while preserving Python code integrity.

    Args:
        search_text (str): The text to search for.
        replace_text (str): The text to replace it with.
        file_extensions (list): A list of file extensions to scan (default: source code and config files).
        backup (bool): Whether to create a backup of modified files.
    """
    if file_extensions is None:
        file_extensions = ['.py', '.tsx', '.js', '.json', '.css', '.scss', '.toml', '.html']  # Safe text-based formats

    for root, _, files in os.walk(BASE_DIR):
        # Skip certain directories (to prevent breaking dependencies)
        if any(skip in root for skip in ['node_modules', '.git', 'venv', '__pycache__']):
            continue

        for file in files:
            if file in EXCLUDED_FILES:  # Skip the excluded file(s)
                print(f"⏭️ Skipping file: {file}")
                continue

            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)

                # Read the file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Use regex to prevent replacing inside Python variables/functions
                new_content = re.sub(rf"\b{re.escape(search_text)}\b", replace_text, content)

                if new_content != content:
                    if backup:
                        shutil.copy(file_path, file_path + ".bak")  # Create a backup before modifying
                        print(f"🔄 Backup created: {file_path}.bak")

                    # Write back the modified content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    print(f"✅ Replaced occurrences in: {file_path}")


def update_header():
    # Modify `header/index.tsx` to comment out `<ReadmeButton />`
    if os.path.exists(header_index_tsx):
        with open(header_index_tsx, 'r') as f:
            header_content = f.read()

        # Step 1️⃣: Comment out <ReadmeButton />
        if "<ReadmeButton" in header_content:
            header_content = re.sub( r'(<ReadmeButton\s*/?>)', r'{/* \1 */}', header_content )

        # Save changes to header/index.tsx
        with open(header_index_tsx, 'w') as f:
            f.write(header_content)

        print("✅ Commented out <ReadmeButton /> in header/index.tsx.")


# Function to update colors
def update_colors():
    # Define separate replacements for light and dark themes
    css_replacements_light = {
        "--primary": "271 52% 45%",
        "--secondary": "0 0% 19%",
        "--accent": "0 0% 26%",
        "--destructive": "0 62.8% 30.6%"
    }
    css_replacements_dark = {
        "--primary": "271 52% 45%",
        "--secondary": "210 50% 80%",
        "--accent": "0 0% 26%",
        "--destructive": "0 62.8% 30.6%"
    }

    # Function to update colors in CSS
    if os.path.exists(css_file_path):
        with open(css_file_path, 'r') as f:
            css_data = f.read()

        # Update light theme
        for key, new_value in css_replacements_light.items():
            css_data = re.sub(rf"(\s*{re.escape(key)}\s*:\s*)\d+(\.\d+)?\s+\d+(\.\d+)?%\s+\d+(\.\d+)?%;",
                              lambda m: f"{m.group(1)}{new_value};", css_data)

        # Update dark theme
        for key, new_value in css_replacements_dark.items():
            css_data = re.sub(rf"(\.dark\s*{{[\s\S]*?{re.escape(key)}\s*:\s*)\d+(\.\d+)?\s+\d+(\.\d+)?%\s+\d+(\.\d+)?%;",
                              lambda m: f"{m.group(1)}{new_value};", css_data)

        # Ensure proper formatting
        css_data = re.sub(r"\n\n+", "\n", css_data).strip()

        with open(css_file_path, 'w') as f:
            f.write(css_data)

        print("✅ Updated index.css with new light and dark theme colors.")


    # Function to update colors in theme.json
    if os.path.exists(theme_json_path):
        with open(theme_json_path, 'r') as f:
            theme_data = json.load(f)

        theme_data.update({
            "light": css_replacements_light,
            "dark": css_replacements_dark
        })

        with open(theme_json_path, 'w') as f:
            json.dump(theme_data, f, indent=4)

        print("✅ Updated theme.json with new light and dark theme colors.")



# Function to replace logos
def replace_logos():
    #  copy(new, old) means copy from [rebranding_assets] to [main_dir]
    shutil.copy(our_logo_dark, os.path.join(public_dir, 'logo_dark.png'))
    shutil.copy(our_logo_light, os.path.join(public_dir, 'logo_light.png'))
    shutil.copy(our_favicon, os.path.join(public_dir, 'favicon.png'))
    print("Replaced logos.")


def replace_favicon():
    """Replace the favicon in frontend/public with the new one from rebranding_assets."""
    source_favicon = os.path.join(BASE_DIR, 'rebranding_assets/favicon.svg')
    destination_favicon = os.path.join(BASE_DIR, 'frontend/public/favicon.svg')

    if os.path.exists(source_favicon):
        shutil.copy(source_favicon, destination_favicon)
        print("✅ Favicon replaced successfully in frontend/public.")
    else:
        print("⚠️ favicon.svg not found in rebranding_assets. Skipping replacement.")


# Function to update footer
def update_footer():
    #  copy(new, old) means copy from [rebranding_assets] to [main_dir]
    shutil.copy(our_logo_light_svg, os.path.join(BASE_DIR, 'frontend/src/assets/logo_light.svg'))
    shutil.copy(our_logo_dark_svg, os.path.join(BASE_DIR, 'frontend/src/assets/logo_dark.svg'))


    with open(watermark_tsx, 'r') as f:
        content = f.read()
    content = content.replace('https://github.com/Chainlit/chainlit', 'https://arabot.io/')
    with open(watermark_tsx, 'w') as f:
        f.write(content)
    print("✅ Updated footer and watermark.")


# Function to inject styles and scripts into config.toml
def inject_themeing():
    # Paths to theme assets
    custom_js_source = os.path.join(BASE_DIR, 'rebranding_assets/custom.js')
    custom_css_source = os.path.join(BASE_DIR, 'rebranding_assets/custom.css')

    custom_js_dest = os.path.join(BASE_DIR, 'public/custom.js')
    custom_css_dest = os.path.join(BASE_DIR, 'public/custom.css')

    # Copy custom.js and custom.css to the public folder, before the next steps
    if os.path.exists(custom_js_source):
        shutil.copy(custom_js_source, custom_js_dest)
    if os.path.exists(custom_css_source):
        shutil.copy(custom_css_source, custom_css_dest)
    print("✅ Copied custom.js & custom.css to public folder.")

    # Update config.toml - it should be after >pip install chainlit
    if os.path.exists(config_toml_path):
        with open(config_toml_path, 'r') as f:
            config_data = f.read()

        # Ensure the [UI] section exists
        if "[UI]" not in config_data:
            config_data += "\n[UI]\n"

        # Check if the [UI] section is already there
        ui_section_match = re.search(r'(\[UI\])([\s\S]*?)(?=\n\[|\Z)', config_data)
        if ui_section_match:
            ui_section_content = ui_section_match.group(2)

            # Update or insert custom_css and custom_js
            if "custom_css =" in ui_section_content:
                ui_section_content = re.sub(r'# custom_css\s*=\s*".*?"', 'custom_css = "public/custom.css"', ui_section_content)
            else:
                ui_section_content += '\ncustom_css = "public/custom.css"'

            if "custom_js =" in ui_section_content:
                ui_section_content = re.sub(r'# custom_js\s*=\s*".*?"', 'custom_js = "public/custom.js"', ui_section_content)
            else:
                ui_section_content += '\ncustom_js = "public/custom.js"'

            # Replace the original [UI] section with the updated content
            config_data = re.sub(r'(\[UI\])([\s\S]*?)(?=\n\[|\Z)', f'\\1{ui_section_content}', config_data)

        # Save back the updated config file
        with open(config_toml_path, 'w') as f:
            f.write(config_data)

        print("✅ Updated config.toml: Injected/Updated custom.js and custom.css under [UI].")


    # Injects custom CSS import after index.css import in main.tsx.
    if os.path.exists(main_tsx_path):
        with open(main_tsx_path, 'r') as f:
            main_tsx_content = f.read()

        # Ensure the custom style import is added after index.css import
        if "import './index.css';" in main_tsx_content and "import '../../public/custom.css';" not in main_tsx_content:
            main_tsx_content = main_tsx_content.replace(
                "import './index.css';",
                "import './index.css'; \nimport '../../public/custom.css';"
            )

            with open(main_tsx_path, 'w') as f:
                f.write(main_tsx_content)
            print("✅ Injected custom-style.css import in main.tsx.")
        else:
            print("⚠️ custom-style.css import already exists or index.css import is missing.")


# Function to update icons - If there are any messages (starters) requires icons
def update_icons():
    icons_dir = os.path.join(BASE_DIR, 'frontend/public/icons')
    outer_public_icons_dir = os.path.join(BASE_DIR, 'public/icons')
    new_icons_dir = os.path.join(BASE_DIR, 'rebranding_assets/icons')

    # Ensure the icons directory exists
    os.makedirs(icons_dir, exist_ok=True)
    os.makedirs(outer_public_icons_dir, exist_ok=True)

    # Copy SVG icons from rebranding_assets/icons to frontend/public/icons
    for icon in os.listdir(new_icons_dir):
        if icon.endswith('.svg'):
            shutil.copy(os.path.join(new_icons_dir, icon), os.path.join(outer_public_icons_dir, icon))
            shutil.copy(os.path.join(new_icons_dir, icon), os.path.join(icons_dir, icon))

    print("✅ Updated icons: Copied all SVG icons to /public/icons & frontend/public/icons.")



# Function to update localization & implement RTL support
def update_localization():
    # Ensure the translations directory exists
    os.makedirs(translations_dir, exist_ok=True)

    # Copy all translation files (.json) into `.chainlit/translations`
    for translation_file in os.listdir(new_translations_dir):
        if translation_file.endswith('.json'):
            source_path = os.path.join(new_translations_dir, translation_file)
            dest_path = os.path.join(translations_dir, translation_file)
            shutil.copy(source_path, dest_path)

    print("✅ Copied localization files to .chainlit/translations.")

    # Ensure the i18n directory exists
    i18n_dir = os.path.join(BASE_DIR, 'frontend/src/components/i18n')
    os.makedirs(i18n_dir, exist_ok=True)

    # Path to langToggle.tsx in rebranding_assets
    lang_toggle_source = os.path.join(BASE_DIR, 'rebranding_assets/langToggle.tsx')
    lang_toggle_dest = os.path.join(i18n_dir, 'langToggle.tsx')

    # Copy langToggle.tsx if it exists in rebranding_assets
    if os.path.exists(lang_toggle_source):
        shutil.copy(lang_toggle_source, lang_toggle_dest)
        print("✅ Copied langToggle.tsx from rebranding_assets to frontend/src/components/i18n.")
    else:
        print("⚠️ langToggle.tsx not found in rebranding_assets. Skipping copy.")




    # ✅ Modify `header/index.tsx` to add LanguageToggle before ThemeToggle
    if os.path.exists(header_index_tsx):
        with open(header_index_tsx, 'r') as f:
            header_content = f.read()

        # Step 1️⃣: Add `<LanguageToggle className='border'/><Separator orientation="vertical" />` before `<ThemeToggle />`
        if "<ThemeToggle />" in header_content and "LanguageToggle" not in header_content:
            header_content = re.sub(
                r'(<ThemeToggle\s*/?>)',
                "<LanguageToggle className='border'/> <Separator orientation='vertical' />\n    \\1",
                header_content
            )

        # Step 2️⃣: Ensure the imports for `LanguageToggle` and `Separator` exist
        if "import { LanguageToggle }" not in header_content:
            header_content = re.sub(
                r'(import .*?;)',  # Insert after the last import statement
                r"\1\nimport { LanguageToggle } from '../i18n/langToggle';\nimport { Separator } from '../ui/separator';",
                header_content,
                count=1
            )

        # Save changes to header/index.tsx
        with open(header_index_tsx, 'w') as f:
            f.write(header_content)

        print("✅ Added LanguageToggle and Separator to header/index.tsx.")



    # Here we can add styles/classes updates
    """
    # Modify DialogPrimitive.Close in dialog.tsx
    with open(dialog_tsx, 'r') as f:
        dialog_content = f.read()
    if 'rtl:left-4' not in dialog_content:
        dialog_content = dialog_content.replace(
            'className="absolute right-4',
            'className="absolute ltr:right-4 rtl:left-4'
        )
    with open(dialog_tsx, 'w') as f:
        f.write(dialog_content)


    print("✅ RTL support adjustments applied.")
    """


# Update custom_build in config.toml // after build
def update_custom_build():
    build_src = os.path.join(BASE_DIR, 'frontend/dist')

    if os.path.exists(build_src):
        if os.path.exists(config_toml_path):
            with open(config_toml_path, 'r') as f:
                config_data = f.read()

            # Ensure the [UI] section exists
            if "[UI]" not in config_data:
                config_data += "\n[UI]\n"

            # Update or insert custom_build and custom_js
            config_data = re.sub(r'# custom_build\s*=\s*".*?"', 'custom_build = "frontend/dist"', config_data)

            # If keys didn't exist, add them
            if '# custom_build =' not in config_data:
                config_data += '\ncustom_styles = "frontend/dist"\n'

            # Save back the updated config file
            with open(config_toml_path, 'w') as f:
                f.write(config_data)

            print("✅ Updated config.toml: Injected/Updated custom_build = frontend/dist.")

















# Run all functions
def run_all():
    # run_pnpm_commands() #❌
    run_chainlit_commands()


    pre_tasks()       #✅
    replace_text_safely("https://github.com/Chainlit/chainlit", "https://arabot.io/")
    update_header()
    update_colors()   #✅
    replace_logos()   #✅
    replace_favicon() #✅
    update_footer()   #✅
    inject_themeing() #✅
    update_icons()    #✅
    update_localization() #✅
    # update_custom_build()
    print("All Arabot branding updates applied successfully! 🚀")

if __name__ == '__main__':
    run_all()





""" Testing Notes
- maybe we have to add public files to /frontend/public also
- .husky there is something blocks pull/push

"""
