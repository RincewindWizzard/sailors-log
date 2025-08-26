#!/bin/bash
set -euo pipefail

REQUIRED_VARS=("CLUSTER_HOST" "SSH_KEY" "KUBECONFIG" "GITHUB_TOKEN" "GITHUB_ACTOR")

NAMESPACE="sailors-log"
TMP_PATH="target"
KUBECONFIG_PATH="$TMP_PATH/kubeconfig.yaml"
SSH_CONTROL_PATH="$TMP_PATH/ssh_control"
SSH_KEY_PATH="$TMP_PATH/ssh_key"

# Source .env file if available
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

# check if all vars are set
for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "$(printenv "$var")" ]; then
    echo "Error: Environment variable '$var' is not set."
    exit 1
  fi
done

echo "All required environment variables are set."


# Create empty tmp path
rm -rf $TMP_PATH
mkdir -p $TMP_PATH

# add ssh private key
echo "$SSH_KEY" > $SSH_KEY_PATH
chmod go-rwx $SSH_KEY_PATH

# Save kubeconfig file
echo "$KUBECONFIG" > $KUBECONFIG_PATH

ssh \
  -f -N \
  -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=$TMP_PATH/known_hosts \
  -i $TMP_PATH/ssh_key \
  -o ControlMaster=yes \
  -o ControlPath=$SSH_CONTROL_PATH \
  -L 6443:localhost:6443 \
  deployment@$CLUSTER_HOST


echo 'Building docker image'

echo "$GITHUB_TOKEN" | docker login ghcr.io -u $GITHUB_ACTOR --password-stdin
docker build -t ghcr.io/sgfh-kiel/sailors-log:latest .
docker push ghcr.io/sgfh-kiel/sailors-log:latest

echo 'Docker image succesfully deployed to ghcr.io/sgfh-kiel/sailors-log:latest'

kubectl apply \
  --kubeconfig=$KUBECONFIG_PATH \
  --recursive \
  --filename "k8s" \
  --namespace "$NAMESPACE"  \
  --prune  \
  --selector managed-by=gitops \
  --prune-allowlist=apps/v1/Deployment \
  --prune-allowlist=core/v1/Service \
  --prune-allowlist=networking.k8s.io/v1/Ingress

# restart to force pull of new images
kubectl rollout restart deployment \
 -l managed-by=gitops --namespace "$NAMESPACE" \
 --kubeconfig="$KUBECONFIG_PATH"



  # Close ssh connection
  ssh -O exit -o ControlPath=$SSH_CONTROL_PATH deployment@$CLUSTER_HOST