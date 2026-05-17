
# Publish workflow

## Rules for LLM agents — read before touching anything

- **Never open a PR.** All work goes directly to the `dev` branch. There is no PR review process.
- **Never push to a feature branch.** Always push commits to `dev` using `git push origin HEAD:dev`.
- **Never use plain `make` or `pelican` directly.** Pelican is not on the global PATH. Always prefix with `uv run` (e.g. `uv run make html`).
- **Drafts are invisible in the built site.** To publish a post, set `status: published` in the frontmatter before running `make github`.
- **`make github` is the single publish command.** It runs the production build and pushes to `master` (GitHub Pages). Do not push to `master` manually.
- **Images go in `content/images/`.** Reference them in markdown as `{static}/images/filename.jpg` (Pelican-specific syntax).

## Workflow

1. Edit content files under `content/`
2. Preview locally: `uv run make html` then `uv run make serve` → http://localhost:8000
   - To view a draft directly, open its URL manually (drafts are not listed in the index)
   - If port 8000 is taken, use `uv run make serve PORT=8080`
   - Stop the server with `pkill -f "pelican -l"`
3. Commit changes on the `dev` branch and push: `git push origin HEAD:dev`
4. When ready to go live: `uv run make github`
