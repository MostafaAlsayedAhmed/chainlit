
""" updates/notes
inject_themeing() we can add variables
".chainlit" will add to the project after "pnpm run preinstall" & "pnpm run install" & "pnpm run dev"
"""

import json
import os
import shutil
import re
import subprocess



# Define paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Paths for colors
theme_json_path = os.path.join(BASE_DIR, 'public/theme.json')
css_file_path = os.path.join(BASE_DIR, 'frontend/src/index.css')

# Paths for logos
public_dir = os.path.join(BASE_DIR, 'public')
logo_dark = os.path.join(BASE_DIR, 'rebranding_assets/logo_dark.png')
logo_light = os.path.join(BASE_DIR, 'rebranding_assets/logo_light.png')
favicon = os.path.join(BASE_DIR, 'rebranding_assets/favicon.png')

# Paths for footer updates
logo_light_svg = os.path.join(BASE_DIR, 'frontend/src/assets/logo_light.svg')
logo_dark_svg  = os.path.join(BASE_DIR, 'frontend/src/assets/logo_dark.svg')
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
        print("🚀 Running preinstall...")
        subprocess.run(["pnpm", "run", "preinstall"], check=True)

        print("🚀 Running install...")
        subprocess.run(["pnpm", "install"], check=True)

        print("🚀 Starting dev server...")
        subprocess.run(["pnpm", "run", "dev"], check=True)

        print("✅ PNPM commands executed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running PNPM command: {e}")


# Function to update colors
def update_colors():
    # Update `theme.json`
    if os.path.exists(theme_json_path):
        with open(theme_json_path, 'r') as f:
            theme_data = json.load(f)

        # Only update the specific colors in theme.json
        theme_updates = {
            "--primary": "200 70% 50%",
            "--secondary": "220 50% 90%",
            "--accent": "200 60% 40%",
            "--destructive": "0 85% 55%"
        }

        theme_data.update(theme_updates)

        with open(theme_json_path, 'w') as f:
            json.dump(theme_data, f, indent=4)

        print("✅ Updated theme.json with new colors.")

    # Update `index.css`
    if os.path.exists(css_file_path):
        with open(css_file_path, 'r') as f:
            css_data = f.read()

        # Define CSS replacements using regex (since CSS uses space-separated HSL values)
        css_replacements = {
            "--primary": "200 70% 50%",
            "--secondary": "220 50% 90%",
            "--accent": "200 60% 40%",
            "--destructive": "0 85% 55%"
        }

        for key, new_value in css_replacements.items():
            # Use regex to find `--primary: 271 52% 45%;` and replace the value
            css_data = re.sub(rf"({key}: )[\d.]+ [\d.]+% [\d.]+%;", rf"\1{new_value};", css_data)

        with open(css_file_path, 'w') as f:
            f.write(css_data)

        print("✅ Updated index.css with new colors.")


# Function to replace logos
def replace_logos():
    #  copy(new, old) means copy from [rebranding_assets] to [main_dir]
    shutil.copy(logo_dark, os.path.join(public_dir, 'logo_dark.png'))
    shutil.copy(logo_light, os.path.join(public_dir, 'logo_light.png'))
    shutil.copy(favicon, os.path.join(public_dir, 'favicon.png'))
    print("Replaced logos.")

# Function to update footer
def update_footer():
    shutil.copy(logo_light_svg, os.path.join(BASE_DIR, 'frontend/src/assets/logo_light.svg'))
    shutil.copy(logo_dark_svg, os.path.join(BASE_DIR, 'frontend/src/assets/logo_dark.svg'))

    with open(watermark_tsx, 'r') as f:
        content = f.read()
    content = content.replace('https://github.com/Chainlit/chainlit', 'https://arabot.io/')
    with open(watermark_tsx, 'w') as f:
        f.write(content)
    print("Updated footer and watermark.")

