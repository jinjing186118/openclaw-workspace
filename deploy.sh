#!/bin/bash
# deploy.sh - 一键部署脚本
# 用法: ./deploy.sh

set -e

echo "🚀 OpenClaw Workspace 部署脚本"
echo "================================"

# 拉取最新代码
echo "📥 拉取最新代码..."
git pull origin main

# 重启 OpenClaw
echo "🔄 重启 OpenClaw..."
openclaw gateway restart

echo "✅ 部署完成！"
echo ""
echo "查看状态: openclaw status"
