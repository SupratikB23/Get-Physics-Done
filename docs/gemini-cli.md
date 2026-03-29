# Gemini CLI Quickstart

Gemini CLI is the terminal app where GPD runs for Gemini users. In this setup, you open `gemini`, then use GPD commands inside that session.

This guide uses the simplest path to get started. Google's official Gemini CLI docs may list additional install, auth, or platform-specific options.

## Before you start

Open your normal terminal in the folder where you want this research project to live.
This guide uses `--local`, so GPD is installed only for the current folder.

## 1) Check that `gemini` works

Run this in your normal terminal:

```bash
gemini --help
```

If that prints help text, Gemini CLI is installed and launchable.
If `gemini` is missing, install the runtime first with:

```bash
npm install -g @google/gemini-cli
```

## 2) Install GPD for Gemini CLI

```bash
npx -y get-physics-done --gemini --local
```

## 3) Start Gemini CLI

From the same project folder:

```bash
gemini
```

If you are not signed in yet, choose **Sign in with Google** and finish the browser login flow.

## 4) First commands inside Gemini CLI

Type these inside Gemini CLI, not in your normal terminal:

```text
/gpd:help
/gpd:start
/gpd:tour
/gpd:new-project --minimal
/gpd:map-research
/gpd:resume-work
```

If you are not sure what this folder is yet, start with `/gpd:start`.
If you want a read-only walkthrough first, use `/gpd:tour`.

Suggested order for beginners: `/gpd:help`, `/gpd:start`, `/gpd:tour`, then either `/gpd:new-project --minimal`, `/gpd:map-research`, or `/gpd:resume-work`.

## 5) What success looks like

- `gemini --help` works.
- `npx -y get-physics-done --gemini --local` finishes without errors.
- `/gpd:help` shows GPD commands.
- `/gpd:start` routes a beginner to the right entry point.
- `/gpd:tour` gives a read-only walkthrough of the main commands.
- `/gpd:new-project --minimal`, `/gpd:map-research`, or `/gpd:resume-work` starts the right GPD flow for new work, existing research, or an existing GPD project.

## 6) Quick troubleshooting

- `gemini: command not found`: install Gemini CLI, then reopen your terminal.
- GPD commands are missing: rerun `npx -y get-physics-done --gemini --local`.
- Not signed in: start `gemini`, choose `Sign in with Google`, and finish the browser login prompt. If you prefer API-key auth, Gemini CLI's official auth guide covers `GEMINI_API_KEY`.

## Official docs

- Google: [Gemini CLI repository and installation](https://github.com/google-gemini/gemini-cli)
- Google: [Gemini CLI authentication guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/authentication.md)
