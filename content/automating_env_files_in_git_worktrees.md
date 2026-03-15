---
Title: Automating .env Files in Git Worktrees: The Hook That Should Have Shipped with Git
Date: 2026-03-12
Author: Sephi Berry
Category: posts
Tags: git, worktrees, automation, developer-experience, devops, agor
Summary: Git worktrees respect .gitignore—which means they don't copy your .env files. Here's the 30-line bash hook that fixed this, the bare repository gotcha that broke it for three hours, and why global automation is both powerful and terrifying.
status: draft
---

# The Moment I Automated Away

It's 11:47 PM. I've just spun up my fourth worktree of the day to review a PR before bed. Run the tests. They fail.

```
Error: DATABASE_URL is not defined
```

Again.

For the fourth time today, I've forgotten to copy `.env` files to the new worktree. I spend 90 seconds finding the bare repository path (because Agor uses bare repos), another 30 seconds copying the files, and—crucially—I've lost the mental thread of what I was reviewing.

This isn't a 2-minute problem. It's a flow-state destruction problem.

**The math:** If you create 3-5 worktrees per day, and spend 2 minutes on environment setup each time, that's **30 hours per year** of pure friction. But the real cost isn't time—it's the cognitive overhead of remembering this manual step exists.

When you're using tools like [Agor](https://agor.live) that create worktrees automatically for agent orchestration, or CI/CD systems that spin them up for parallel test runs, manual environment propagation becomes untenable.

I spent three hours building a git hook to eliminate this. Then I spent three *more* hours debugging why it silently failed on bare repositories. Here's what I learned.

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

We used to solve "environment per branch" by checking in `.env.example` and copying it manually. That worked when you created a branch once a week. It breaks down when you're creating worktrees five times a day.

Let's fix it.

---

# Three Approaches to Environment Propagation

## Option 1: Symlinks (Single Source of Truth)

The simplest approach: link all worktrees to a centralized `.env` file.

```bash
# From your worktree directory
ln -s ~/.agor/repos/jounce/.env .env
```

**Trade-off:** You get a single source of truth—update the central file, all worktrees see it. But you've eliminated isolation. If you need to test against staging in one worktree and production (read-only) in another, symlinks break the model.

```
# All worktrees point to the same config
main/.env         -> ~/repos/project/.env
feature-a/.env    -> ~/repos/project/.env  # Can't diverge!
feature-b/.env    -> ~/repos/project/.env
```

**When to use:** Small teams, single environment, rarely diverging configs.

**When to avoid:** Multi-region deployments, feature flag testing, any scenario where per-worktree config matters.

---

## Option 2: Manual Setup Scripts (Explicit Control)

Add a `justfile` or Makefile target that developers run manually:

```bash
# justfile
setup-env:
    @echo "Copying .env files from main repo..."
    @cp ~/.agor/repos/jounce/.env* .
```

Then run it after creating a worktree:

```bash
git worktree add ../feature-x
cd ../feature-x
just setup-env  # Explicit, no surprises
```

**Trade-off:** You get explicit control. No global automation side effects. The cost? Every developer has to remember to run it. Every. Single. Time.

**When to use:** Infrequent worktree creation, teams that value explicitness over convenience.

**When to avoid:** High-velocity teams, automated worktree creation, workflows where "remember to run the script" becomes a single point of failure.

---

## Option 3: Global Git Hook (Zero-Touch Automation)

A `post-checkout` hook that runs automatically when worktrees are created.

This is the option I chose. Here's why: I use Agor for multi-agent orchestration, which creates worktrees programmatically. Manual steps don't scale.

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
/Users/josephberry/.agor/repos/jounce/.git

$ git rev-parse --git-dir
/Users/josephberry/.agor/repos/jounce/.git  # Same!

# Worktree
$ git rev-parse --git-common-dir
/Users/josephberry/.agor/repos/jounce/.git  # Points to main

$ git rev-parse --git-dir
/Users/josephberry/.agor/worktrees/jounce/feature-x/.git  # Different!
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
.agor/repos/jounce/.git/        # Bare repo (no checkout)
.agor/worktrees/jounce/main/    # Worktree (has checkout)
```

If you try to run `git check-ignore` from a bare repo directory, git fails:

```bash
$ cd .agor/repos/jounce/.git
$ git check-ignore .env
fatal: this operation must be run in a work tree
```

By switching to the worktree context with `cd "$WORKTREE_ROOT"`, we sidestep this entirely. The worktree *does* have a working tree, so it can evaluate `.gitignore` rules.

This detail cost me three hours of debugging. The hook ran, printed success, and did nothing. The `git check-ignore` command failed silently, and I didn't notice because I suppressed the errors with `2>/dev/null`.

**Lesson:** Always validate that your automation did what you think it did. Don't trust exit codes—check the filesystem.

---

# Validation: Does It Actually Work?

Let me show you this in action. I'll create a new worktree through Agor (which uses bare repos) with five different `.env` files in the main repository.

**Before creating the worktree:**

```bash
$ ls ~/.agor/repos/jounce/.env*
.env.dev  .env.eu.prd  .env.test  .env.us.dev  .env.us.prd
```

**Create the worktree:**

```bash
$ git worktree add ../test-delete-me
Preparing worktree (new branch 'test-delete-me')
HEAD is now at bde5f89f wip: pre review
🔧 Git worktree detected - checking for .env files to copy...
  ✓ Copied .env.dev to worktree
  ✓ Copied .env.eu.prd to worktree
  ✓ Copied .env.test to worktree
  ✓ Copied .env.us.dev to worktree
  ✓ Copied .env.us.prd to worktree
