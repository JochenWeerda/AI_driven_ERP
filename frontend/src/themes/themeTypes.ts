// Typdefinitionen für das Theme-System
import { PaletteOptions, ThemeOptions } from '@mui/material/styles';

// Verfügbare Theme-Modi
export type ThemeMode = 'light' | 'dark' | 'high-contrast';

// Verfügbare Theme-Varianten (Farbschemata)
export type ThemeVariant = 'odoo' | 'default' | 'modern' | 'classic';

// Theme-Parameter für LLM-Anpassungen
export interface ThemeParameters {
  primaryColor?: string;
  secondaryColor?: string;
  fontSize?: 'small' | 'medium' | 'large';
  spacing?: 'compact' | 'normal' | 'comfortable';
  borderRadius?: 'none' | 'small' | 'medium' | 'large';
  fontFamily?: string;
  visualDensity?: 'low' | 'medium' | 'high';
}

// Theme-Konfigurationsobjekt
export interface ThemeConfig {
  mode: ThemeMode;
  variant: ThemeVariant;
  parameters?: ThemeParameters;
}

// Interface für Theme-Palette mit erweiterten Eigenschaften
export interface ExtendedPaletteOptions extends PaletteOptions {
  customBackground?: {
    header?: string;
    sidebar?: string;
    footer?: string;
    card?: string;
    hover?: string;
  };
  customText?: {
    primary?: string;
    secondary?: string;
    disabled?: string;
    hint?: string;
  };
}

// Erweiterte ThemeOptions mit zusätzlichen Eigenschaften
export interface ExtendedThemeOptions extends ThemeOptions {
  palette?: ExtendedPaletteOptions;
  visualDensity?: number;
}

// Interface für Theme-Anbieter, um Themes zu registrieren und abzurufen
export interface ThemeProviderInterface {
  getTheme: (config: ThemeConfig) => ExtendedThemeOptions;
  getCurrentThemeConfig: () => ThemeConfig;
  setThemeConfig: (config: ThemeConfig) => void;
} 