# Function to inject styles and scripts into config.toml
def inject_themeing():
    # Paths to theme assets
    custom_js_source = os.path.join(BASE_DIR, 'rebranding_assets/custom.js')
    custom_css_source = os.path.join(BASE_DIR, 'rebranding_assets/custom.css')

    custom_js_dest = os.path.join(BASE_DIR, 'public/custom.js')
    custom_css_dest = os.path.join(BASE_DIR, 'public/custom.css')

    # Copy custom.js and custom.css to the public folder
    if os.path.exists(custom_js_source):
        shutil.copy(custom_js_source, custom_js_dest)
    if os.path.exists(custom_css_source):
        shutil.copy(custom_css_source, custom_css_dest)
    print("✅ Copied custom.js & custom.css to public folder.")

    # Update config.toml
    if os.path.exists(config_toml_path):
        with open(config_toml_path, 'r') as f:
            config_data = f.read()

        # Ensure the [UI] section exists
        if "[UI]" not in config_data:
            config_data += "\n[UI]\n"

        # Update or insert custom_css and custom_js
        config_data = re.sub(r'# custom_css\s*=\s*".*?"', 'custom_css = "public/custom.css"', config_data)
        config_data = re.sub(r'# custom_js\s*=\s*".*?"', 'custom_js = "public/custom.js"', config_data)

        # If keys didn't exist, add them
        if '# custom_css =' not in config_data:
            config_data += '\ncustom_styles = "public/custom.css"\n'
        if '# custom_js =' not in config_data:
            config_data += 'custom_js = "public/custom.js"\n'

        # Save back the updated config file
        with open(config_toml_path, 'w') as f:
            f.write(config_data)

        print("✅ Updated config.toml: Injected/Updated custom.js and custom.css.")


# Function to update icons
""" If there are any messages (starters) requires icons """
def update_icons():
    icons_dir = os.path.join(BASE_DIR, 'frontend/public/icons')
    new_icons_dir = os.path.join(BASE_DIR, 'rebranding_assets/icons')

    for icon in os.listdir(new_icons_dir):
        if icon.endswith('.svg'):
            shutil.copy(os.path.join(new_icons_dir, icon), os.path.join(icons_dir, icon))
    print("Updated icons.")


# Function to update localization
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
                "<LanguageToggle className='border'/><Separator orientation='vertical' />\n    \\1",
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

    print("✅ RTL support adjustments applied.")


# Function to implement RTL support
def enable_rtl():
    # Modify DialogPrimitive.Close in dialog.tsx ✅
    with open(dialog_tsx, 'r') as f:
        dialog_content = f.read()
    if 'rtl:left-4' not in dialog_content:
        dialog_content = dialog_content.replace(
            'className="absolute right-4',
            'className="absolute ltr:right-4 rtl:left-4'
        )
    with open(dialog_tsx, 'w') as f:
        f.write(dialog_content)

    print("RTL support enabled.")






    # # Modify _mixins.scss
    # with open(mixins_scss, 'r') as f:
    #     mixins_content = f.read()
    # if 'direction' not in mixins_content:
    #     mixins_content += '\nbody { direction: rtl; }'
    # with open(mixins_scss, 'w') as f:
    #     f.write(mixins_content)

    # # Modify _custom_stylesheets.scss
    # with open(custom_styles_scss, 'r') as f:
    #     custom_styles_content = f.read()
    # if 'text-align: right' not in custom_styles_content:
    #     custom_styles_content += '\nbody { text-align: right; }'
    # with open(custom_styles_scss, 'w') as f:
    #     f.write(custom_styles_content)

    """
    Still this part needs to be updated -
    I made them in just one css file "/public/custom_style.css" to be injected in config.toml,
    it's working well at the backend project, but not working in the frontend.
    I will use the /public/custom_style.css also in the frontend .main.tsx file.
    then add it too inject_themeing() function.
    """











# Run all functions
def run_all():
    run_pnpm_commands() # Run this function at the appropriate step in your script

    update_colors()
    replace_logos()
    update_footer()
    inject_themeing()
    update_icons()
    update_localization()
    enable_rtl()
    print("All branding updates applied successfully!")

if __name__ == '__main__':
    run_all()

