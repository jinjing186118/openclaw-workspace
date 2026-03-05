#!/bin/bash
cd /root/.openclaw/workspace

LOG=/root/.openclaw/workspace/install_log.txt
> "$LOG"

install_skill() {
    local skill="$1"
    local bot="$2"
    local attempt=0
    local max_attempts=3
    
    while [ $attempt -lt $max_attempts ]; do
        result=$(clawhub install "$skill" 2>&1)
        
        if echo "$result" | grep -q "OK. Installed"; then
            echo "$bot|$skill|SUCCESS" >> "$LOG"
            echo "✅ $skill"
            return 0
        elif echo "$result" | grep -q "suspicious"; then
            echo "$bot|$skill|SECURITY_SKIP" >> "$LOG"
            echo "🔒 $skill (security)"
            return 1
        elif echo "$result" | grep -q "not found"; then
            echo "$bot|$skill|NOT_FOUND" >> "$LOG"
            echo "❌ $skill (not found)"
            return 1
        elif echo "$result" | grep -q "already exists"; then
            echo "$bot|$skill|EXISTS" >> "$LOG"
            echo "⏭️ $skill (exists)"
            return 0
        elif echo "$result" | grep -q "Rate limit"; then
            attempt=$((attempt + 1))
            echo "⏳ $skill rate limited, attempt $attempt, waiting 45s..."
            sleep 45
        else
            echo "$bot|$skill|UNKNOWN: $result" >> "$LOG"
            echo "❓ $skill (unknown error)"
            return 1
        fi
    done
    echo "$bot|$skill|RATE_LIMIT_FAIL" >> "$LOG"
    echo "💥 $skill (rate limit exceeded after retries)"
    return 1
}

DELAY=25

echo "========== DEV (3 remaining) =========="
for skill in create-cli agent-nestjs-skills agentbench; do install_skill "$skill" "dev"; sleep $DELAY; done

echo "========== CONTENT (10) =========="
for skill in convert-to-pdf markdown-converter chain-of-density meeting-notes meeting-to-action confluence capacities custom-smtp-sender book-reader contract-generator; do install_skill "$skill" "content"; sleep $DELAY; done

echo "========== OPS (10) =========="
for skill in bing-search aisa-twitter-skill anycrawl amazon-data ai-news-oracle osint-graph-analyzer tweet-processor finance-news attio-crm appstore-rating-pulse; do install_skill "$skill" "ops"; sleep $DELAY; done

echo "========== VIDEO (10) =========="
for skill in eachlabs-video-generation eachlabs-video-edit eachlabs-image-generation eachlabs-image-edit fal-ai heygen-avatar-lite chart-image captions agents-skill-podcastifier eachlabs-face-swap; do install_skill "$skill" "vedio"; sleep $DELAY; done

echo "========== BRAND (10) =========="
for skill in bluesky bird brand-voice-profile brw-marketing-principles brw-newsletter-creation-curation campaign-orchestrator cold-email ghost-cms botsee go-to-market; do install_skill "$skill" "brand"; sleep $DELAY; done

echo "========== REQUIREMENTS (10) =========="
for skill in data-analyst duckdb-en senior-data-scientist agile-product-owner marketing-strategy-pmm competitor-analyzer clickup-mcp csv-pipeline amplitude-automation business-development; do install_skill "$skill" "requirements"; sleep $DELAY; done

echo ""
echo "========== DONE =========="
echo "Results:"
cat "$LOG"
