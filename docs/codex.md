# Codex Quickstart for GPD

Use this if you are a physics researcher and want GPD inside the OpenAI Codex CLI.

This guide uses the simplest path to get started. OpenAI's official Codex docs may list additional install, auth, or platform-specific options.

## What Codex is here

In this project, “Codex” means the Codex CLI runtime that GPD installs into. Once GPD is set up, you run GPD commands inside Codex with the `$gpd-...` syntax.

If you are on Windows, the official Codex docs currently say Windows support is experimental and recommend using Codex in WSL for the best experience.

## Before you start

Open your normal terminal in the folder where you want this research project to live.
This guide uses `--local`, so GPD is installed only for the current folder.

## 1) Confirm `codex` works

From your normal terminal:

```bash
codex --help
```

If that prints help text, Codex is installed and launchable.
If `codex` is missing, install the runtime first with:

```bash
npm install -g @openai/codex
```

## 2) Install GPD for Codex

Copy-paste this exact command:

```bash
npx -y get-physics-done --codex --local
```

## 3) Start Codex

From the same project folder:

```bash
codex
```

The first time you run Codex, it should prompt you to sign in with your ChatGPT account or an API key.

## 4) First commands inside Codex

Type these inside Codex, not in your normal terminal:

```text
$gpd-help
$gpd-start
$gpd-tour
$gpd-new-project --minimal
$gpd-map-research
$gpd-resume-work
```

If you are not sure what this folder is yet, start with `$gpd-start`.
If you want a read-only walkthrough first, use `$gpd-tour`.

Suggested order for beginners: `$gpd-help`, `$gpd-start`, `$gpd-tour`, then either `$gpd-new-project --minimal`, `$gpd-map-research`, or `$gpd-resume-work`.

## 5) What success looks like

You are in the right place when:

- `codex --help` works.
- `npx -y get-physics-done --codex --local` finishes without errors.
- Inside Codex, `$gpd-help` shows the GPD command list.
- `$gpd-start` routes a beginner to the right entry point.
- `$gpd-tour` gives a read-only walkthrough of the main commands.
- `$gpd-new-project --minimal`, `$gpd-map-research`, or `$gpd-resume-work` starts the right GPD flow for new work, existing research, or an existing GPD project.

## 6) Quick troubleshooting

- If a command is missing, make sure you are typing it inside Codex, not in your normal terminal.
- If `codex` is not found, install or relaunch Codex first.
- If Codex says you are not signed in, finish the Codex login flow, then rerun `$gpd-help`.

## Official docs

- OpenAI: [Codex CLI docs](https://developers.openai.com/codex/cli)
- OpenAI: [Codex authentication](https://developers.openai.com/codex/auth)
