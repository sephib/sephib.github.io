---
Title: Automating .env Files in Git Worktrees
Date: 2026-03-12
Author: Sephi Berry
Category: posts
Tags: git, worktrees, automation, devops, agor
Summary: Git worktrees respect .gitignore — which means they don't have .env files from the bare git cloned repo. Here's a bash hook that fixed this.
---

# The Moment I Automated Away

It's 11:47 PM. I've just spun up my fourth worktree of the day to review a PR before bed. Run the tests. They fail.

```
Error: DATABASE_URL is not defined
```

Again.

For the fourth time today, I've forgotten to copy `.env` files to the new worktree. I spend 90 seconds finding the repository path (because Agor uses bare repos), another 30 seconds copying the files, and—crucially—I've lost the mental thread of what I was reviewing.

When you're using tools like [Agor](https://agor.live) that create git worktrees automatically for each agent task, manual environment propagation becomes untenable.

---

# Why Git Worktrees Don't Copy .env Files (And Why That's Correct)

Git worktrees solve a problem we've had since 2010: the branch-switching dance. Before worktrees, switching branches meant stashing work, hoping the checkout didn't break, and watching your IDE rebuild indexes. Worktrees give each branch its own isolated working directory:

```
project/
├── main/           # main branch worktree
├── feature-auth/   # feature branch worktree
└── .git/           # shared git metadata
```

But worktrees inherit a design decision from `git checkout`: **they respect `.gitignore`**. This is architecturally correct—gitignored files are local configuration, not source code. They shouldn't propagate automatically.

The problem emerges when you have:
- **Multiple environment files** (`.env`, `.env.test`, `.env.staging`)
- **Automated worktree creation** (CI/CD, orchestration platforms)
- **Bare repositories** (modern tooling like Agor, GitLab runners, GitHub Actions)

We used to solve "environment per branch" by checking in `.env.example` and copying it manually. Then once the `.env` was configured - any branch in that was in the folder had an up-to-date `.env` file. But now when we have a separate folder for each branch - we need to manually copy the `.env` whenever we create a new _git worktree_

Let's fix it.

---

# Global Git Hook (Zero-Touch Automation)

A `post-checkout` hook that runs automatically when worktrees are created.

### The Hook Architecture

Git provides hooks—scripts that run at specific lifecycle events. `post-checkout` runs after any checkout operation, including worktree creation. We can detect worktrees by comparing two git internals:

```bash
--git-common-dir  # The shared .git directory (main repo)
--git-dir         # The current .git directory (worktree-specific)
```

In a regular repo, these paths are identical. In a worktree, they differ:

```
# Main repo
$ git rev-parse --git-common-dir
~/.agor/repos/my-repo/.git

$ git rev-parse --git-dir
~/.agor/repos/my-repo/.git  # Same!

# Worktree
$ git rev-parse --git-common-dir
~/.agor/repos/my-repo/.git  # Points to main

$ git rev-parse --git-dir
~/.agor/worktrees/my-repo/feature-x/.git  # Different!
```

When they differ, we know we're in a worktree. Then we can copy `.env` files from the main repo.

### Setup (One-Time)

```bash
# Create global hooks directory
mkdir -p ~/.git-hooks

# Tell git to use it for all repos
git config --global core.hooksPath ~/.git-hooks

# Create the hook
touch ~/.git-hooks/post-checkout
chmod +x ~/.git-hooks/post-checkout
```

### The Hook Implementation

Here's the full script with inline commentary on the critical decisions:

