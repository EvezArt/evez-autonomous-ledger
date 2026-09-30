"""Canonical EVEZ event v1 contract and hashing.

Dependency-light implementation of evez.event.v1.
Uses only Pydantic and Python stdlib.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

SCHEMA_VERSION = "evez.event.v1"


class Source(BaseModel):
    """Event origin."""
    model_config = ConfigDict(extra="forbid")
    repo: str = Field(min_length=1)
    service: str = Field(min_length=1)
    agent: str | None = None


class Subject(BaseModel):
    """What the event is about."""
    model_config = ConfigDict(extra="forbid")
    kind: str = Field(min_length=1)
    id: str = Field(min_length=1)


class Trace(BaseModel):
    """Causal and correlation context."""
    model_config = ConfigDict(extra="forbid")
    run_id: str = Field(min_length=1)
    parent_event_id: str | None = None
    correlation_id: str = Field(min_length=1)


class Policy(BaseModel):
    """Action policy and capability requirements."""
    model_config = ConfigDict(extra="forbid")
    required_capabilities: list[str] = Field(default_factory=list)
    risk: Literal["low", "medium", "high", "critical"] = "low"
    human_approval: bool = False


class Integrity(BaseModel):
    """Hash chain and verification."""
    model_config = ConfigDict(extra="forbid")
    prev_hash: str | None = None
    event_hash: str | None = None


class Event(BaseModel):
    """Canonical EVEZ event."""
    model_config = ConfigDict(extra="forbid")
    event_id: str = Field(min_length=1)
    event_type: str = Field(pattern=r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)+$")
    schema_version: Literal[SCHEMA_VERSION] = SCHEMA_VERSION
    ts: datetime
    source: Source
    subject: Subject
    trace: Trace
    payload: dict[str, Any] = Field(default_factory=dict)
    policy: Policy = Field(default_factory=Policy)
    integrity: Integrity = Field(default_factory=Integrity)

    @field_validator("ts")
    @classmethod
    def require_utc_timezone(cls, value: datetime) -> datetime:
        """Require all timestamps to be timezone-aware."""
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("ts must include timezone information")
        return value.astimezone(timezone.utc)

    def unsigned_dict(self) -> dict[str, Any]:
        """Produce canonical form without event_hash for signing."""
        value = self.model_dump(mode="json")
        value["integrity"]["event_hash"] = None
        return value

    def canonical_bytes(self) -> bytes:
        """Produce deterministic bytes for hashing.
        
        Uses:
        - Sorted keys
        - Compact separators
        - UTF-8 encoding
        - No pretty-printing
        """
        return json.dumps(
            self.unsigned_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")

    def computed_hash(self) -> str:
        """Compute SHA-256 hash of canonical form."""
        digest = hashlib.sha256(self.canonical_bytes()).hexdigest()
        return f"sha256:{digest}"

    def seal(self, previous_hash: str | None = None) -> Event:
        """Seal the event with hash-chain link and event hash.
        
        Args:
            previous_hash: Hash of the previous event in the chain.
            
        Returns:
            Self (for chaining).
        """
        self.integrity.prev_hash = previous_hash
        self.integrity.event_hash = self.computed_hash()
        return self

    def verify(self) -> bool:
        """Verify event integrity.
        
        Returns:
            True if event_hash matches the computed hash of the canonical form.
        """
        if self.integrity.event_hash is None:
            return False
        expected = self.integrity.event_hash
        computed = self.computed_hash()
        return expected == computed

    def to_jsonl(self) -> str:
        """Serialize to JSON Lines format."""
        return self.model_dump_json()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Event:
        """Deserialize from dict."""
        return cls.model_validate(data)

    @classmethod
    def from_json(cls, text: str) -> Event:
        """Deserialize from JSON or JSON Lines."""
        return cls.model_validate_json(text)


class ActionReceipt(BaseModel):
    """Receipt for an executed action."""
    model_config = ConfigDict(extra="forbid")
    action_id: str = Field(min_length=1)
    event_id: str = Field(min_length=1)
    tool: str = Field(min_length=1)
    status: Literal["approved", "denied", "executed", "failed"]
    capabilities: list[str] = Field(default_factory=list)
    approval_id: str | None = None
    output_hash: str | None = None
    error: str | None = None
    side_effects: list[str] = Field(default_factory=list)

    def to_event(
        self,
        run_id: str,
        source: Source,
        correlation_id: str,
        prev_hash: str | None = None,
    ) -> Event:
        """Convert receipt to event for ledger storage."""
        return Event(
            event_id=self.action_id,
            event_type="action.receipt",
            ts=datetime.now(timezone.utc),
            source=source,
            subject=Subject(kind="action", id=self.action_id),
            trace=Trace(
                run_id=run_id,
                correlation_id=correlation_id,
                parent_event_id=self.event_id,
            ),
            payload=self.model_dump(exclude_none=True),
            policy=Policy(required_capabilities=[], risk="low", human_approval=False),
        ).seal(prev_hash)
