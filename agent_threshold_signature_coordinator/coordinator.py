"""Core Threshold Signature Coordinator implementation."""
import hmac
import hashlib
import time
from typing import Dict, Set, List, Any, Optional


class ActionProposal:
    def __init__(self, action_id: str, tool_name: str, payload: Dict[str, Any], required_signatures: int):
        self.action_id = action_id
        self.tool_name = tool_name
        self.payload = payload
        self.required_signatures = required_signatures
        self.signatures: Dict[str, str] = {}
        self.is_approved = False

    @property
    def payload_digest(self) -> str:
        s = f"{self.tool_name}:{self.payload}"
        return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


class ThresholdSignatureCoordinator:
    def __init__(self, authorized_keys: Dict[str, str]):
        self.authorized_keys = authorized_keys  # agent_id -> secret_key
        self._proposals: Dict[str, ActionProposal] = {}

    def create_proposal(self, action_id: str, tool_name: str, payload: Dict[str, Any], required_signatures: int) -> ActionProposal:
        proposal = ActionProposal(action_id, tool_name, payload, required_signatures)
        self._proposals[action_id] = proposal
        return proposal

    def sign_proposal(self, action_id: str, agent_id: str) -> Dict[str, Any]:
        if action_id not in self._proposals:
            raise KeyError("Proposal not found")
        if agent_id not in self.authorized_keys:
            raise PermissionError("Signer not authorized")

        p = self._proposals[action_id]
        key = self.authorized_keys[agent_id]
        sig = hmac.new(key.encode("utf-8"), p.payload_digest.encode("utf-8"), hashlib.sha256).hexdigest()
        p.signatures[agent_id] = sig

        if len(p.signatures) >= p.required_signatures:
            p.is_approved = True

        return {
            "action_id": action_id,
            "agent_id": agent_id,
            "signatures_collected": len(p.signatures),
            "required": p.required_signatures,
            "is_approved": p.is_approved
        }

    def verify_action_permit(self, action_id: str) -> bool:
        p = self._proposals.get(action_id)
        return bool(p and p.is_approved)
