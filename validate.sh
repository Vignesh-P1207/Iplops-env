#!/usr/bin/env bash
#
# OpenEnv Submission Validator for IPLOps-Env
# Checks Docker build, API endpoints, and inference script
#

set -uo pipefail

# Colors
if [ -t 1 ]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  BOLD='\033[1m'
  NC='\033[0m'
else
  RED='' GREEN='' YELLOW='' BOLD='' NC=''
fi

echo -e "${BOLD}========================================${NC}"
echo -e "${BOLD}IPLOps-Env Validation Script${NC}"
echo -e "${BOLD}========================================${NC}\n"

# Check 1: Docker build
echo -e "${YELLOW}[1/5] Checking Docker build...${NC}"
if docker build -t iplops-env . > /dev/null 2>&1; then
  echo -e "${GREEN}✓ Docker image builds successfully${NC}\n"
else
  echo -e "${RED}✗ Docker build failed${NC}"
  exit 1
fi

# Check 2: Start container
echo -e "${YELLOW}[2/5] Starting container...${NC}"
docker run -d -p 8000:8000 --name iplops-test iplops-env > /dev/null 2>&1
sleep 5

if docker ps | grep -q iplops-test; then
  echo -e "${GREEN}✓ Container started successfully${NC}\n"
else
  echo -e "${RED}✗ Container failed to start${NC}"
  docker logs iplops-test
  docker rm -f iplops-test > /dev/null 2>&1
  exit 1
fi

# Check 3: Health endpoint
echo -e "${YELLOW}[3/5] Testing health endpoint...${NC}"
if curl -s http://localhost:8000/health | grep -q "healthy"; then
  echo -e "${GREEN}✓ Health endpoint responds correctly${NC}\n"
else
  echo -e "${RED}✗ Health endpoint failed${NC}"
  docker logs iplops-test
  docker rm -f iplops-test > /dev/null 2>&1
  exit 1
fi

# Check 4: Reset endpoint
echo -e "${YELLOW}[4/5] Testing reset endpoint...${NC}"
if curl -s -X POST http://localhost:8000/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": 1}' | grep -q "observation"; then
  echo -e "${GREEN}✓ Reset endpoint works${NC}\n"
else
  echo -e "${RED}✗ Reset endpoint failed${NC}"
  docker rm -f iplops-test > /dev/null 2>&1
  exit 1
fi

# Check 5: Inference script
echo -e "${YELLOW}[5/5] Testing inference script...${NC}"
if python inference.py 1 2>&1 | grep -q "RESULT"; then
  echo -e "${GREEN}✓ Inference script runs successfully${NC}\n"
else
  echo -e "${RED}✗ Inference script failed${NC}"
  docker rm -f iplops-test > /dev/null 2>&1
  exit 1
fi

# Cleanup
docker rm -f iplops-test > /dev/null 2>&1

echo -e "${BOLD}========================================${NC}"
echo -e "${GREEN}${BOLD}✓ All validation checks passed!${NC}"
echo -e "${BOLD}========================================${NC}\n"

echo -e "Your submission is ready for:"
echo -e "  • Docker deployment"
echo -e "  • Hugging Face Spaces"
echo -e "  • OpenEnv validation"
echo -e "\nNext steps:"
echo -e "  1. Push to Hugging Face Spaces"
echo -e "  2. Set environment variables (API_BASE_URL, MODEL_NAME, HF_TOKEN)"
echo -e "  3. Test with: python inference.py <task_id>"

exit 0
