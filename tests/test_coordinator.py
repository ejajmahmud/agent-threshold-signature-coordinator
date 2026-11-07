"""Tests for agent-threshold-signature-coordinator."""
import unittest
from agent_threshold_signature_coordinator.coordinator import ThresholdSignatureCoordinator


class TestThresholdCoordinator(unittest.TestCase):
    def setUp(self):
        self.keys = {"a1": "k1", "a2": "k2", "a3": "k3"}
        self.coord = ThresholdSignatureCoordinator(self.keys)

    def test_quorum_approval(self):
        self.coord.create_proposal("act_1", "deploy", {"env": "prod"}, required_signatures=2)
        r1 = self.coord.sign_proposal("act_1", "a1")
        self.assertFalse(r1["is_approved"])
        r2 = self.coord.sign_proposal("act_1", "a2")
        self.assertTrue(r2["is_approved"])
        self.assertTrue(self.coord.verify_action_permit("act_1"))

    def test_unauthorized_signer(self):
        self.coord.create_proposal("act_2", "run", {}, required_signatures=1)
        with self.assertRaises(PermissionError):
            self.coord.sign_proposal("act_2", "hacker_agent")
