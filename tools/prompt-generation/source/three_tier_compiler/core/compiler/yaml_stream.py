"""Canonical renderer for compiled prompt streams.

ADR-26007 ("Format is Architecture") mandates that compiled output is a YAML-like
stream, not raw JSON: structural noise such as quotes and backticks is stripped so
the model reads constraints rather than markup.

This module is the single implementation of that rendering rule. Both the
Three-Tier compiler and the blueprint loader delegate here, so the format cannot
drift between the two project formats the Warehouse serves.
"""

from __future__ import annotations

from typing import Any, List

DEFAULT_NOISE_CHARS: List[str] = ['"', "`", "'"]


def strip_noise(text: str, noise_chars: List[str]) -> str:
    """Remove format-noise characters from a scalar value.

    Args:
        text (str): The scalar to clean.
        noise_chars (List[str]): Characters to delete (e.g. quotes, backticks).

    Returns:
        str: The cleaned text.
    """
    for char in noise_chars:
        text = text.replace(char, "")
    return text


def render_yaml_stream(data: Any, noise_chars: List[str] | None = None, indent_level: int = 0) -> str:
    """Render a nested structure as a noise-stripped YAML-like stream.

    Args:
        data (Any): The structure to render (dict, list, or scalar).
        noise_chars (List[str], optional): Characters to strip. Defaults to
            quotes and backticks.
        indent_level (int, optional): Current indentation depth.

    Returns:
        str: The rendered stream. Empty lines are removed.
    """
    noise = DEFAULT_NOISE_CHARS if noise_chars is None else noise_chars
    indent = "  " * indent_level
    lines: List[str] = []

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{indent}{key}:")
                lines.append(render_yaml_stream(value, noise, indent_level + 1))
            else:
                lines.append(f"{indent}{key}: {strip_noise(str(value), noise)}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{indent}-")
                lines.append(render_yaml_stream(item, noise, indent_level + 1))
            else:
                lines.append(f"{indent}- {strip_noise(str(item), noise)}")
    else:
        return f"{indent}{strip_noise(str(data), noise)}"

    return "\n".join(filter(None, lines))
