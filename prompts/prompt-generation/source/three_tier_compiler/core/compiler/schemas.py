"""
Block Schemas for the Industrial Block Compiler.

These schemas ensure that all T1, T2, and T3 blocks adhere to the 
Deterministic Pedagogical Contract (ADR-26024).
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field

class BlockContract(BaseModel):
    """
    The base contract for any pedagogical block.
    Blocks can contain arbitrary keys, but must be valid JSON.
    """
    # We allow extra fields because blocks are domain-specific
    model_config = {"extra": "allow"}

class IdentityBlock(BlockContract):
    """Schema for T1 Identity blocks."""
    law: Dict[str, Any] = Field(..., description="The core pedagogical laws of the mentor")
    toolset: Dict[str, Any] = Field(..., description="The set of cognitive tools available")
    hierarchy_of_authority: Dict[str, Any] = Field(..., description="Priority order of constraints")

class DomainBlock(BlockContract):
    """Schema for T2 Domain blocks."""
    technical_constraints: Union[Dict[str, Any], List[Any]] = Field(..., description="Domain-specific hardware/software constraints")
    success_criteria: Union[Dict[str, Any], List[Any]] = Field(..., description="What constitutes mastery in this domain")

class ProbeResponse(BaseModel):
    """Contract for the Hybrid Probing Strategy LLM output.

    Determines if the current user answers are sufficient for high-precision
    personalization or if a follow-up probe is required.
    """
    decision: str = Field(..., description="Either 'SUFFICIENT' or 'PROBE'")
    question: Optional[str] = Field(None, description="The follow-up question to ask the user")
    reasoning: str = Field(..., description="Internal reasoning for the decision")
    target_field: Optional[str] = Field(None, description="The UserAnswers field to update with the response")

class SteeringBlock(BaseModel):
    """
    The T3 Steering Block Contract.
    
    This block transforms user-specific attributes into high-precision pedagogical 
    constraints. Unlike T1/T2 blocks, which define 'How to teach' and 'What to teach', 
    the Steering Block defines 'Who is being taught' and the resulting constraints 
    on the delivery (e.g., jargon limits, pacing, and verification rigor).
    """
    steering_constraints: List[str] = Field(
        ..., 
        description="List of [CONSTRAINT] and [CONTEXT] markers that steer the LLM's reasoning."
    )
    user_context: Dict[str, Any] = Field(
        ..., 
        description="Raw user attributes used for traceability and RAM updates."
    )
