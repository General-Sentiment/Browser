# Browser

Lightweight Electron browser. Page fills the entire window. All UI is behind Cmd+K.

## Quick Start

```
npm install
npm start
```

## Structure

- `main.js` — Electron main process. Manages WebContentsViews (one per tab), IPC, settings, site rules, history.
- `preload.js` — contextBridge exposing `window.browser` API to the renderer.
- `ui/` — Overlay UI. No build step, plain ES modules.
  - `index.html` — Shell.
  - `app.js` — Preact app. Renders the Cmd+K overlay (address bar, tabs, history).
  - `settings.js` — Settings view (site rules, source directory, updates).
  - `style.css` — Styles (light/dark, oklch color space, CSS variables in :root).
  - `lib/` — Vendored Preact + htm + hooks. Do not npm install these.
- `sites/` — Default site rules shipped with the app.
  - `sites.yaml` — Rule definitions (name, enabled, matches, css, js).
  - `youtube/` — YouTube customizations (hide Shorts, redirect to subscriptions).
  - `instagram/` — Instagram customizations (hide suggestions, redirect to Following).
- `docs/plan.md` — Original design doc.

## Key Shortcuts

- `Cmd+K` / `Cmd+L` — Toggle overlay
- `Cmd+T` — New tab
- `Cmd+W` — Close tab
- `Cmd+N` — New window
- `Cmd+Shift+[` / `Cmd+Shift+]` — Switch tabs

## Settings

Config lives in `~/.browser/settings.yml` (created on first run).

## Site Rules

Site rules inject custom CSS and JS into pages by URL pattern. Configuration is in `sites/sites.yaml`:

```yaml
rules:
  - name: YouTube
    enabled: true
    matches:
      - "*://www.youtube.com/*"
    css:
      - sites/youtube/style.css
    js:
      - sites/youtube/script.js
```

- `matches` uses glob patterns: `*` matches any characters. Example: `*://www.youtube.com/*`
- `css` and `js` are arrays of file paths relative to the sites directory root.
- CSS is injected via `webContents.insertCSS()` after the page finishes loading.
- JS is injected via `webContents.executeJavaScript()` in the page's main world (full DOM access).
- Rules can be toggled on/off from the settings gear in the Cmd+K overlay.

### Working with site rules in Claude Code

When the user asks to customize a site (e.g. "hide the sidebar on twitter" or "make youtube cleaner"):

1. Read `sites/sites.yaml` to check if a rule already exists for that site.
2. If no rule exists, create a new directory under `sites/` (e.g. `sites/twitter/`) and add `style.css` and/or `script.js`.
3. Add a rule entry to `sites/sites.yaml` with the correct `matches` pattern and file paths.
4. If a rule already exists, edit the existing CSS/JS files.

Guidelines for site CSS/JS:
- Use `!important` on CSS rules to override site styles.
- For SPAs (YouTube, Instagram, Twitter), listen for navigation events since pages don't fully reload.
- JS runs in the main world with full access to the page's DOM and window object.
- Keep scripts minimal. Prefer CSS-only solutions when possible.

## Ejecting

Eject copies both `ui/` and `sites/` to a user-chosen directory. The app then loads from the ejected copy instead of the built-in files. This lets users (or Claude Code) edit the overlay UI and site rules freely.

Resolution chain: ejected directory -> built-in package (fallback).

After an app update, if built-in files changed, the settings view shows which files diverged. Run `/update-ui` in Claude Code to merge upstream changes.

## Conventions

- No build tools. UI is vanilla ES modules importing from `./lib/preact.js`.
- Use `html` tagged template literals (htm) instead of JSX.
- Keep it small.
