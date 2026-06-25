---
Title: Mixed Traffic: When Agentic and Traditional Teams Share the Same Road
Date: 2026-06-21
Author: Sephi Berry
Category: posts, agentic sdlc, agentic engineering
status: draft
Summary: The friction between agentic and traditional developers isn't a culture problem. It's an infrastructure problem — and the autonomous car analogy shows exactly why.
---

Two lanes of traffic. One side: autonomous vehicles making thousands of micro-optimizations per second, adjusting following distance, anticipating merges, coordinating silently with each other. The other side: human drivers doing what human drivers do — checking mirrors, making judgment calls, occasionally hesitating at a yellow light.

Then they merge.

Not catastrophically. Just — awkwardly. Inefficiently. With friction that neither driver expected and the road didn't account for.

This is what's happening inside engineering teams right now. Some developers are running agents overnight, opening PRs by morning, and operating in an async, intent-driven workflow. Others are working in the familiar cadence of human-paced implementation. The "road" — your processes, rituals, and tooling — was built for one type of traffic. It's now carrying both. Nobody designed it that way. It just happened.

---

# The Road Wasn't Built for Both

Traffic infrastructure works because it was designed around a single baseline: human reaction time. Signal timing, lane widths, yield conventions, merge geometry — all of it assumes a human at the wheel, reacting to inputs within a human window. It works well for one vehicle profile. Reasonably well for a second. It was never stress-tested for both simultaneously at scale.

Autonomous vehicles aren't wrong. Human drivers aren't wrong. The road was optimized for one profile — and running both simultaneously surfaces design assumptions that were always baked in but never visible when everyone used the same vehicle.

The software development equivalent: standups, sprint retros, PR review SLAs, code ownership conventions, deployment  cycles. These weren't designed by accident. They were designed thoughtfully, for a specific mode of working — one that assumed humans are the unit of implementation. That work arrives in human-sized chunks. That the developer who opens a PR spent the preceding week writing it.

---

# Where the Friction Shows Up

**Review cadence is traffic signal timing calibrated for human reaction speeds.** An agentic developer opening eight PRs from a single overnight run hits a structural bottleneck: review SLAs calibrated for one or two PRs per developer per day. The signal timing is wrong for the throughput. The bottleneck isn't the reviewer's capability — it's that the process doesn't account for burst volume.

**Sprint rituals are rules written before autonomous vehicles existed.** Standups, story point estimation, sprint planning — these make sense when implementation is the human's primary contribution. They create overhead when agents are doing the implementation and humans are steering. Estimating a ticket the agent will complete overnight, in a ceremony that assumes the estimating human will do the work, is the software equivalent of running a human-driver road test on a self-driving car.

**PR size conventions are lane discipline.** "Keep PRs small" is reviewer advice — it exists because human reviewers struggle with large diffs. Agent-generated PRs may be larger but internally coherent: a complete feature, properly tested, logically structured. Applying the "small PR" rule to agent output is applying lane-width rules designed for one vehicle to something with different geometry.

**Deployment gates are intersection right-of-way.** Who has authority to merge? What triggers a release? These rules assume a human made a traceable judgment call at each step. When an agent authors the commit, the accountability model gets complicated. The right-of-way rules don't fully resolve.

---

# The Convoy Problem

A convoy moves at the speed of the slowest vehicle.

This is the underappreciated consequence of mixed-traffic teams. When a shared process exists — PR review, sprint ceremonies, release approval — its throughput is constrained by the participant for whom that process creates the most friction. The process becomes a shared resource. Shared resources get optimized for their modal user, not their edge cases.

If your PR review process is calibrated for human pace, the agentic developer's overnight output queues behind it. The process worked exactly as designed. It just wasn't designed for that volume.

Neither participant is wrong. The convoy problem isn't caused by bad drivers — it's caused by applying a shared speed constraint to vehicles with different performance profiles. The constraint is the design choice that creates the friction. Pointing at the cars doesn't fix the road.

---

# What Mixed-Traffic Infrastructure Actually Looks Like

The wrong conclusion is "everyone should go agentic." Mixed traffic is the reality. The question is how to design infrastructure that serves both modes without forcing either one to pretend it's the other.

**Adaptive signals.** Review processes that flex on PR origin and risk level, not a uniform SLA applied to everything. An agent-generated PR with high test coverage and narrow scope is a different review problem than a complex human-authored architectural change. Review automation — CODEOWNERS, CI gating, coverage thresholds — can serve as the adaptive layer for low-risk, high-confidence PRs without removing human judgment from high-stakes ones.

**Separated lanes where useful.** Not all workflows need to be shared. A fast path for agent-generated, low-risk, high-coverage changes can coexist with a standard lane for human-authored, higher-complexity work. Different vehicle profiles, different lanes.

**Redesigned shared intersections.** Some workflows must involve both modes: planning sessions, design reviews, incident response. These need to be redesigned explicitly for mixed participation, not defaulted to either style.

**Infrastructure investment.** Mixed-traffic roads require more sophisticated signaling, not less. Mixed-mode teams need explicit tooling investment: better async communication, clearer escalation paths, shared observability of what agents are doing between standups. That's not a cultural ask — it's an engineering one.

---

# The Road Ahead

The road ahead has both types of vehicles on it — and that's not a temporary state. It's the medium-term reality for most engineering teams.

The friction isn't a symptom of a culture problem. It's the reality most teams are living with right now — and it rewards whoever addresses it first.
