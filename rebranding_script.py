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


# Icons: frontend\public\**.svg


# Localization:
 - Adding ar.json and other languages files to ".chainlit/translations" (.chainlit is beside frontend & backend folders).
 - Add NEW dropdown component: frontend/src/components/i18n/langToggle.tsx
 - some pages require classes!

# RTL support:
##  Add
## Localization - changeLanguage(): changes in 4 files
## Localization - mixins file & custom stylesheets
 -
 -
"""
# https://chatgpt.com/share/67adfd9d-0dec-800f-b35e-9b47d472096b

"""
I want to automate rebranding (change logos, colors, some texts) for a repo from github that I copied it to my bitbucket, chainlit => Mostafa-chainlit, I made some updates, and when there is a new release in the main repo, I want that update with my branding.
here are some tasks what I want to do them programmatically, not manually :
"""
