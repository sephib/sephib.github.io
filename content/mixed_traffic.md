---
Title: Mixed Traffic: When Agentic and Traditional Teams Share the Same Road
Date: 2026-06-21
Author: Sephi Berry
Category: posts
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

The software development equivalent: standups, sprint cadence, PR review SLAs, code ownership conventions, deployment authority chains. These weren't designed by accident. They were designed thoughtfully, for a specific mode of working — one that assumed humans are the unit of implementation. That work arrives in human-sized chunks. That the developer who opens a PR spent the preceding week writing it.

Those assumptions are no longer universal. And the friction that follows isn't a sign that someone is working wrong. It's a sign that the infrastructure has a design gap.

---

# Where the Friction Shows Up

The friction is real and specific. It shows up in the same places on every mixed team.

**Review cadence is traffic signal timing calibrated for human reaction speeds.** Signals are timed for the gap between green and the next car clearing an intersection. An agentic developer opening eight PRs from a single overnight run hits a structural bottleneck: review SLAs calibrated for one or two PRs per developer per day. The signal timing is wrong for the throughput. PRs queue. The agentic developer waits. The bottleneck isn't the reviewer's capability — it's that the process doesn't account for burst volume.

**Sprint rituals are rules written before autonomous vehicles existed.** Standups, story point estimation, sprint planning — these make sense when implementation is the human's primary contribution. They create overhead when agents are doing the implementation and humans are steering. Estimating a ticket the agent will complete overnight, in a ceremony that assumes the estimating human will do the work, is the software equivalent of running a human-driver road test on a self-driving car.

**PR size conventions are lane discipline.** "Keep PRs small" is reviewer advice — it exists because human reviewers struggle with large diffs. Agent-generated PRs may be larger but internally coherent: a complete feature, properly tested, logically structured. Applying the "small PR" rule to agent output is applying lane-width rules designed for one vehicle to something with different geometry. The convention doesn't fail because it was bad — it fails because it was written for a different driver.

**Deployment gates are intersection right-of-way.** Who has authority to merge? What triggers a release? These rules assume a human made a traceable judgment call at each step. When an agent authors the commit, the accountability model gets complicated. The right-of-way rules don't fully resolve.

---

# The Convoy Problem

A convoy moves at the speed of the slowest vehicle.

This is the underappreciated consequence of mixed-traffic teams. When a shared process exists — PR review, sprint ceremonies, release approval — its throughput is constrained by the participant for whom that process creates the most friction. The process becomes a shared resource. Shared resources get optimized for their modal user, not their edge cases.

If your PR review process is calibrated for human pace, the agentic developer's overnight output queues behind it. The process worked exactly as designed. It just wasn't designed for that volume.

If your sprint ceremony assumes human implementation cycles, the agentic developer waits while the ritual catches up. The cadence isn't broken — it just doesn't fit both rhythms simultaneously.

Neither participant is wrong. The convoy problem isn't caused by bad drivers — it's caused by applying a shared speed constraint to vehicles with different performance profiles. The constraint is the design choice that creates the friction. Pointing at the cars doesn't fix the road.

---

# What Mixed-Traffic Infrastructure Actually Looks Like

The wrong conclusion is "everyone should go agentic." Mixed traffic is the reality — and probably should be. The question is how to design infrastructure that serves both modes without forcing either one to pretend it's the other.

**Adaptive signals.** Review processes that flex based on PR origin and risk level, not a uniform SLA applied to everything. An agent-generated PR with high test coverage, a narrow scope, and a clean diff is a different review problem than a complex human-authored architectural change. Treating them identically is handing a pedestrian crossing button to a car. Review automation — CODEOWNERS, CI gating, coverage thresholds — can serve as the adaptive layer that changes the signal for low-risk, high-confidence PRs without removing human judgment from high-stakes ones.

**Separated lanes where useful.** Not all workflows need to be shared. A fast path for agent-generated, low-risk, high-coverage changes can coexist with a standard lane for human-authored, higher-complexity work. This isn't hierarchy — it's fit. Different vehicle profiles, different lanes.

**Redesigned shared intersections.** Some workflows must involve both modes: planning sessions, design reviews, incident response. These are the intersections — the places where lanes merge and both types of traffic have to navigate the same space. They need to be redesigned explicitly for mixed participation, not defaulted to either style. The autonomous vehicle and the human driver both need to get through the intersection. Designing for only one doesn't make the other disappear.

**Infrastructure investment.** Mixed-traffic roads require more sophisticated signaling, not less. Mixed-mode teams need explicit tooling investment: better async communication, clearer escalation paths, shared observability of what agents are doing between standups. The signals have to get smarter because the traffic has gotten more complex. That's not a cultural ask — it's an engineering one.

---

# The Question Worth Asking Now

Which of your current processes were designed assuming everyone works the same way?

That question — applied to standups, PR review, sprint cadence, deployment authority, how your team writes and consumes documentation — is where the infrastructure audit starts. In each case: does this process assume a particular mode of working? What breaks when that assumption stops being universal?

Not "should we adopt agentic workflows?" That question will answer itself. The more tractable question is which of your shared processes have implicit single-driver assumptions built in — and what it would take to redesign them for both.

That's a design conversation. Not a culture one.

---

# The Road Ahead

The road ahead has both types of vehicles on it. That's not a temporary state to be resolved once a winning approach is declared — it's the medium-term reality for most engineering teams, and probably the long-term one too. The teams that move faster won't be the ones who pick a winner. They'll be the ones who design infrastructure that works for both simultaneously.

The friction isn't proof that one approach is wrong. It's a design signal.

The problem was never the cars.

It was always the road.
