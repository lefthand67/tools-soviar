import logging
from typing import Dict, Any, List
from apps.cli.collector import UserAnswers
from core.compiler.schemas import SteeringBlock

logger = logging.getLogger(__name__)

class SteeringGenerator:
    """
    Implements the Precision Personalization Contract for T3 Steering blocks.

    This generator transforms raw UserAnswers into a set of hard pedagogical constraints.
    The goal is to move from probabilistic 'personas' to deterministic 'steering markers'.
    
    Markers used:
    - [CONSTRAINT]: A mandatory reasoning rule (e.g., 'Forbidden: jargon').
    - [CONTEXT]: Environmental or identity facts that inform the prompt's local context.
    
    Symmetry Mandate: The constraints generated here must be a direct reflection of the 
    precision captured during the collection phase.
    """

    # Mapping of experience levels to specific pedagogical constraints
    # These constraints enforce the 'Skeptical Mastery' approach based on user level.
    EXPERIENCE_MAP = {
        "absolute beginner": [
            "[CONSTRAINT]: Use 'Reductive Bridge' for all new concepts.",
            "[CONSTRAINT]: Forbidden: jargon without immediate trivial examples.",
            "[CONSTRAINT]: Prioritize conceptual intuition over formal notation."
        ],
        "self-taught enthusiast": [
            "[CONSTRAINT]: Focus on filling 'knowledge gaps' and correcting misconceptions.",
            "[CONSTRAINT]: Use 'First-Principles Resets' when errors are detected.",
            "[CONSTRAINT]: Balance practical application with theoretical rigor."
        ],
        "professional": [
            "[CONSTRAINT]: Prioritize industrial-grade patterns over academic theory.",
            "[CONSTRAINT]: Focus on 'Trade-offs', 'Complexity Analysis', and 'Edge Cases'.",
            "[CONSTRAINT]: Use high-density technical language; skip introductory fluff."
        ]
    }

    # Mapping of learning goals to steering constraints
    # These constraints align the 'Scribe Ledger' requirements with user intent.
    GOAL_MAP = {
        "broad theoretical overview": [
            "[CONSTRAINT]: Prioritize breadth over depth.",
            "[CONSTRAINT]: Map connections between different sub-domains.",
            "[CONSTRAINT]: Use high-level analogies to explain complex systems."
        ],
        "practical how-to skills": [
            "[CONSTRAINT]: Prioritize 'Implementation' over 'Theory'.",
            "[CONSTRAINT]: Every concept must be followed by a concrete task.",
            "[CONSTRAINT]: Focus on tool-chain proficiency and workflow efficiency."
        ],
        "deep expert-level mastery": [
            "[CONSTRAINT]: Prioritize depth and rigorous proof.",
            "[CONSTRAINT]: Challenge the student with adversarial edge cases.",
            "[CONSTRAINT]: Require formal verification of all core ALOs."
        ]
    }

    def generate_steering_block(self, answers: UserAnswers) -> SteeringBlock:
        """
        Transforms UserAnswers into a T3 SteeringBlock.

        Logic:
        1. Maps experience level to constrained pedagogy (Skeptical Mastery).
        2. Maps learning goals to specific evidence-based requirements.
        3. Inject strategy-specific markers (e.g., High-Density mode for TIME-BOXED).
        4. Captures environment as local [CONTEXT].

        Returns:
            SteeringBlock: A validated contract containing constraints and user context.
        """
        logger.info("Generating T3 steering block for user: %s", answers.experience_level)

        constraints = []

        # 1. Resolve Experience Constraints
        exp_key = answers.experience_level.lower()
        for key, value in self.EXPERIENCE_MAP.items():
            if key in exp_key or exp_key in key:
                constraints.extend(value)
                break
        else:
            logger.warning("No experience map match for: %s", exp_key)

        # 2. Resolve Goal Constraints
        goal_key = answers.learning_goals.lower()
        for key, value in self.GOAL_MAP.items():
            if key in goal_key or goal_key in key:
                constraints.extend(value)
                break
        else:
            logger.warning("No goal map match for: %s", goal_key)

        # 3. Handle Time Constraints
        if "TIME-BOXED" in answers.strategy:
            constraints.append("[CONSTRAINT]: Implement 'High-Density' mode. Skip redundant introductions; move directly to evidence-based verification.")

        # 4. Environment/Tooling context
        if answers.environment:
            constraints.append(f"[CONTEXT]: User is working in environment: {answers.environment}")

        # Create and validate the final T3 block structure using the contract
        return SteeringBlock(
            steering_constraints=constraints,
            user_context={
                "experience": answers.experience_level,
                "goals": answers.learning_goals,
                "strategy": answers.strategy
            }
        )
