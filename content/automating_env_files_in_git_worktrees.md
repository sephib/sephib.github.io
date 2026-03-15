---
Title: Automating .env Files in Git Worktrees: The Hook That Should Have Shipped with Git
Date: 2026-03-12
Author: Sephi Berry
Category: posts
Tags: git, worktrees, automation, developer-experience, devops, agor
Summary: Git worktrees don't copy gitignored files because they respect .gitignore. This is correct behavior—but it's also a pain in the ass when you're creating worktrees automatically. A global post-checkout hook solves this, but only if you understand bare repositories.
status: draft
---

# The "So What?": Flow-State Destruction at Scale

If you're still manually copying `.env` files to git worktrees, you're bleeding time. Not hours—minutes per worktree. But those minutes compound into something worse than lost productivity: **flow-state destruction**.

Here's the scenario: You're working on a feature branch. You need to quickly switch context to review a PR. You create a new worktree, run the tests, and they fail with `DATABASE_URL not found`. You've forgotten to copy the `.env` file. Again.

The problem isn't the 30 seconds it takes to copy files—it's the **mental context switch** of remembering to do it, finding the source directory (especially fun with bare repositories), and the cognitive overhead of "which .env files do I actually need?" When you're creating 3-5 worktrees per day—or using orchestration tools like [Agor](https://agor.live) that spin them up automatically—this friction becomes untenable.

**The math is simple:** Manual steps that happen frequently are technical debt masquerading as "best practices."

---

# Historical Context: How We Got Here

Git worktrees are the spiritual successor to the old `git checkout` branch dance we did in 2010. Back then, switching branches meant stashing work, hoping nothing broke, and praying your IDE didn't lose its mind rebuilding indexes. Worktrees fixed that by giving each branch its own isolated working directory—a clean separation that mirrors what we learned from containerization: isolation beats shared mutable state.

But worktrees inherited a design decision from `git checkout`: they respect `.gitignore`. This is **architecturally correct**—gitignored files are local configuration, not source code. They shouldn't propagate automatically.

The problem? That architectural purity breaks down when you have:
- **Multiple environment files** (`.env.dev`, `.env.staging`, `.env.prod`)
- **Automated worktree creation** (CI/CD, orchestration platforms)
- **Bare repositories** (modern tooling like Agor, GitLab runners)

We used to solve "environment configuration per branch" by checking in `.env.example` and copying it manually. That worked when you created a branch once a week. It doesn't scale when you're creating worktrees 5 times a day.

---

# The Technical Deep Dive: Three Approaches to Environment Propagation

## Pillar 1: Symlinks (Single Source of Truth)

**Approach:** Link all worktrees to a centralized `.env` file.

```bash
ln -s /Users/josephberry/.agor/repos/jounce/.env .env
```

**Architectural trade-off:** This gives you a single source of truth—change the central file, all worktrees pick it up. But you've also eliminated isolation: all worktrees share the same configuration. If you need to test against a staging database in one worktree and production (read-only) in another, symlinks break the model.

**When this works:** Small teams, single environment, rarely diverging configs.

**When this breaks:** Multi-region deployments, testing different feature flags per branch, or any scenario where worktree-specific config matters.

---

## Pillar 2: Manual Setup Scripts (Explicit Control)

**Approach:** Add a `justfile` or Makefile target that developers run manually.

```bash
just setup-env  # Copies .env files from main repo to current worktree
```

**Architectural trade-off:** You get explicit control over when/what gets copied. No surprises, no global automation side effects. The cost? Every developer has to remember to run it. Every. Single. Time.

**When this works:** Infrequent worktree creation, teams that value explicitness over convenience.

**When this breaks:** High-velocity teams, automated worktree creation (CI/CD), or any workflow where "remembering to run the script" becomes a SPOF for productivity.

---

## Pillar 3: Global Git Hook (Zero-Touch Automation)

**Approach:** A `post-checkout` hook that runs automatically when worktrees are created.

```bash
# Setup (one-time)
mkdir -p ~/.git-hooks
git config --global core.hooksPath ~/.git-hooks

# Create ~/.git-hooks/post-checkout (script below)
chmod +x ~/.git-hooks/post-checkout
```

**The hook:**

