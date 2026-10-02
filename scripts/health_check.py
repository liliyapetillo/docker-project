# Checks that the prod ECS service has as many tasks running as it wants.
# Exits 0 if healthy, 1 otherwise, so this can gate a CI/CD pipeline.
import os
import sys

import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Read from the same ECS_CLUSTER / ECS_SERVICE_PROD secrets deploy.yml uses.
CLUSTER = os.getenv("ECS_CLUSTER")
SERVICE = os.getenv("ECS_SERVICE_PROD")


def main():
    if not CLUSTER or not SERVICE:
        print("FAIL: set ECS_CLUSTER and ECS_SERVICE_PROD environment variables")
        return 1

    try:
        services = boto3.client("ecs").describe_services(
            cluster=CLUSTER, services=[SERVICE]
        )["services"]
    except (ClientError, BotoCoreError) as e:
        print(f"FAIL: could not describe service {SERVICE!r} in cluster {CLUSTER!r}: {e}")
        return 1

    if not services:
        print(f"FAIL: service {SERVICE!r} not found in cluster {CLUSTER!r}")
        return 1

    running, desired = services[0]["runningCount"], services[0]["desiredCount"]
    ok = running == desired
    print(f"{'PASS' if ok else 'FAIL'}: {SERVICE} running {running}/{desired} tasks")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
