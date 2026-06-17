---
Title: The 2-Hour Daily: When the Meeting Becomes the Work
Date: 2026-06-17
Author: Sephi Berry
Category: posts
Status: published
Summary: How the daily standup has been fully inverted by AI agents — from 15 minutes of reporting to 2 hours of deciding.
---

# The Meeting Nobody Needed

You know the ritual. Fifteen minutes every morning. "Yesterday I worked on the auth module. Today I'm continuing the auth module. No blockers." Repeat for eight people. Someone pastes a Jira link. The scrum master updates the board. Meeting over — now go do the actual work.

That model assumed one thing: humans generate output during the day, and the meeting exists to sync on that output. Reporting is the interface between the humans doing the work and the team trying to stay coordinated.

What if that assumption just broke?

Because here's what's happening on agentic teams right now: the agents worked overnight. By the time you open your laptop, there are already PRs to review, tickets updated, and three implementation branches in progress. The 15-minute report is irrelevant — you don't need to sync on human output when agent output is already in the repo.

What's been inverted isn't the cadence. It's the model itself.

---

# The First Flip

A while back I wrote about how [the standup shifted from "what did I do?" to "what did the agent do overnight?"](https://sephib.github.io/agent-dailies-and-the-flipped-development-cycle.html) — the flipped development cycle where agents handle rote implementation while humans spend their prime time on verification, steering, and resolving the ambiguities that agents correctly surface.

That was just the beginning.

What I didn't fully articulate then: the inversion doesn't stop at cadence. It goes all the way down. The standup isn't just reporting different things now — the standup *is* the work. The human's core contribution has moved from "implementing" to "deciding." And the daily session is where that deciding happens.

---

# Enter FullSend

The clearest signal I've seen that this isn't hypothetical came from a Red Hat engineering presentation that walked through the [FullSend framework](https://github.com/fullsend-ai/fullsend) — a living design document for fully autonomous agentic software development.

FullSend describes an end-to-end pipeline where agents triage incoming issues, implement solutions, run code review, and merge to production — with minimal human touchpoints. It's not a research paper or a speculative roadmap. It's a work in progress, but the teams involved are already feeling the shift. The direction is clear.

What struck me wasn't the autonomy of any single step. It's the architecture: the whole system is designed around the assumption that humans aren't the ones doing implementation. They're the ones setting direction and resolving the edge cases that agents correctly escalate.

When you look at FullSend, something becomes obvious: the meeting isn't a preamble to the work. It's the control plane for the work.

---

# The Daily as Control Room

Here's what actually happens in a well-run extended daily on an agentic team — and why each of these is *work*, not reporting:

**Strategic direction.** Which problems matter most this cycle? What's the shape of the solution we want? Agents are fast. Misdirected fast is expensive. Choosing the right target is a human call.

**Priority triage.** The backlog has 40 items agents could plausibly pick up today. Which 5 actually move the needle? That judgment doesn't delegate cleanly — it requires context about business constraints, team capacity, and technical risk that agents don't carry reliably.

**Escalation resolution.** Agents hit genuine ambiguity. When they do, they surface it rather than guess past it. The daily is where humans work through those cases — not as overhead, but as a feature. The agent asking "I found three valid approaches and can't determine which aligns with your architecture goals" is the system working correctly.

**Intent authoring.** This is the one that surprised me most when I saw it in practice. The highest-leverage work on an agentic team isn't code review — it's writing clear intent documents. Specs, acceptance criteria, architectural constraints, definitions of done. The quality of your input is the ceiling on the agent's output. Senior engineers who used to spend 70% of their time implementing now spend that time writing the kind of clear, precise intent that unlocks the next 24 hours of agent execution.

None of this is reporting. All of it is deciding. The meeting is the work.

---

# The Pipeline That Follows

The moment the daily ends, the pipeline spins up automatically.

A transcription agent captures everything discussed. A task-extraction agent parses decisions and action items from the transcript. Jira tickets get created or updated with full context. GitHub issues receive structured comments. Implementation agents pick up the queue — bug fixes, feature slices, refactors — and start executing in parallel branches.

By mid-afternoon, you have PRs to review and progress summaries ready for the next morning's session.

What runs on human time: the morning decisions. What runs on agent time: everything downstream. The meeting is the chokepoint in the best possible sense — where human judgment concentrates, then fans out into parallel execution that runs through the night.

I've been running variations of this workflow using [Agor](https://agor.live) for session orchestration, Claude Code for implementation, and a lightweight spec-based approach for intent capture. The pipeline is real. The leverage is real. The adjustment period is also real — it takes time to learn to write intent precisely enough that agents can execute without constant re-steering.

---

# The Train Rails

The metaphor that's been most useful for me: agents operate on train rails.

They need a track, not just a destination. You can tell a train where it's going, but without rails it doesn't move. The rails are: intent documents, spec-driven constraints, defined acceptance criteria, clear escalation paths, and architectural guardrails that tell the agent what category of solution is in scope.

The key thing most people get wrong here: this isn't about constraining agents. It's about enabling them to move fast without guessing at the wrong moments. Guardrails exist only where the cost of a wrong guess is high — not everywhere. Over-railing an agent is just bureaucracy in disguise. You want a clear track, not a cage.

The rails get laid in the daily. That's the insight I keep coming back to. The session isn't where you pick the destination — it's where you lay track. Better track means faster, more reliable execution through the night. Vague intent documents are rail gaps. They're where agents either stall or go off-path, and either outcome costs you the next morning's review session to untangle.

---

# The Adoption Gap

Most teams I talk to haven't started this yet. A few are deep into it. The gap between those two groups is growing.

For early adopters, the inversion is already the default. The questions are about optimization: tighter intent documents, better escalation design, smarter review gates, faster transcript-to-ticket pipelines.

For most orgs, the question is still "should we?" And the honest answer is: the longer you wait, the more ground you're giving up — not because the technology is moving fast (it is), but because the *practice* takes time to develop. Writing clear intent is a skill. Designing good escalation logic is a skill. Running an effective extended daily instead of a meandering status meeting is a skill. These don't come automatically with the tooling.

The developer skill that matters now isn't writing faster code. It's writing clearer intent. Engineers who can articulate what done looks like — precisely enough for an agent to execute, self-verify, and know when to escalate — are the ones who'll be setting direction for the rest of the team.

The meeting isn't overhead anymore.

It's the product.

---

*Notes:*

1. The FullSend framework mentioned above: [https://github.com/fullsend-ai/fullsend](https://github.com/fullsend-ai/fullsend) — worth reading as a design document even if you're not adopting it wholesale.
2. Prior post on the flipped development cycle: [Agent Dailies and the Flipped Development Cycle](https://sephib.github.io/agent-dailies-and-the-flipped-development-cycle.html)
3. Spec-driven development as a methodology for intent authoring: [Spec-driven development on Wikipedia](https://en.wikipedia.org/wiki/Spec-driven_development) and [speckit workflows](https://github.com/github/spec-kit)
