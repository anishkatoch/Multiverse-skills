# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Repository structure

This repo holds Claude Code skills, each in its own top-level folder:

- `Apexforge/` - frontend UI builder skill
- `TurboDeck/` - PowerPoint deck builder skill

Each skill folder typically contains the skill itself (`SKILL.md` plus
supporting files), a `-workspace` folder with eval iterations, and an
`-INSTALL.md` file.

## Hard rules

- Never use an em dash (—) anywhere in this repo: code, comments, commit
  messages, docs, or any generated content. Use a comma, a period, or
  rewrite the sentence instead.
- Never list Claude, Claude Code, or any AI assistant as a contributor or
  author in this repo. This means:
  - No `Co-Authored-By: Claude ...` lines in commit messages.
  - No "Generated with Claude Code" lines in commit messages or PR
    descriptions.
  - No AI attribution in file headers, changelogs, or docs.
  - All commits and PRs should attribute authorship to the human
    maintainer only: name/email `katochaneesh@gmail.com`, username
    `anishkatoch`.
