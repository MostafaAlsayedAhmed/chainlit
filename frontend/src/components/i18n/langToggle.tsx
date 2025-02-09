import { useState, useEffect } from 'react';
import { cn } from '@/lib/utils';
import { Languages } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';

import { useTranslation } from 'react-i18next';
interface Props {
  className?: string;
}


export function LanguageToggle({ className }: Props) {
  const { i18n } = useTranslation();
  const savedLanguage = localStorage.getItem('lang') || 'en';

  useEffect(() => {
    i18n.changeLanguage(savedLanguage);
    document.documentElement.dir = savedLanguage === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = savedLanguage;
  }, [i18n]);

  const handleLanguageChange = (newLang: 'en' | 'ar') => {
    i18n.changeLanguage(newLang);
    localStorage.setItem('lang', newLang);
    document.documentElement.dir = newLang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = newLang;
    window.location.reload(); // Refresh to apply changes globally
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className={cn(
            'text-muted-foreground hover:text-muted-foreground',
            className
          )}
        >
          <Languages className="!size-5 rotate-0 scale-100 transition-all" />
          <span className="sr-only">Toggle Language</span>
          {/* savedLanguage    {savedLanguage} */}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => handleLanguageChange('ar')} className={savedLanguage == 'ar' ? 'active' : ''}>
          العربية (Arabic)
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => handleLanguageChange('en')} className={savedLanguage == 'en' ? 'active' : ''}>
          English
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
