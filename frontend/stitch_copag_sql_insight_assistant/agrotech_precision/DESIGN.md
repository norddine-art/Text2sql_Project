---
name: AgroTech Precision
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#3f4945'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#707975'
  outline-variant: '#bfc9c4'
  surface-tint: '#29695b'
  primary: '#00342b'
  on-primary: '#ffffff'
  primary-container: '#004d40'
  on-primary-container: '#7ebdac'
  inverse-primary: '#94d3c1'
  secondary: '#785900'
  on-secondary: '#ffffff'
  secondary-container: '#fdc003'
  on-secondary-container: '#6c5000'
  tertiary: '#232f35'
  on-tertiary: '#ffffff'
  tertiary-container: '#39454b'
  on-tertiary-container: '#a5b2ba'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#afefdd'
  primary-fixed-dim: '#94d3c1'
  on-primary-fixed: '#00201a'
  on-primary-fixed-variant: '#065043'
  secondary-fixed: '#ffdf9e'
  secondary-fixed-dim: '#fabd00'
  on-secondary-fixed: '#261a00'
  on-secondary-fixed-variant: '#5b4300'
  tertiary-fixed: '#d7e4ec'
  tertiary-fixed-dim: '#bbc8d0'
  on-tertiary-fixed: '#111d23'
  on-tertiary-fixed-variant: '#3c494f'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  headline-xl:
    fontFamily: Geist
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
  data-mono:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style
This design system establishes a high-trust, corporate identity that bridges the gap between traditional agriculture and cutting-edge data science. The brand personality is authoritative yet transparent, designed to evoke feelings of stability, growth, and technological foresight.

The visual style is a refined **Modern Glassmorphism**. It utilizes semi-transparent surfaces to imply depth and technical sophistication without sacrificing the clarity required for complex agricultural data. A "TL;DR First" information hierarchy prioritizes executive summaries and high-level KPIs at the top of every view, ensuring that critical insights are immediate, with granular data available through progressive disclosure.

## Colors
The palette is rooted in **Deep Forest Green (#004D40)**, representing the heritage of agriculture and the reliability of a corporate entity. This is balanced by a dominant use of **Crisp White** and **Slate Gray (#F8FAFC)** to ensure a clean, tech-focused environment that minimizes cognitive load.

**Subtle Gold/Amber (#FFC107)** is reserved exclusively for premium data highlights, trend alerts, and high-value insights. This "harvest" accent color should be used sparingly—only when user attention is required for critical yield data or financial fluctuations. Backgrounds utilize high-transparency whites to create the glass effect, while borders use a faint tint of the primary green to maintain brand cohesion even in structural elements.

## Typography
The system employs a dual-font strategy. **Geist** is used for headlines, labels, and data points to provide a technical, precise, and modern feel. Its monospaced-influenced tracking makes it ideal for the tabular data frequent in agricultural reporting. **Inter** is used for all body copy and long-form descriptions to ensure maximum readability and a professional, approachable tone.

Information hierarchy follows a strict top-down approach. The "TL;DR" sections should use `headline-lg` for key metrics and `body-lg` for brief summaries. All numerical data in charts or tables should utilize the `data-mono` style for alignment and clarity.

## Layout & Spacing
This design system utilizes a **Fixed Grid** model for desktop to maintain corporate structure, transitioning to a **Fluid Grid** for mobile devices. The layout is based on a 12-column grid with generous 24px gutters to allow the UI to "breathe," reflecting the openness of the agricultural landscape.

- **Desktop:** 12-column grid, centered, 1280px max width.
- **Tablet:** 8-column grid, 24px margins.
- **Mobile:** 4-column grid, 16px margins.

Spacing follows a strict 4px baseline rhythm. "TL;DR First" components are always placed in the top-most container, spanning the full width of the grid to ensure immediate visibility upon page load.

## Elevation & Depth
Depth is communicated through **Glassmorphic layering** rather than traditional heavy shadows. Surfaces use a `backdrop-filter: blur(12px)` combined with a semi-transparent white fill. 

A "stacked" hierarchy is achieved through:
1.  **Level 0 (Canvas):** Crisp White (#FFFFFF) or Light Gray (#F8FAFC).
2.  **Level 1 (Cards/Sections):** Glass surface with a 1px border of `rgba(0, 77, 64, 0.08)`.
3.  **Level 2 (Active/Hover):** A soft, diffused ambient shadow (`0 8px 30px rgba(0, 0, 0, 0.04)`) to indicate interactivity.

This creates a "light-through-glass" effect that feels clean and high-tech, avoiding the "muddy" look of traditional skeuomorphism.

## Shapes
The shape language is **Rounded**, striking a balance between the organic nature of agriculture and the precision of technology. 

- **Standard Elements (Buttons, Inputs):** 0.5rem (8px) radius.
- **Large Elements (Cards, Modals):** 1rem (16px) radius.
- **Data Tags/Chips:** 1.5rem (24px) for a pill-shaped appearance.

Borders are kept extremely thin (1px) to maintain the delicate glass aesthetic, always using the primary green at a low opacity to define edges without closing off the layout.

## Components
- **Buttons:** Primary buttons use a solid Deep Forest Green with white text. Secondary buttons use a transparent background with a 1px green border. High-priority "Premium" actions may use an Amber text or small Amber icon accent.
- **TL;DR Cards:** Featured at the top of pages. These use a slightly thicker glass blur and contain a single prominent metric (Geist Headline) and a one-sentence summary.
- **Input Fields:** Minimalist design with a 1px bottom border that transforms into a full 1px enclosure on focus. Labels use the `label-caps` style for a professional, form-like feel.
- **Data Tables:** Highly structured using Geist. Row hover states should use a subtle tint of the primary color (`rgba(0, 77, 64, 0.02)`).
- **Progressive Disclosure:** Use "Chevron-down" icons to hide granular technical data under "TL;DR" summaries, keeping the initial view clean and executive-friendly.
- **Chips:** Used for categorizing crop types or data status. These are pill-shaped and use low-saturation background tints to prevent visual noise.