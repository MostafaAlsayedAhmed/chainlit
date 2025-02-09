import getRouterBasename from '@/lib/router';
import App from 'App';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import {
  useApi,
  useAuth,
  useChatInteract,
  useConfig
} from '@chainlit/react-client';

// Import local translations
import enTranslations from '../public/locales/en.json';
import arTranslations from '../public/locales/ar.json';

export default function AppWrapper() {
  const [translationLoaded, setTranslationLoaded] = useState(false);
  const { isAuthenticated, isReady } = useAuth();
  const { windowMessage } = useChatInteract();
  // const { language: languageInUse } = useConfig();
  const { i18n } = useTranslation();

  /*
  function handleChangeLanguage(languageBundle: any): void {
    i18n.addResourceBundle(languageInUse, 'translation', languageBundle);
    i18n.changeLanguage(languageInUse);
  }

  const { data: translations } = useApi<any>(
    `/project/translations?language=${languageInUse}`
  );

  useEffect(() => {
    if (!translations) return;
    handleChangeLanguage(translations.translation);
    setTranslationLoaded(true);
  }, [translations]);
  */

  useEffect(() => {
    const savedLanguage = localStorage.getItem('lang') || 'en';
    i18n.changeLanguage(savedLanguage);

    // Add translation resources manually
    i18n.addResourceBundle('en', 'translation', enTranslations, true, true);
    i18n.addResourceBundle('ar', 'translation', arTranslations, true, true);
    
    document.documentElement.dir = savedLanguage === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = savedLanguage;
    
    setTranslationLoaded(true);
  }, [i18n]);
  
  useEffect(() => {
    const handleWindowMessage = (event: MessageEvent) => {
      windowMessage(event.data);
    };
    window.addEventListener('message', handleWindowMessage);
    return () => window.removeEventListener('message', handleWindowMessage);
  }, [windowMessage]);

  if (!translationLoaded) return null;

  if (
    isReady &&
    !isAuthenticated &&
    window.location.pathname !== getRouterBasename() + '/login' &&
    window.location.pathname !== getRouterBasename() + '/login/callback'
  ) {
    window.location.href = getRouterBasename() + '/login';
  }
  return <App />;
}
