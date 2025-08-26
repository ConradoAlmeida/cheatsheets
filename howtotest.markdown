# Local Testing & Development Guide

This guide explains how to clone, validate, and run the site locally on different environments (Windows native, WSL2, Debian/Ubuntu based, Fedora) plus an optional Docker method. Use this when reviewing Pull Requests before merging.

---

## 1. Repository Structure Essentials

Key files involved in a local build:

- _data/store-data.csv (command data source – STRICT 4 columns)
- _data/lang-data.yml (navigation hierarchy)
- index.html / *-cheat.html pages (Liquid templates)
- scripts/validate_csv.py (structure validator)

You can test most changes just by editing the CSV & YAML then reloading the local server.

---

## 2. CSV Validation (Always First)

Run (Python 3 required):

```bash
python scripts/validate_csv.py
```

Success: "CSV validation passed". Any ERROR must be fixed before build / PR approval.

---

## 3. Windows (Native) Setup

1. Install Ruby + DevKit (from <https://rubyinstaller.org>) – choose version compatible with GitHub Pages (3.2.x typically).
1. Create a Gemfile (if not present) with:

   ```ruby
   source 'https://rubygems.org'
   gem 'github-pages', group: :jekyll_plugins
   ```

1. Install dependencies:

   ```bash
   bundle install
   ```

1. Serve site:

   ```bash
   bundle exec jekyll serve --livereload
   ```

1. Browse: <http://127.0.0.1:4000>
1. Validate CSV after any data edit:

   ```bash
   python scripts/validate_csv.py
   ```

Troubleshooting:

- If "bundle" not found: `gem install bundler`
- Delete `_site` and `.jekyll-cache` if stale build issues appear.

---

## 4. WSL2 (Ubuntu / Debian) Setup

Recommended to keep dev tooling isolated from Windows.

1. Install WSL (if needed): `wsl --install -d Ubuntu`
1. Update packages:

   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

1. Install prerequisites:

   ```bash
   sudo apt install -y build-essential ruby-full zlib1g-dev git python3
   ```

1. (Optional) Use user gem directory:

   ```bash
   echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
   echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

1. Clone project (or work inside a Linux copy):

   ```bash
   cd ~/projects && git clone https://github.com/ConradoAlmeida/cheatsheets.git
   cd cheatsheets
   ```

1. Install gems:

   ```bash
   bundle install
   ```

1. Serve:

   ```bash
   bundle exec jekyll serve --livereload --host 0.0.0.0
   ```

1. Access from Windows browser: <http://127.0.0.1:4000>
1. Validate CSV:

   ```bash
   python3 scripts/validate_csv.py
   ```

Performance Note: For faster file IO keep the repo inside the Linux filesystem (e.g. `~/projects`) rather than `/mnt/c/`.

---

## 5. Native Debian / Ubuntu (Outside WSL)

Essentially identical to WSL2 steps above:

```bash
sudo apt update && sudo apt install -y build-essential ruby-full zlib1g-dev git python3
bundle install
bundle exec jekyll serve
```

Then visit: <http://localhost:4000>

---

## 6. Fedora Setup

1. Install dependencies:

   ```bash
   sudo dnf install -y @development-tools ruby ruby-devel zlib-devel redhat-rpm-config git python3
   ```

1. (Optional) Set GEM_HOME:

   ```bash
   echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
   echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

1. Clone project:

   ```bash
   git clone https://github.com/ConradoAlmeida/cheatsheets.git
   cd cheatsheets
   ```

1. Install gems:

   ```bash
   bundle install
   ```

1. Serve:

   ```bash
   bundle exec jekyll serve --livereload
   ```

1. Validate CSV:

   ```bash
   python3 scripts/validate_csv.py
   ```

SELinux Note: Usually no change needed; if port blocked, allow 4000 or use `--port 4001`.

---

## 7. Optional Docker Method

From project root (no Ruby on host):

```bash
docker run --rm -p 4000:4000 -v "$PWD":/srv/jekyll -it jekyll/jekyll jekyll serve --livereload
```

Browse <http://127.0.0.1:4000>.

Run CSV validation on host (needs Python) or add another container stage.

---

## 8. Pull Request Review Flow

1. Fetch PR 42 example:

   ```bash
   git fetch origin pull/42/head:pr-42
   git checkout pr-42
   ```

1. Run validator:

   ```bash
   python3 scripts/validate_csv.py
   ```

1. Start server:

   ```bash
   bundle exec jekyll serve
   ```

1. Manual checks:

   - New group appears (home + nav)
   - No blank pages
   - Tables render; no malformed cells
   - Existing sections unaffected

1. Approve or request changes.

---

## 9. Gemfile Reference

Commit for reproducibility:

```ruby
source 'https://rubygems.org'
gem 'github-pages', group: :jekyll_plugins
```

---

## 10. Common Issues & Fixes

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| Build hangs or Pages timeout | Malformed CSV (column count) | Run validator & fix line shown |
| Liquid error for undefined variable | Typo in grupo name | Ensure CSV grupo matches page filter |
| Child cards missing | Missing children array or duplicate entry | Check `_data/lang-data.yml` for duplicates |
| Garbled Pandas multi-column command | Unquoted commas inside field | Wrap command in double quotes |
| Slow file updates in WSL | Repo on `/mnt/c` | Move repo to Linux filesystem |

---

## 11. Clean Up / Reset

Remove generated artifacts:

```bash
rm -rf _site .jekyll-cache vendor
```

Reinstall:

```bash
bundle install
```

---

## 12. Security / Contribution Notes

- Never commit secrets (none required).
- Keep descriptions short and English-only.
- Run validator before every commit that touches the CSV.

---

Happy testing! Open an issue if you find a gap in this guide.