```bash
#!/bin/bash
# Global git hook: automatically copy .env files to new worktrees

# Get paths to git directories
MAIN_REPO_PATH=$(git rev-parse --git-common-dir 2>/dev/null)
CURRENT_PATH=$(git rev-parse --git-dir 2>/dev/null)

# Detect if we're in a worktree (paths differ)
if [ "$MAIN_REPO_PATH" != "$CURRENT_PATH" ]; then
    # Get filesystem paths (not .git internals)
    MAIN_REPO_ROOT=$(dirname "$MAIN_REPO_PATH")
    WORKTREE_ROOT=$(git rev-parse --show-toplevel)

    echo "🔧 Git worktree detected - checking for .env files to copy..."

    # Find all .env files in main repo
    # maxdepth 3: prevents performance death in monorepos
    # 2>/dev/null: suppress errors in repos without .env files
    env_files=$(find "$MAIN_REPO_ROOT" -maxdepth 3 -name '.env*' -type f 2>/dev/null)

    echo "$env_files" | while read -r env_file; do
        # Get relative path (e.g., ".env" or "apps/web/.env")
        rel_path="${env_file#$MAIN_REPO_ROOT/}"

        # CRITICAL: Check gitignore from worktree context
        # This is the line that makes it work with bare repositories
        if (cd "$WORKTREE_ROOT" && git check-ignore -q "$rel_path" 2>/dev/null); then
            target="$WORKTREE_ROOT/$rel_path"

            # Only copy if file doesn't exist (respect manual configs)
            if [ ! -f "$target" ]; then
                mkdir -p "$(dirname "$target")"
                cp "$env_file" "$target"
                echo "  ✓ Copied $rel_path to worktree"
            fi
        fi
    done

    echo "✅ .env setup complete for worktree"
fi
```

### Why the `cd $WORKTREE_ROOT` Matters

The most important line in this script is:

```bash
if (cd "$WORKTREE_ROOT" && git check-ignore -q "$rel_path" 2>/dev/null); then
```

Why run `git check-ignore` from the worktree context instead of the current directory?

**Bare repositories don't have a working tree.**

If you're using Agor, GitLab CI, or GitHub Actions with worktrees, you're dealing with bare repos:

```
.agor/repos/my-repo/.git/        # Bare repo (no checkout)
.agor/worktrees/my-repo/main/    # Worktree (has checkout)
```

If you try to run `git check-ignore` from a bare repo directory, git fails:

```bash
$ cd .agor/repos/my-repo/.git
$ git check-ignore .env
fatal: this operation must be run in a work tree
```

By switching to the worktree context with `cd "$WORKTREE_ROOT"`, we sidestep this entirely. The worktree *does* have a working tree, so it can evaluate `.gitignore` rules.

**Lesson:** Always validate that your automation did what you think it did. Don't trust exit codes—check the filesystem.

---

# The Battle Scars: What They Don't Tell You About Global Hooks

## 5. Global Hooks Break Team Onboarding

If you rely on this hook and forget to document it, new team members will waste hours debugging why worktrees "just work" on your machine but fail on theirs.

**Solutions:**
- Add hook setup to your team's onboarding docs
- Commit a project-local hook to `.git/hooks/` and teach people to symlink it
- Consider using a dotfiles manager that installs hooks automatically

---


# Conclusion: Automate Friction, But Measure the Cost

Developer experience is measured in **friction removed**, not features added.

**The principle:** Automate the things you do frequently, but measure the cost.

Global hooks are powerful.

---

# Next Steps

**To implement this yourself:**

1. **Create the global hooks directory:**
   ```bash
   mkdir -p ~/.git-hooks
   git config --global core.hooksPath ~/.git-hooks
   ```

2. **Copy the hook script** (from the "Hook Implementation" section above) to `~/.git-hooks/post-checkout`

3. **Make it executable:**
   ```bash
   chmod +x ~/.git-hooks/post-checkout
   ```

4. **Test with a bare repo:**
   ```bash
   git clone --bare <your-repo-url> test-bare
   cd test-bare
   git worktree add ../test-worktree
   ls ../test-worktree/.env*  # Verify files copied
   ```

5. **Add to your team docs** so onboarding doesn't break

**Further reading:**

- [Git Worktrees Official Docs](https://git-scm.com/docs/git-worktree) - The canonical reference
- [Working with Git Worktrees - Chris DiCarlo](https://chrisdicarlo.ca/blog/working-with-git-worktrees-part-2/) - Practical workflows
- [therohitdas/copy-env](https://github.com/therohitdas/copy-env) - Similar approach as a standalone tool
- [Git Hooks Documentation](https://git-scm.com/docs/githooks) - All available hook types