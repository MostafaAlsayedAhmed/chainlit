# https://chatgpt.com/share/67adfd9d-0dec-800f-b35e-9b47d472096b

"""
I want to automate rebranding (change logos, colors, some texts) for a repo from github that I copied it to my bitbucket, chainlit => Mostafa-chainlit,
I made some updates, and when there is a new release in the main repo, I want that update with my branding.
here are some tasks what I want to do them programmatically, not manually :
"""


""" ✅
# Colors:
 = To update the build project => /public/theme.json
 = To update the frontend      => frontend/src/index.css


# Logo: (Note: public folder out of the frontend folder)
 = /public/logo_dark.png
 = /public/logo_light.png
 = /public/favicon.png


# Footer: Change Icons
 = frontend/src/assets/logo_light.svg
 = frontend/src/assets/logo_dark.svg
 = frontend\src\components\WaterMark.tsx (change the link https://github.com/Chainlit/chainlit to https://arabot.io/)


# Themeing - Custom Styles & Scripts:
  You can inject them into the application by adding the file (in public folder) [or via an external link for css] to the config.toml under [UI] configrations


# Icons: (for starters messages) frontend\public\**.svg



# RTL support:
## Add Localization - changeLanguage(): changes in 4 files
 - Adding ar.json and other languages files to ".chainlit/translations" (.chainlit is beside frontend & backend folders).
 - Add NEW dropdown component: frontend/src/components/i18n/langToggle.tsx

 - _mixins file & _custom_stylesheets
 - Add    <LanguageToggle className='border'/>    in frontend/src/components/header/index.tsx
 -  DialogPrimitive.Close className="absolute ltr:right-4 rtl:left-4 ....." in  frontend/src/components/ui/dialog.tsx (NewChat ❌ button)
 -
"""
# what is the content of the rebranding_assets folder? = >>
"""
/rebranding_assets
│── custom.css                   (Merged RTL styles + Custom styles)
│── custom.js                    (Custom scripts for UI enhancements)
│── langToggle.tsx               (Language switcher component)
│── 📂translations/
│   ├── ar.json
│   ├── en.json
│   └── more_languages.json
│── logo_dark.png                (Brand-specific dark logo)
│── logo_light.png               (Brand-specific light logo)
│── favicon.png                  (Brand-specific favicon)
│── theme.json                   (Branding color overrides)
│── 📂icons/                     (Folder for custom SVG icons)
│   ├── icon1.svg                (Custom icon example)
│   ├── icon2.svg                (More icons as needed)
│   └── ...                      (All branding-related icons)

"""
