#!/bin/bash

export AWS_PAGER=""

# Instance details
INSTANCE_ID="i-00b8be37010e3631f"  # ← Replace with your actual instance ID
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

# Live wait loop
echo "⏳ Waiting for instance to stop..."
while true; do
  CURRENT_STATE=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --region "$REGION" \
    --query "Reservations[0].Instances[0].State.Name" \
    --output text)

  echo "   → Current state: $CURRENT_STATE"
  if [ "$CURRENT_STATE" == "stopped" ]; then
    echo "✅ Instance is now stopped!"
    break
  fi

  sleep 5
done