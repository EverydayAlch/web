// ============================================
//   EVERYDAY ALCHEMY / SANCTUM — DESIGN TOKENS
//   ============================================
//   Single source of truth for Expo / React Native.
//   Import anywhere: import { colors, fonts, spacing } from './tokens'
//   ============================================

// --- COLORS ---

export const colors = {

  // Backgrounds
  obsidian:  '#0a0908',   // primary app background
  deep:      '#111009',   // screen backgrounds
  charcoal:  '#1a1814',   // card backgrounds
  ash:       '#2a2822',   // hover states, subtle fills

  // Gold — primary accent
  gold:      '#c9a96e',   // primary accent, active nodes, CTAs
  goldLight: '#e2c98a',   // emphasis, apex elements, highlights
  goldDim:   '#8a6e3e',   // muted labels, secondary markers

  // Text
  cream:     '#f0e8d8',   // primary text
  creamMid:  'rgba(240, 232, 216, 0.65)',  // body text
  creamLow:  'rgba(240, 232, 216, 0.35)',  // placeholder, disabled

  // Utility
  fog:       'rgba(240, 232, 216, 0.06)',
  fogMid:    'rgba(240, 232, 216, 0.12)',
  goldBorder:'rgba(201, 169, 110, 0.2)',
  goldGlow:  'rgba(201, 169, 110, 0.07)',

  // Skill Tree
  nodeLocked:         'rgba(42, 40, 34, 0.8)',
  nodeUnlocked:       'rgba(201, 169, 110, 0.15)',
  nodeComplete:       '#c9a96e',
  nodeActive:         '#e2c98a',
  nodeBorderLocked:   'rgba(201, 169, 110, 0.2)',
  nodeBorderUnlocked: 'rgba(201, 169, 110, 0.6)',
  constellationLine:  'rgba(201, 169, 110, 0.25)',

  // Transparent overlays
  overlay: {
    light: 'rgba(10, 9, 8, 0.6)',
    mid:   'rgba(10, 9, 8, 0.8)',
    heavy: 'rgba(10, 9, 8, 0.95)',
  },
};


// --- TYPOGRAPHY ---

export const fonts = {
  logo:    'Cinzel',       // logo only
  heading: 'Amulet',       // H1, H2, H3, screen titles
  body:    'TheSeasons',   // body text, descriptions, Seshat
  ui:      'Jost',         // labels, nav, eyebrows, utility text
};

export const fontSizes = {
  xs:   10,
  sm:   12,
  base: 15,
  md:   18,
  lg:   22,
  xl:   28,
  '2xl': 36,
  '3xl': 48,
  hero:  64,
};

export const fontWeights = {
  light:    '300',
  regular:  '400',
  medium:   '500',
  semibold: '600',
};

export const letterSpacing = {
  tight:   -0.5,
  normal:   0.3,
  wide:     2,
  wider:    4,
  widest:   6,
};

export const lineHeights = {
  tight:  1.1,
  snug:   1.4,
  normal: 1.7,
  loose:  1.9,
};


// --- SPACING ---

export const spacing = {
  xs:  8,
  sm:  16,
  md:  24,
  lg:  40,
  xl:  60,
  '2xl': 80,
  '3xl': 120,
};


// --- BORDER RADIUS ---

export const radius = {
  sm:   4,
  md:   8,
  lg:   16,
  full: 9999,
};


// --- SHADOWS ---

export const shadows = {
  goldSm: {
    shadowColor: '#c9a96e',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 4,
  },
  goldMd: {
    shadowColor: '#c9a96e',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.2,
    shadowRadius: 30,
    elevation: 8,
  },
  goldLg: {
    shadowColor: '#c9a96e',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.25,
    shadowRadius: 60,
    elevation: 16,
  },
};


// --- ANIMATION DURATIONS (ms) ---

export const duration = {
  fast:   200,
  base:   300,
  slow:   500,
  reveal: 800,
};


// --- FONT LOADING (for useFonts in Expo) ---
//
// Add to your root layout:
//
// const [fontsLoaded] = useFonts({
//   'Amulet':     require('./assets/fonts/Amulet.ttf'),
//   'TheSeasons': require('./assets/fonts/TheSeasons.ttf'),
//   'TheSeasons-Italic': require('./assets/fonts/TheSeasons-Italic.ttf'),
//   'Cinzel':     require('./assets/fonts/Cinzel.ttf'),
//   'Jost':       require('./assets/fonts/Jost.ttf'),
// });