✅ .env setup complete for worktree
```

**Verify in the new worktree:**

```bash
$ cd ../test-delete-me
$ ls -la .env*
-rw-r--r--  .env.dev
-rw-r--r--  .env.eu.prd
-rw-r--r--  .env.test
-rw-r--r--  .env.us.dev
-rw-r--r--  .env.us.prd
```

Zero manual intervention. Works with bare repos. Applies globally to all repos on my system.

---

# The Battle Scars: What They Don't Tell You About Global Hooks

## 1. Silent Failures Will Destroy Your Productivity

The first version of this hook ran, printed success messages, and did absolutely nothing. The `git check-ignore` failed silently, the error was suppressed, and I assumed it worked.

I spent an hour running the hook manually, adding `set -x` debug output, and tracing through the execution before I realized: **I wasn't validating the actual output**.

```bash
# What I should have done immediately
$ ls worktree/.env*  # Does the file exist?
ls: .env*: No such file or directory  # Nope!
```

**Lesson:** Test the outcome, not the process. If your automation says it worked, verify the filesystem state.

## 2. Bare Repositories Are Everywhere in Modern Workflows

If you're using Agor, GitLab CI/CD runners, or GitHub Actions with worktrees, you're dealing with bare repos. The first version of this hook assumed a working tree existed. It doesn't.

**Always test your git automation against bare repositories:**

```bash
# Create a test bare repo
$ git clone --bare https://github.com/user/repo.git test-bare
$ cd test-bare
$ git worktree add ../test-worktree
# Does your hook work?
```

## 3. Global Hooks Are Powerful But Dangerous

This hook runs for *every* repository on your system. Every branch switch. Every worktree creation.

If you introduce a bug—an infinite loop, a `rm -rf`, an accidental network call—you've broken your entire development environment.

I've seen global hooks that:
- Broke CI pipelines by assuming specific directory structures
- Introduced 5-second delays on every `git checkout` (they were hitting the network!)
- Silently corrupted repos by copying tracked files

**Safeguards I added:**

```bash
# 1. Suppress errors in repos without expected structure
2>/dev/null

# 2. Only copy gitignored files (never touch tracked files)
git check-ignore -q "$rel_path"

# 3. Never overwrite existing files (respect manual configs)
if [ ! -f "$target" ]; then

# 4. Limit search depth to prevent performance death
find "$MAIN_REPO_ROOT" -maxdepth 3
```

## 4. Performance Matters at Scale

I originally used `find` with no depth limit. On a large monorepo with nested `node_modules`, this added **8 seconds** to every worktree creation.

```bash
# Before (slow)
find "$MAIN_REPO_ROOT" -name '.env*' -type f

# After (fast)
find "$MAIN_REPO_ROOT" -maxdepth 3 -name '.env*' -type f
```

`maxdepth 3` brought it back under 100ms. Measure your automation—death by a thousand papercuts is still death.

## 5. Global Hooks Break Team Onboarding

If you rely on this hook and forget to document it, new team members will waste hours debugging why worktrees "just work" on your machine but fail on theirs.

**Solutions:**
- Add hook setup to your team's onboarding docs
- Commit a project-local hook to `.git/hooks/` and teach people to symlink it
- Consider using a dotfiles manager that installs hooks automatically

---

# Decision Framework: Which Approach Should You Use?

## Use the global hook if:

✅ You create worktrees frequently (3+ per day)
✅ You use tools that automate worktree creation (Agor, CI/CD)
✅ You work with bare repositories
✅ You value zero-touch workflows and are willing to maintain the hook
✅ Your environment files rarely need per-worktree customization

## Use manual scripts if:

✅ You rarely create worktrees (less than once per week)
✅ You need different configs per worktree (staging vs prod)
✅ You want explicit control over environment propagation
✅ Your team is uncomfortable with global git automation

## Use symlinks if:

✅ You have a single environment and rarely need isolation
✅ Your worktrees never diverge in configuration
✅ You're willing to sacrifice isolation for simplicity

---

# Conclusion: Automate Friction, But Measure the Cost

Developer experience is measured in **friction removed**, not features added.

This 30-line bash script eliminated a recurring pain point I'd tolerated for months. But the bare repository gotcha cost me three hours of debugging. That three hours taught me more about git worktree internals than the previous year of casual usage.

**The principle:** Automate the things you do frequently, but measure the cost.

Global hooks are powerful. They're also a liability. If your hook breaks, it breaks *everything*. Test against bare repos. Validate actual behavior, not just exit codes. Document it for your team.

If you're using git worktrees in production workflows—especially with orchestration tools like Agor—automate your environment management. But do it carefully. Your 2am debugging self will either thank you or curse you, depending on whether you tested the edge cases.

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

**Questions I'm still exploring:**

- How do teams handle per-worktree secrets with tools like `direnv`?
- What's the best approach for multi-region deployments where each worktree needs region-specific configs?
- Has anyone integrated this with secret managers (1Password, AWS Secrets Manager) for automated secret rotation?

*If you've solved environment propagation differently—especially in high-velocity CI/CD environments or multi-region setups—I'd love to hear about it. Drop me a note or open an issue with your approach.*
