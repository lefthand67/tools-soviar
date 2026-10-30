import json
import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Set

from core.compiler.schemas import BlockContract, IdentityBlock, DomainBlock
from core.compiler.yaml_stream import render_yaml_stream, strip_noise

logger = logging.getLogger(__name__)

class ThreeTierCompiler:
    """
    The ThreeTierCompiler implements the 'Deterministic Pedagogical Compiler' logic.

    Motivation: To eliminate 'Prompt Drift', we separate pedagogy (T1), technical laws (T2),
    and local context (T3). This compiler recursively resolves a manifest and its
    dependencies (Blocks) into a single, high-precision system prompt.

    Architecture (ADR-26015): SSoT Hub (Blocks) -> Manifest -> Compiled Prompt.
    """

    def __init__(self, t1_path: str, t2_path: str, noise_chars: List[str] = None):
        """
        Initialize the compiler with paths to the Universal and Domain libraries.

        Args:
            t1_path (str): Absolute path to the Tier 1 (Universal) block library.
            t2_path (str): Absolute path to the Tier 2 (Domain) block library.
            noise_chars (List[str], optional): Characters to strip from the final output. 
                Defaults to ['"', '`', "'"].
        """
        self.t1_path = Path(t1_path)
        self.t2_path = Path(t2_path)
        self.noise_chars = noise_chars or ['"', '`', "'"]

    def _validate_block(self, data: Dict[str, Any], path: Path) -> None:
        """
        Performs structural validation on a block based on its content.
        
        Logic:
        - Recursively check for patterns that match IdentityBlock or DomainBlock.
        - If a dict contains 'law' and 'toolset', it MUST be a valid IdentityBlock.
        - If a dict contains 'technical_constraints', it MUST be a valid DomainBlock.

        Args:
            data (Dict[str, Any]): The JSON content of the block to validate.
            path (Path): Path to the block file for error reporting.

        Raises:
            ValueError: If the block violates the structural contract for 
                IdentityBlock or DomainBlock.
        """
        def validate_recursive(item: Any):
            if not isinstance(item, dict):
                return

            # Check if this specific dict looks like an Identity Block
            if "law" in item and "toolset" in item:
                try:
                    IdentityBlock(**item)
                except Exception as e:
                    raise ValueError(f"Malformed Identity Block: {e}")
            
            # Check if this specific dict looks like a Domain Block
            if "technical_constraints" in item:
                try:
                    DomainBlock(**item)
                except Exception as e:
                    raise ValueError(f"Malformed Domain Block: {e}")

            # Recurse into values to find wrapped blocks
            for val in item.values():
                validate_recursive(val)

        try:
            validate_recursive(data)
        except ValueError as e:
            raise ValueError(f"Block structural validation failed for {path}: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected validation error for {path}: {e}")

    def _resolve_recursive(self, file_path: Path, visited: Set[Path] = None, allowed_roots: Set[Path] = None) -> Dict[str, Any]:
        """
        Recursively resolves '_includes' in JSON blocks to build the final merged state.

        Args:
            file_path (Path): The path to the JSON block to resolve.
            visited (Set[Path], optional): Set of already visited paths to detect 
                circular dependencies.
            allowed_roots (Set[Path], optional): Set of trusted root directories 
                to prevent path traversal attacks.

        Returns:
            Dict[str, Any]: The fully resolved and merged block data.

        Raises:
            RecursionError: If a circular dependency is detected.
            PermissionError: If the resolved path is outside of all allowed roots.
            FileNotFoundError: If the block file does not exist.
            json.JSONDecodeError: If the block contains malformed JSON.
            ValueError: If the block fails structural validation.
        """
        if visited is None:
            visited = set()

        abs_path = file_path.resolve()
        if abs_path in visited:
            raise RecursionError(f"Circular dependency detected: {abs_path}")

        # --- Path Traversal Protection ---
        if allowed_roots:
            is_allowed = any(abs_path.is_relative_to(root.resolve()) for root in allowed_roots)
            if not is_allowed:
                raise PermissionError(f"Security violation: Block path {abs_path} is outside of all allowed directories {allowed_roots}")

        visited.add(abs_path)

        if not abs_path.exists():
            raise FileNotFoundError(f"Block file not found: {abs_path}")

        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                logger.warning("Block file is empty: %s. Treating as empty dictionary.", abs_path)
                data = {}
            else:
                data = json.loads(content)

        # --- Structural Validation ---
        self._validate_block(data, abs_path)

        merged_data = {}

        # 1. Process includes first (The Base Layers)
        if "_includes" in data:
            for include_rel_path in data["_includes"]:
                # Resolve relative to the current block's directory
                include_path = (abs_path.parent / include_rel_path).resolve()
                included_content = self._resolve_recursive(include_path, visited.copy(), allowed_roots=allowed_roots)

                # Traceability: Log the merge
                overwritten_keys = [k for k in included_content if k in merged_data]
                logger.debug("[MERGE] %s -> %s (Overwrote: %s)",
                             include_rel_path, abs_path.name, overwritten_keys)

                merged_data.update(included_content)
            del data["_includes"]
        # 2. Current block overrides includes (The Specific Layer)
        overwritten_by_self = [k for k in data if k in merged_data]
        logger.debug("[MERGE] Base -> %s (Overwrote: %s)", abs_path.name, overwritten_by_self)
        
        merged_data.update(data)
        return merged_data

    def compile_prompt(self, manifest: Dict[str, Any], t3_path: str = None, in_memory_overrides: Dict[str, Any] = None) -> str:
        """
        Performs the Three-Tier Merge:
        1. Resolves the manifest (and its recursive blocks).
        2. Merges T1 (Universal) and T2 (Domain) law fragments.
        3. Applies T3 (Project) overrides from disk and/or in-memory.
        4. Formats the result into a noise-stripped YAML-like stream.

        Symmetry Mandate:
        The output must be a perfect reflection of the manifest's resolution state.
        T3 overrides (including in-memory steering) MUST have the final word,
        overriding any contradictory instructions in T1 or T2.

        Args:
            manifest (Dict[str, Any]): The project manifest defining T1, T2, and T3 blocks.
            t3_path (str, optional): Absolute path to the Tier 3 project directory.
            in_memory_overrides (Dict[str, Any], optional): High-priority runtime overrides.

        Returns:
            str: The final compiled system prompt as a YAML-like stream.

        Raises:
            RecursionError: If circular dependencies exist in blocks.
            PermissionError: If blocks are accessed outside allowed roots.
            FileNotFoundError: If manifest-defined blocks are missing.
        """
        final_state = {}
        allowed_roots = {self.t1_path, self.t2_path}

        # Resolve T1 Blocks
        for block_name in manifest.get("t1", []):
            path = self.t1_path / block_name
            final_state.update(self._resolve_recursive(path, allowed_roots=allowed_roots))

        # Resolve T2 Blocks
        for block_name in manifest.get("t2", []):
            # If block_name contains a slash (e.g. 'computing/core.json'),
            # it's relative to the t2_path.
            path = self.t2_path / block_name
            final_state.update(self._resolve_recursive(path, allowed_roots=allowed_roots))

        # Resolve T3 Overrides from Disk
        if t3_path:
            t3_root = Path(t3_path)
            allowed_roots.add(t3_root)
            override_filename = manifest.get("t3", "overrides.json")
            override_path = t3_root / override_filename
            if override_path.exists():
                final_state.update(self._resolve_recursive(override_path, allowed_roots=allowed_roots))

        # Apply In-Memory T3 Overrides (Highest Priority)
        if in_memory_overrides:
            final_state.update(in_memory_overrides)

        # Convert the merged state into the final prompt stream
        return self.to_yaml_stream(final_state)

    def to_yaml_stream(self, data: Any, indent_level: int = 0) -> str:
        """
        Converts merged JSON data to a YAML-like stream for the LLM.

        Delegates to the canonical renderer in `core.compiler.yaml_stream` so the
        compiler and the blueprint loader cannot drift in output format.

        Args:
            data (Any): The data structure to convert (Dict, List, or Scalar).
            indent_level (int): Current indentation level for recursive calls.

        Returns:
            str: A string representation of the data in YAML-like format.
        """
        return render_yaml_stream(data, self.noise_chars, indent_level)

    def _strip_noise(self, text: str) -> str:
        """
        Strips noise characters to prevent LLM 'description mode'.

        Args:
            text (str): The input text to clean.

        Returns:
            str: Text with all characters in `self.noise_chars` removed.
        """
        return strip_noise(text, self.noise_chars)
