"""
Domain Resolver — The precision mapping layer for T2 Domain Laws.

As mandated by ADR-26036, the Domain Resolver prevents 'generic' technical laws
by implementing a Match -> Refine -> Architect resolution pipeline.

Resolution Flow:
1. Match: Map the broad topic to a base domain directory (e.g., 'python').
2. Refine: Use subtopics to narrow down the specific technical laws (e.g., 'asyncio.json').
3. Architect: If no match is found, delegate synthesis to the Domain Architect (fallback to 'general').
"""

import json
import logging
from pathlib import Path
from typing import List, Optional
from apps.cli.collector import UserAnswers

logger = logging.getLogger(__name__)


class DomainLawError(RuntimeError):
    """A resolved T2 block is missing, empty, or not a domain-law document.

    Raised instead of returning a path that would compile to `{}`. An empty domain
    law is indistinguishable from no domain law at runtime, so the failure belongs
    at build time, where it can name the file that needs fixing.
    """


class DomainResolver:
    """
    Implements the T2 Domain Resolution logic.

    As mandated by ADR-26036, this resolver prevents 'generic' technical laws
    by implementing a Match -> Refine -> Architect resolution pipeline.
    The goal is to ensure the mentor possesses a high-precision technical 'Law'
    that is mapped directly to the user's topic and subtopics.
    """

    def __init__(self, domains_root: Path):
        """
        Initialize the resolver with the path to the domain library.

        Args:
            domains_root (Path): Absolute path to the templates/domains/ directory.
        """
        self.domains_root = domains_root

    def resolve(self, answers: UserAnswers) -> List[str]:
        """
        Resolves the T2 blocks based on the Precision Personalization Contract.

        Resolution Flow:
        1. Match: Map the broad topic to a base domain directory (e.g., 'python').
        2. Refine: Use subtopics to narrow the focus (e.g., 'asyncio.json').
        3. Architect: Fallback to a 'general' domain or delegate to a synthesis agent.

        Args:
            answers (UserAnswers): The collected user answers containing topic and subtopics.

        Returns:
            List[str]: A list of relative paths to the resolved Domain Blocks.

        Raises:
            DomainLawError: If resolution yields no block, or a block that is empty
            or not a domain-law document. A project is never provisioned with an
            unenforceable technical law.
        """
        topic = answers.topic.strip().lower()
        logger.info("Resolving T2 domain blocks for topic: %s", topic)

        # 1. Match: Find the base domain slug
        domain_slug = self._match(topic)

        if not domain_slug:
            # 3. Architect: Handle unknown domains
            blocks = self._architect(topic)
        else:
            # 2. Refine: Use subtopics to narrow the focus
            blocks = self._refine(domain_slug, answers.subtopics)

        self._validate(blocks, topic)
        return blocks

    def _match(self, topic: str) -> Optional[str]:
        """
        Tries to find a matching domain directory in templates/domains/.

        Contract:
        - Must return the exact directory name if it exists (case-insensitive).
        - Returns None if no directory matches the topic.

        Args:
            topic (str): The lower-case topic string to match.

        Returns:
            Optional[str]: The matched directory name if found, otherwise None.
        """
        # 1. Try exact match first (fast path)
        domain_path = self.domains_root / topic
        if domain_path.is_dir():
            logger.info("Exact domain match found: %s", topic)
            return topic

        # 2. Case-insensitive search (fallback for Linux)
        try:
            for entry in self.domains_root.iterdir():
                if entry.is_dir() and entry.name.lower() == topic:
                    logger.info("Case-insensitive domain match found: %s (as %s)", topic, entry.name)
                    return entry.name
        except OSError as e:
            logger.error("Error accessing domains root: %s", e)

        return None

    def _refine(self, domain_slug: str, subtopics: Optional[str]) -> List[str]:
        """
        Refines the base domain block set using subtopics.

        Logic:
        - If no subtopics, return all .json files in the domain directory (standard base).
        - If subtopics are provided, try to find matching .json files for each subtopic.
        - If specific subtopic blocks are found, they take precedence over 'core.json'.

        Args:
            domain_slug (str): The matched domain directory name.
            subtopics (Optional[str]): A comma-separated string of subtopics.

        Returns:
            List[str]: A list of relative paths to the refined Domain Blocks.
        """
        domain_path = self.domains_root / domain_slug

        if not subtopics:
            return self._get_all_json_files(domain_path, domain_slug)

        normalized_subtopics = [s.strip().lower() for s in subtopics.split(",")]
        refined_blocks = []

        for sub in normalized_subtopics:
            sub_file = domain_path / f"{sub}.json"
            if sub_file.exists():
                logger.info("Refinement match: %s/%s.json", domain_slug, sub)
                refined_blocks.append(f"{domain_slug}/{sub}.json")

        if refined_blocks:
            return refined_blocks

        # Fallback to base domain if no subtopic matches
        logger.info("No subtopic refinement possible for %s, using base blocks.", domain_slug)
        return self._get_all_json_files(domain_path, domain_slug)

    def _architect(self, topic: str) -> List[str]:
        """
        Handles the 'Architect' path when no domain is found.

        In a fully agentic system, this would trigger the DomainArchitectAgent
        to synthesize a new domain block. Until then it falls back to the
        'general' domain, whose law is a real, enforceable block.

        Contract:
        - Must return the 'general' domain blocks.
        - Raises DomainLawError if 'general' is missing: falling back to nothing
          would provision a mentor with no technical law at all.

        Args:
            topic (str): The topic that failed to match any existing domain.

        Returns:
            List[str]: Relative paths to the 'general' domain blocks.

        Raises:
            DomainLawError: If the 'general' fallback domain is absent.
        """
        logger.warning("No domain match for '%s'. Triggering Architect path (fallback to general).", topic)

        fallback_path = self.domains_root / "general"
        if fallback_path.is_dir():
            return self._get_all_json_files(fallback_path, "general")

        raise DomainLawError(
            f"Domain match failed for topic '{topic}' and no 'general' fallback exists "
            f"at {fallback_path}. Refusing to provision a mentor with no domain law."
        )

    def _validate(self, blocks: List[str], topic: str) -> None:
        """
        Verifies that every resolved block is a usable domain-law document.

        A zero-byte or `{}` block compiles to nothing and is undetectable at
        runtime, so it is rejected here, at build time.

        Args:
            blocks (List[str]): Relative block paths returned by resolution.
            topic (str): The topic being resolved, for the error message.

        Raises:
            DomainLawError: If the list is empty, a file is missing or unreadable,
            or the document carries no technical constraints or success criteria.
        """
        if not blocks:
            raise DomainLawError(
                f"Resolution for topic '{topic}' produced no domain blocks. "
                f"Every project requires a technical law."
            )

        for relative in blocks:
            path = self.domains_root / relative
            try:
                raw = path.read_text(encoding="utf-8")
            except OSError as exc:
                raise DomainLawError(
                    f"Domain block '{relative}' resolved for topic '{topic}' is unreadable: {exc}"
                ) from exc

            if not raw.strip():
                raise DomainLawError(
                    f"Domain block '{relative}' resolved for topic '{topic}' is empty. "
                    f"An empty law compiles to no law; fill it in."
                )

            try:
                data = json.loads(raw)
            except ValueError as exc:
                raise DomainLawError(
                    f"Domain block '{relative}' resolved for topic '{topic}' is not valid JSON: {exc}"
                ) from exc

            if not isinstance(data, dict):
                raise DomainLawError(
                    f"Domain block '{relative}' resolved for topic '{topic}' is a "
                    f"{type(data).__name__}, not a domain-law object."
                )

            missing = [
                key
                for key in ("technical_constraints", "success_criteria")
                if not data.get(key)
            ]
            if missing:
                raise DomainLawError(
                    f"Domain block '{relative}' resolved for topic '{topic}' lacks {missing}. "
                    f"A domain law needs both a constraint list and success criteria."
                )

    def _get_all_json_files(self, path: Path, domain_slug: str) -> List[str]:
        """
        Returns all .json files in a directory relative to the domains root.

        Args:
            path (Path): Absolute path to the domain directory.
            domain_slug (str): The name of the domain directory.

        Returns:
            List[str]: A list of relative paths (e.g., 'python/core.json').
        """
        return [f"{domain_slug}/{f.name}" for f in path.glob("*.json")]
