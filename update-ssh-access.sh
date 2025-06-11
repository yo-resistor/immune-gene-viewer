#!/bin/bash

export AWS_PAGER=""

# Configuration
SECURITY_GROUP_ID="sg-0064a66ec816cab08"
REGION="us-west-2"
PORT=22
USER="ubuntu"
INSTANCE_IP="52.42.31.181"

# Step 1: Get current public IP
MY_IP=$(curl -s https://checkip.amazonaws.com)
CIDR="${MY_IP}/32"

echo "📡 Your current IP: $CIDR"

# Step 2: Check if this IP is already allowed in the SG
IS_ALLOWED=$(aws ec2 describe-security-groups \
    --group-ids "$SECURITY_GROUP_ID" \
    --region "$REGION" \
    --query "SecurityGroups[0].IpPermissions[?ToPort==\`$PORT\`].IpRanges[?CidrIp=='$CIDR']" \
    --output text)

if [[ -n "$IS_ALLOWED" ]]; then
    echo "🔍 IP is allowed. Verifying SSH access..."
    
    ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -i /Users/yunpro/Dropbox/Mac/Desktop/immune-gene-viewer/keypair/immune-viewer-instance-keypair.pem $USER@$INSTANCE_IP "exit" 2>/dev/null
    
    if [[ $? -eq 0 ]]; then
        echo "✅ SSH is accessible. No changes needed."
        exit 0
    else
        echo "⚠️ IP is allowed but SSH failed. Proceeding to update."
    fi
else
    echo "🚫 IP not allowed. Proceeding to update security group..."
fi

# Step 3: Revoke all other existing IPs on port 22
OLD_CIDRS=$(aws ec2 describe-security-groups \
    --group-ids "$SECURITY_GROUP_ID" \
    --region "$REGION" \
    --query "SecurityGroups[0].IpPermissions[?ToPort==\`$PORT\`].IpRanges[].CidrIp" \
    --output text)

for OLD_CIDR in $OLD_CIDRS; do
    if [[ "$OLD_CIDR" != "$CIDR" ]]; then
        echo "⛔ Revoking $OLD_CIDR"
        aws ec2 revoke-security-group-ingress \
            --group-id "$SECURITY_GROUP_ID" \
            --protocol tcp \
            --port $PORT \
            --cidr "$OLD_CIDR" \
            --region "$REGION"
    fi
done

# Step 4: Authorize the new IP
echo "🔐 Authorizing $CIDR"
aws ec2 authorize-security-group-ingress \
    --group-id "$SECURITY_GROUP_ID" \
    --protocol tcp \
    --port $PORT \
    --cidr "$CIDR" \
    --region "$REGION"

echo "✅ SSH access updated for $CIDR"