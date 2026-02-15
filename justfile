# Justfile for Pelican static site

# Default recipe - show help
default:
    @just --list

# Configuration
INPUTDIR := "content"
OUTPUTDIR := "output"
CONFFILE := "pelicanconf.py"
PUBLISHCONF := "publishconf.py"
GITHUB_PAGES_BRANCH := "master"
# Aliases
alias sp := spellcheck
alias spf := spellcheck-fix
alias s := serve
alias sd := serve-drafts

# Spell check markdown files (optionally pass a specific file)
spellcheck file="":
    #!/usr/bin/env bash
    if [ -z "{{file}}" ]; then
        uv run codespell {{INPUTDIR}}/*.md {{INPUTDIR}}/**/*.md --skip="*.ipynb"
    else
        uv run codespell "{{file}}"
    fi


# Spell check with interactive fix mode (optionally pass a specific file)
spellcheck-fix file="":
    #!/usr/bin/env bash
    if [ -z "{{file}}" ]; then
        uv run codespell {{INPUTDIR}}/*.md {{INPUTDIR}}/**/*.md --skip="*.ipynb" -i 3 -w
    else
        uv run codespell "{{file}}" -i 3 -w
    fi

# Review: run spell check and build site to check for errors
review: spellcheck
    uv run pelican {{INPUTDIR}} -o {{OUTPUTDIR}} -s {{CONFFILE}}
    @echo "Review complete. Check output above for any issues."

# Build the site for local development
build:
    uv run pelican {{INPUTDIR}} -o {{OUTPUTDIR}} -s {{CONFFILE}}

# Build the site with production settings
publish:
    uv run pelican {{INPUTDIR}} -o {{OUTPUTDIR}} -s {{PUBLISHCONF}}

# Serve site locally with live reload
serve:
    uv run pelican -lr {{INPUTDIR}} -o {{OUTPUTDIR}} -s {{CONFFILE}}

# Serve site locally with drafts visible
serve-drafts:
    uv run pelican -lr {{INPUTDIR}} -o {{OUTPUTDIR}} -s {{CONFFILE}} -D

# List all draft posts
list-drafts:
    @grep -l "status: draft" {{INPUTDIR}}/*.md {{INPUTDIR}}/**/*.md 2>/dev/null || echo "No drafts found"

# Deploy to GitHub Pages
deploy: publish
    uv run ghp-import -m "Generate Pelican site" -b {{GITHUB_PAGES_BRANCH}} {{OUTPUTDIR}}
    git push origin {{GITHUB_PAGES_BRANCH}}

# Full deploy workflow: spell check, publish, and deploy
deploy-full: spellcheck publish
    uv run ghp-import -m "Generate Pelican site" -b {{GITHUB_PAGES_BRANCH}} {{OUTPUTDIR}}
    git push origin {{GITHUB_PAGES_BRANCH}}

# Clean output directory
clean:
    rm -rf {{OUTPUTDIR}}
