#!/bin/bash

export AWS_PAGER=""

# Instance details
INSTANCE_ID="i-00b8be37010e3631f"
REGION="us-west-2"

echo "🔍 Checking current EC2 state..."

STATE=$(aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --region "$REGION" \
  --query "Reservations[0].Instances[0].State.Name" \
  --output text)

if [ "$STATE" == "stopped" ]; then
  echo "✅ Instance is already stopped. No action taken."
  exit 0
fi

echo "🛑 Stopping EC2 instance: $INSTANCE_ID..."
aws ec2 stop-instances \
  --instance-ids "$INSTANCE_ID" \
  --region "$REGION" >/dev/null

echo "⏳ Waiting for instance to enter 'stopped' state..."
aws ec2 wait instance-stopped \
  --instance-ids "$INSTANCE_ID" \
  --region "$REGION"

echo "✅ EC2 instance is now stopped!"