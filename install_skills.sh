#!/bin/bash
cd /root/.openclaw/workspace

DELAY=20
SUCCESS=0
SECURITY_SKIP=0
NOT_FOUND=0
RATE_LIMIT=0

install_skill() {
    local skill="$1"
    echo "=== Installing: $skill ==="
    result=$(clawhub install "$skill" 2>&1)
    echo "$result" | tail -3
    
    if echo "$result" | grep -q "OK. Installed"; then
        echo "STATUS: SUCCESS"
        SUCCESS=$((SUCCESS + 1))
    elif echo "$result" | grep -q "suspicious"; then
        echo "STATUS: SECURITY_SKIP"
        SECURITY_SKIP=$((SECURITY_SKIP + 1))
    elif echo "$result" | grep -q "not found"; then
        echo "STATUS: NOT_FOUND"
        NOT_FOUND=$((NOT_FOUND + 1))
    elif echo "$result" | grep -q "Rate limit"; then
        echo "STATUS: RATE_LIMIT - retrying after 30s..."
        RATE_LIMIT=$((RATE_LIMIT + 1))
        sleep 30
        result=$(clawhub install "$skill" 2>&1)
        echo "$result" | tail -3
        if echo "$result" | grep -q "OK. Installed"; then
            echo "STATUS: SUCCESS (retry)"
            SUCCESS=$((SUCCESS + 1))
            RATE_LIMIT=$((RATE_LIMIT - 1))
        fi
    elif echo "$result" | grep -q "already exists"; then
        echo "STATUS: ALREADY_EXISTS"
    fi
    sleep $DELAY
}

# ===== DEV (need 3 more: have cicd-pipeline, audit-code, clean-pytest, api-tester, curl-http, aws-solution-architect, senior-devops = 7) =====
echo "========== DEV BOT =========="
for skill in create-cli docx-skill agent-nestjs-skills; do
    install_skill "$skill"
done

# ===== CONTENT (10) =====
echo "========== CONTENT BOT =========="
for skill in convert-to-pdf markdown-converter chain-of-density meeting-notes meeting-to-action confluence capacities custom-smtp-sender book-reader contract-generator; do
    install_skill "$skill"
done

# ===== OPS (10) =====
echo "========== OPS BOT =========="
for skill in bing-search aisa-twitter-skill anycrawl amazon-data ai-news-oracle osint-graph-analyzer tweet-processor finance-news attio-crm ai-news-zh; do
    install_skill "$skill"
done

# ===== VIDEO (10) =====
echo "========== VIDEO BOT =========="
for skill in eachlabs-video-generation eachlabs-video-edit eachlabs-image-generation eachlabs-image-edit fal-ai heygen-avatar-lite chart-image captions agents-skill-podcastifier eachlabs-face-swap; do
    install_skill "$skill"
done

# ===== BRAND (10) =====
echo "========== BRAND BOT =========="
for skill in bluesky bird brand-voice-profile brw-marketing-principles brw-newsletter-creation-curation campaign-orchestrator cold-email ghost-cms botsee go-to-market; do
    install_skill "$skill"
done

# ===== REQUIREMENTS (10) =====
echo "========== REQUIREMENTS BOT =========="
for skill in data-analyst duckdb-en senior-data-scientist agile-product-owner marketing-strategy-pmm competitor-analyzer clickup-mcp csv-pipeline amplitude-automation business-development; do
    install_skill "$skill"
done

echo ""
echo "========== SUMMARY =========="
echo "Success: $SUCCESS"
echo "Security skip: $SECURITY_SKIP"
echo "Not found: $NOT_FOUND"
echo "Rate limit failures: $RATE_LIMIT"
