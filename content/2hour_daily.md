---
Title: The 2-Hour Daily: When the Meeting Becomes the Work
Date: 2026-06-17
Author: Sephi Berry
Category: posts, agentic sdlc, daily
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

A while back I wrote about how [the standup shifted from "what did I do?" to "what did the agent do overnight?"](https://sephib.github.io/agent-dailies-and-the-flipped-development-cycle.html) — the flipped development cycle where agents handle the core implementation while humans spend their prime time on verification, steering, and resolving the ambiguities that agents surface.

That was just the beginning.

What I didn't fully understand then: the inversion doesn't stop at there. It goes all the way to the root of a _standup_. The standup isn't just reporting different things now — the standup *is* the work. The human's core contribution has moved from "implementing" to "deciding". And the daily session is where that deciding happens.

---

# Agentic SDLC - FullSend

The clearest signal I've seen that this isn't hypothetical came from a Red Hat engineering presentation that walked through the [FullSend agentic framework](https://github.com/fullsend-ai/fullsend) project — a living design document for fully autonomous agentic software development within GitHub.

FullSend describes an end-to-end pipeline where agents triage incoming issues, implement solutions, run code review, and merge to production — with minimal human touchpoints. It's a work in progress, but the teams involved are already feeling the shift.  

The Ah-Ah moment was when the presenter said that they increased the daily from 10 minutes to over an hour...


---

# The Daily as Control Room

Here's what actually happens in a well-run extended daily on an agentic team — and why the *work* is with in the *daily meeting*:

**Strategic direction.** Which problems matter most this cycle? What's the shape of the solution we want? Agents are fast. Misdirected fast is expensive. Choosing the right target is a human call.

**Priority triage.** The backlog has 40 items agents could plausibly pick up today. Which 5 actually move the needle? That judgment doesn't delegate cleanly — it requires context about business constraints, team capacity, and technical risk that agents don't carry reliably.

**Escalation resolution.** Agents hit genuine ambiguity. When they do, they should surface it rather than guess past it. The daily is where humans work through those cases — not as overhead, but as a feature. The agent asking "I found three valid approaches and can't determine which aligns with your architecture goals" is the system working correctly.

**Intent authoring.** The highest-leverage work on an agentic team isn't code review — it's writing clear intent documents. Specs, acceptance criteria, architectural constraints, definitions of done. The quality of your input is the ceiling on the agent's output. Senior engineers who used to spend 70% of their time implementing now spend that time writing the kind of clear, precise intent that unlocks the next 24 hours of agent execution.

None of this is reporting. All of it is deciding. The meeting is the work.

---

# The Pipeline That Follows

The moment the daily ends, the pipeline spins up automatically.

A transcription agent captures everything discussed. A task-extraction agent parses decisions and action items from the transcript. Jira tickets get created or updated with full context. GitHub issues receive structured comments. Implementation agents pick up the queue — bug fixes, feature slices, refactors — and start executing in parallel branches.

By mid-afternoon, you have PRs to review and progress summaries ready for the next morning's session.

What runs on human time: the morning decisions. What runs on agent time: everything downstream. The meeting is the chokepoint in the best possible sense — where human judgment concentrates, then fans out into parallel execution that runs through the night.

I've been running variations of this workflow using [Agor](https://agor.live) for session orchestration, Claude Code for implementation, and a lightweight spec-based approach for intent capture. The pipeline is real. The leverage is real. The adjustment period is also real — it takes time to learn setup the system and align with the team workflow.


---

# From Builders to Directors

Software teams used to organize around a simple model: engineers build, meetings coordinate.

Agentic development changes that.

If agents can implement, review, test, and move work forward asynchronously, implementation stops being the center of gravity. Direction becomes the scarce resource.

The question shifts from:

*"Who is going to build this?"*

to:

*"What should exist tomorrow?"*

Human leverage moves into choosing priorities, resolving ambiguity, defining constraints, and expressing intent clearly enough for execution to happen without constant intervention.

The daily isn't shrinking.

It's becoming the interface between human judgment and machine output.

---

*Notes:*

1. The FullSend framework mentioned above: [https://github.com/fullsend-ai/fullsend](https://github.com/fullsend-ai/fullsend) — worth reading as a design document even if you're not adopting it wholesale.
2. Prior post on the flipped development cycle: [Agent Dailies and the Flipped Development Cycle](https://sephib.github.io/agent-dailies-and-the-flipped-development-cycle.html)
3. My current _Go To_ spec driven workflow - [flightctl ai-workflows](https://github.com/flightctl/ai-workflows)
