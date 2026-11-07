"""CLI for agent-threshold-signature-coordinator."""
import sys
import argparse
from .coordinator import ThresholdSignatureCoordinator


def main():
    parser = argparse.ArgumentParser(description="Agent Threshold Signature Coordinator")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    args = parser.parse_args()

    if args.demo:
        keys = {"agent_sec": "key1", "agent_lead": "key2", "agent_qa": "key3"}
        coord = ThresholdSignatureCoordinator(keys)
        p = coord.create_proposal("prop_01", "drop_production_db", {"target": "prod_users"}, required_signatures=2)
        print(f"Proposal created. Digest: {p.payload_digest}")
        s1 = coord.sign_proposal("prop_01", "agent_sec")
        print(f"Sign 1: Approved={s1['is_approved']}")
        s2 = coord.sign_proposal("prop_01", "agent_lead")
        print(f"Sign 2: Approved={s2['is_approved']}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