```bash
#!/bin/bash
# Global git hook to automatically copy .env files to new worktrees

MAIN_REPO_PATH=$(git rev-parse --git-common-dir 2>/dev/null)
CURRENT_PATH=$(git rev-parse --git-dir 2>/dev/null)

if [ "$MAIN_REPO_PATH" != "$CURRENT_PATH" ]; then
    MAIN_REPO_ROOT=$(dirname "$MAIN_REPO_PATH")
    WORKTREE_ROOT=$(git rev-parse --show-toplevel)

    echo "🔧 Git worktree detected - checking for .env files to copy..."

    env_files=$(find "$MAIN_REPO_ROOT" -maxdepth 3 -name '.env*' -type f 2>/dev/null)

    echo "$env_files" | while read -r env_file; do
        rel_path="${env_file#$MAIN_REPO_ROOT/}"

        # CRITICAL: Check from worktree context (works with bare repos!)
        if (cd "$WORKTREE_ROOT" && git check-ignore -q "$rel_path" 2>/dev/null); then
            target="$WORKTREE_ROOT/$rel_path"
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

**Architectural trade-offs:**
- **Pro:** Fully automatic. Works with Agor, CI/CD, any tool that creates worktrees.
- **Pro:** Global—one setup, applies to all repos on the system.
- **Con:** Global hooks run for *every* repo. If the script has a bug, it affects everything.
- **Con:** Debugging is harder—hooks run invisibly in the background.

**Edge case that breaks most implementations:** Bare repositories (see Battle Scars section).

---

# How It Works: Worktree Detection and Gitignore Context

The hook works by comparing two git internals:

```bash
--git-common-dir  # Where the shared .git directory lives
--git-dir         # Where the current .git directory lives
```

In a regular repo, these are the same. In a worktree, they differ—`--git-common-dir` points to the main repo, `--git-dir` points to the worktree's `.git` file.

**The critical line:**

```bash
if (cd "$WORKTREE_ROOT" && git check-ignore -q "$rel_path" 2>/dev/null); then
```

This runs `git check-ignore` **from the worktree context**, not from the main repo. Why does this matter?

**Bare repositories don't have a working tree.** If you try to run `git check-ignore` from a bare repo directory, git fails because there's no checkout to evaluate `.gitignore` rules against. By switching to the worktree context, we sidestep this entirely.

---

# Validation: Does It Actually Work?

**Test case:** Create a new worktree via Agor with 5 different `.env` files in the main repo.

**Hook output:**

```
🔧 Git worktree detected - checking for .env files to copy...
  ✓ Copied .env.us.dev to worktree
  ✓ Copied .env.us.prd to worktree
  ✓ Copied .env.test to worktree
  ✓ Copied .env.dev to worktree
  ✓ Copied .env.eu.prd to worktree
✅ .env setup complete for worktree
```

**Verification:**

```bash
ls -la /Users/josephberry/.agor/worktrees/Jounce-IO/jounce/test-delete-me/.env*

-rw-r--r--  .env.dev
-rw-r--r--  .env.eu.prd
-rw-r--r--  .env.test
-rw-r--r--  .env.us.dev
-rw-r--r--  .env.us.prd
```

Zero manual intervention. Works with bare repos. Scales globally.

---

# The Battle Scars Section: What They Don't Tell You

**Bare repositories are everywhere in modern workflows.** If you're using Agor, GitLab CI/CD runners, or GitHub Actions with worktrees, you're dealing with bare repos. The first version of this hook failed silently for 3 hours because I assumed a working tree existed. It doesn't. Always test your git automation against bare repos.

**Silent failures will destroy your productivity.** The initial hook ran, printed success messages, and did absolutely nothing. The `git check-ignore` command failed silently, the error was suppressed, and I assumed it worked. **Always validate that your automation actually did what you think it did.** Don't trust exit codes—check the filesystem.

**Global hooks are powerful but dangerous.** This hook runs for *every* repository on your system. Every branch switch. Every worktree creation. If you fat-finger the script and introduce an infinite loop or a `rm -rf`, you've just nuked your entire development environment. I've seen global hooks that:
- Broke CI pipelines by assuming specific directory structures
- Introduced 5-second delays on every `git checkout` (they were hitting the network!)
- Silently corrupted repos by copying tracked files

**Safeguards I added:**
- `2>/dev/null` to suppress errors in repos without the expected structure
- Only copy files that match `.gitignore` (never touch tracked files)
- Never overwrite existing files (respect manual configurations)
- Limit `find` depth to 3 levels (prevent performance death in monorepos)

**Performance matters at scale.** I originally used `find` with no depth limit. On a large monorepo, this added 8 seconds to every worktree creation. `maxdepth 3` brought it back under 100ms. Measure your automation—death by a thousand papercuts is still death.

**Global hooks break team onboarding.** If you rely on this hook and forget to document it, new team members will waste hours debugging why their worktrees "just work" on your machine but fail on theirs. Add it to your team's setup documentation, or better yet, commit a project-local hook to `.git/hooks/` and teach people to symlink it.

---

# When to Use This Approach (And When Not To)

**Use the global hook if:**
- You create worktrees frequently (3+ per day)
- You use tools that automate worktree creation (Agor, CI/CD)
- You work with bare repositories
- You value zero-touch workflows and are willing to maintain the hook

**Use manual scripts if:**
- You rarely create worktrees (less than once per week)
- You need different configs per worktree (staging vs prod)
- You want explicit control over environment propagation
- Your team is uncomfortable with global git automation

**Use symlinks if:**
- You have a single environment and rarely need isolation
- Your worktrees never diverge in configuration
- You're willing to sacrifice isolation for simplicity

---

# The Pragmatic Takeaway

Developer experience is measured in **friction removed**, not features added. This 30-line bash script eliminated a recurring pain point that I'd tolerated for months. The bare repository gotcha cost me 3 hours, but understanding *why* it failed made the architecture clearer.

**The principle:** Automate the things you do frequently, but measure the cost. Global hooks are powerful, but they're also a liability. If your hook breaks, it breaks *everything*. Test against bare repos, validate actual behavior (not just exit codes), and document the hell out of it for your team.

If you're using git worktrees in production workflows—especially with orchestration tools—automate your environment management. But do it carefully. Your 2am debugging self will either thank you or curse you, depending on whether you tested the edge cases.

---

**Full hook script:** Available in this post (copy the code block above)

**Related reading:**
- [Working with Git Worktrees - Chris DiCarlo](https://chrisdicarlo.ca/blog/working-with-git-worktrees-part-2/)
- [therohitdas/copy-env](https://github.com/therohitdas/copy-env) - Similar approach as a standalone tool

*Have you solved this differently? Especially interested in hearing from teams using direnv, per-worktree configs, or alternative strategies for multi-region setups.*
