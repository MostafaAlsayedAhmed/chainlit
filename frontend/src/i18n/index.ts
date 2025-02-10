import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';  
import enTranslations from '@/locales/en.json'; 
import arTranslations from '@/locales/ar.json';

const i18nConfig = { 
  defaultNS: 'translation',
  resources: {
    en: { translations: enTranslations },
    ar: { translations: arTranslations }
  },
  lng: localStorage.getItem('lang') || 'en',
  fallbackLng: 'en',
  interpolation: { escapeValue: false }
};

export function i18nSetupLocalization(): void {
  i18n
    .use(initReactI18next)
    .init(i18nConfig)
    .catch((err) => console.error('[i18n] Failed to setup localization.', err));
}


 
  