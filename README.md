# Cheat Sheets

> Lightweight data‑driven collection of technology cheat sheets (Git, VS Code, Python ecosystem, Docker, Linux distros, Markdown, Windows) built with Jekyll + Liquid using a single CSV as the command source and a YAML file for hierarchical navigation.

![Repo Size](https://img.shields.io/github/repo-size/ConradoAlmeida/cheatsheets?label=size)
![Last Commit](https://img.shields.io/github/last-commit/ConradoAlmeida/cheatsheets)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

![GitHub Logo](GitHub-Logo.png)

## Table of Contents

1. [Overview](#overview)
2. [Data Model](#data-model)
3. [Pages & Navigation](#pages--navigation)
4. [Adding Commands](#adding-commands)
5. [Adding a New Cheat Sheet](#adding-commands)
6. [CSV Validation Workflow](#csv-validation-workflow)
7. [Roadmap](#roadmap)
8. [Development](#development)
9. [Contributing](#contributing)
10. [License](#license)

## Overview

The site renders cheat sheets from a central CSV file (`_data/store-data.csv`) and a hierarchical navigation definition (`_data/lang-data.yml`). Each top‑level or child entry in the YAML maps to an HTML page (e.g. `git-cheat.html`, `pandas-cheat.html`). Pages reuse the same Liquid loop pattern: filter rows by the `grupo` column and group them by `categoria`.

## Data Model

`_data/store-data.csv` columns (must be exactly 4):

1. comandos  – the raw command / snippet
2. descricao – short English description
3. categoria – logical sub‑section displayed as a table group
4. grupo     – matches a cheat sheet's group name (e.g. `Git/GitHub`, `Docker Compose`)

Separator lines start with `#` (e.g. `# -------------------- Git --------------------`) and are ignored by the build but useful for human scanning. No blank lines are allowed. All non‑comment lines must have exactly three commas (4 columns).

## Pages & Navigation

Navigation lives in `_data/lang-data.yml`. Example excerpt:

```yml
- lang-name: Python
  lang-alias: py
  page: py-cheat.html
  children:
    - lang-name: Pandas
      page: pandas-cheat.html
    - lang-name: Pipenv
      page: pipenv-cheat.html
```

If `children` is present, the home page shows a badge with the number of child items and renders extra cards for each child.

## Adding Commands

1. Open `_data/store-data.csv`.
2. Locate the correct section or add a new `# -------------------- NAME --------------------` separator.
3. Append a new line: `command,Description,Category,GroupName`
4. Ensure there are EXACTLY 4 columns (3 commas). Do not leave trailing commas.
5. Avoid raw double quotes inside fields; prefer single quotes or escape properly.
6. Keep descriptions short (<= 60 chars ideal).

Example:

```liquid
    {% endfor %}
    </tbody>
  </table>
{% endfor %}
```

## CSV Validation Workflow

Automated safety net: `.github/workflows/csv-validate.yml` runs `scripts/validate_csv.py` on every push / pull request to `main`.

The script enforces:

- Header matches: `comandos,descricao,categoria,grupo`
- No blank lines
- Exactly 4 columns for non‑comment lines
- No unbalanced double quotes
- Warns about duplicate (command + group) pairs

Run locally (PowerShell / Bash):

```bash
python scripts/validate_csv.py
```

If it exits with code 1 fix the reported errors before pushing.

## Roadmap

Completed:

- [x] Hierarchical navigation (Python → Pandas / Pipenv; Docker → Docker Compose; Linux distros)
- [x] Remove legacy PyCharm content
- [x] Windows (winget + system + setup) section
- [x] Home page card layout
- [x] English translation of data & pages
- [x] CSV structural validator & GitHub Action

Planned / Ideas:

- [ ] Theming variable for card color palette
- [ ] Optional non‑table (freeform) content blocks
- [ ] Auto‑generate menu from CSV groups (reduce duplication with YAML)
- [ ] Additional Python tools (e.g. Poetry, PyInstaller, Plotly examples)
- [ ] Excel / VBA cheat sheets
- [ ] Normalize category naming style

## Development

Local Jekyll build (optional if you just rely on GitHub Pages):

1. Create a `Gemfile` with `github-pages` gem (not yet included in repo).
2. Run `bundle install`.
3. Serve: `bundle exec jekyll serve`.

> For now the repository relies on GitHub Pages’ built-in build environment.

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make changes (ensure CSV passes validation)
4. Commit: `git commit -m "feat: add X"`
5. Push: `git push origin feat/your-feature`
6. Open a Pull Request

Please keep commands concise and in English.

## License

MIT License. See [LICENSE](LICENSE.md).

---

Made with simple data + Liquid. PRs welcome.

[Back to top](#cheat-sheets)
