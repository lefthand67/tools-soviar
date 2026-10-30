---
name: rdd-business-requirements
description: Guides the creation of Business Requirements (BR) for new features. Focuses on user intent, business value, and high-level success criteria.
---

# PROTOCOL: Business Requirements Engineering

## [STATE: INITIALIZATION]
- **Action:** Determine the current date (`YYYYMMDD`) and the feature `<slug>`.
- **Directory Setup:** Create the feature bundle root: `docs/requirements/features/<YYYYMMDD>_<slug>/`.
- **Infrastructure:** 
  1. Create `docs/requirements/features/<YYYYMMDD>_<slug>/context.md`.
  2. Create `docs/requirements/features/<YYYYMMDD>_<slug>/br/`.
- **Artifacts:** Initialize `elicitation.md` (for raw Q&A) and `br.md` within the `br/` folder.

## [STATE: ELICITATION]
- **Action:** Conduct a clarification interview with the user.
- **Recording:** Log all questions and answers in `docs/requirements/features/<YYYYMMDD>_<slug>/br/elicitation.md`.
- **Goal:** Extract the "True Intent" and identify hidden constraints.

## [STATE: DRAFTING]
- **Artifact:** `docs/requirements/features/<YYYYMMDD>_<slug>/br/br.md`
- **Template:**
  - **Feature Name:** <Name>
  - **User Story:** "As a [role], I want to [action] so that [value]."
  - **Business Value & Rationale:** Why is this important?
  - **Impact of Non-Fulfillment:** Consequences of ignoring this requirement.
  - **Success Criteria (SMART):** Specific, Measurable, Achievable, Relevant, Time-bound.
  - **Stakeholders:** Who is impacted?
  - **Out of Scope:** Explicit boundaries.

## [STATE: REVIEW_GATE]
- **Action:** Dispatch Review Subagent.
- **Context:** `[elicitation.md, br.md]`
- **Review-Criteria:** Does the BR perfectly encapsulate the intent found in the elicitation? Are criteria SMART?
- **Sign-off:** Save the verdict in `docs/requirements/features/<YYYYMMDD>_<slug>/br/review.md`.

## [TRANSITION]
Proceed to `rdd-functional-requirements` using the same `<YYYYMMDD>_<slug>` directory.
