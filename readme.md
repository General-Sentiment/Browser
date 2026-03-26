# General Browser

An ultralight minimal browser with (basically) no interface. Pages fill the entire window. All controls live behind a single Cmd+K overlay: address bar, tabs, history.

Deeply inspired by [Oryoki](https://github.com/thmsbfft/oryoki), which proved that a browser could be reduced to almost nothing and still be everything you need.

**macOS only for now.**

## Philosophy

The entire source ships inside the app. There is no build step, no bundler, no transpiler. The code you see is the code that runs. You can open the source files and edit them directly.

Site rules let you inject your own CSS and JS into any page. Instead of reaching for a separate ad blocker or extension, you intervene directly: hide what you don't want, restyle what you do, add behavior where it's missing. The browser is just a thin shell around your preferences.

When the app updates, your modifications don't get overwritten. An LLM-assisted merge reconciles upstream changes with whatever you've done to the source. The codebase evolves like a living thing. Upstream improvements graft onto your local mutations, and the result is software that is partly the thing that was shipped and partly the thing you made it into.

## Usage

```
npm install
npm start
```

Cmd+K (or Cmd+L) opens the overlay. Type a URL or search query, press Enter. Escape closes it. That's the whole interface.

## Shortcuts

| Key           | Action         |
| ------------- | -------------- |
| Cmd+K / Cmd+L | Toggle overlay |
| Cmd+T         | New tab        |
| Cmd+W         | Close tab      |
| Cmd+N         | New window     |
| Cmd+Shift+[   | Previous tab   |
| Cmd+Shift+]   | Next tab       |
| Escape        | Close overlay  |

## Settings

All configuration lives in `~/.browser/settings.yml`, created on first run.

## Site Rules

Inject custom CSS and JS into any site. Rules are defined in `~/.browser/sites.yaml` and the actual CSS/JS files live in `~/.browser/sites/`.

The app ships with default rules for YouTube and Instagram. Toggle them on or off from the gear icon in the overlay.

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

File paths are relative to `~/.browser/`. Glob patterns for URL matching: `*` matches anything.

## Ejecting

Click the gear icon in the overlay and choose "Eject" to copy the browser's source files to a directory you control. This copies both the overlay UI and the default site rules. The app loads your copies instead of the built-in ones. Edit freely.

When the app updates and the built-in files change, the settings view shows which files diverged. Run `/update-ui` in Claude Code to merge upstream changes around your customizations.

## Structure

```
main.js          Electron main process
preload.js       IPC bridge
ui/
  index.html     Shell
  app.js         Preact overlay app
  settings.js    Settings view
  style.css      Styles (light/dark, oklch)
  lib/           Vendored preact + htm + hooks
sites/           Default site rules (youtube, instagram)
```
