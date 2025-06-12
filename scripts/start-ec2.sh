#!/bin/bash

export AWS_PAGER=""

# Instance details
INSTANCE_ID="i-037e0c7f9dbc9db27"  # ← Replace with your actual instance ID
REGION="us-west-2"

echo "🔍 Checking current EC2 state..."

STATE=$(aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --region "$REGION" \
  --query "Reservations[0].Instances[0].State.Name" \
  --output text)

if [ "$STATE" == "running" ]; then
  echo "✅ Instance is already running. No action taken."
  exit 0
fi

echo "🚀 Starting EC2 instance: $INSTANCE_ID..."
aws ec2 start-instances \
  --instance-ids "$INSTANCE_ID" \
  --region "$REGION" >/dev/null

# Live wait loop
echo "⏳ Waiting for instance to start..."
while true; do
  CURRENT_STATE=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --region "$REGION" \
    --query "Reservations[0].Instances[0].State.Name" \
    --output text)

  echo "   → Current state: $CURRENT_STATE"
  if [ "$CURRENT_STATE" == "running" ]; then
    echo "✅ Instance is now running!"
    break
  fi

  sleep 5
done