---
name: premium-ui-design
description: Guidelines and patterns for implementing world-class UI design, micro-interactions, magnetic button effects, shimmer skeletons, and spring animations.
---

# Premium UI Design & Micro-Interactions Skill

This skill provides best practices for crafting production-grade, premium web application interfaces with fluid animations, magnetic micro-interactions, sleek dark mode surfaces, and responsive visual feedback.

## Design Principles

### 1. Visual Hierarchy & Surface Depth
- Use dark slate surfaces (`#09090b` canvas, `#0d0d11` sidebar, `#16161b` cards).
- Use subtle high-contrast borders (`1px solid rgba(255, 255, 255, 0.08)`).
- Layer depth with precise elevation shadows rather than harsh drop-shadows:
  `box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05)`

### 2. Premium Button Visual Effects
- **Hover Sheen**: A subtle light reflection sliding across the button on hover.
- **Active Press State**: Tactile feel using `transform: scale(0.98)` on click.
- **Glowing Accent Focus**: Smooth focus ring with soft glow opacity transitions.

### 3. Skeleton Loading States
- Always use smooth animated shimmering gradients for loading states instead of plain text loaders:
  `background: linear-gradient(90deg, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.03) 75%)`

### 4. Fluid Motion & Micro-Animations
- Use spring-like cubic-bezier transitions for UI elements (`cubic-bezier(0.16, 1, 0.3, 1)`).
- Animate panel tab switches with a simultaneous opacity fade and 8px vertical translate.
