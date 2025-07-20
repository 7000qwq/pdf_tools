#!/bin/bash
# PDF页面删除工具启动脚本

echo "🗑️ 启动PDF页面删除工具..."
echo "支持删除指定页面或保留指定页面"
echo "================================"

cd "$(dirname "$0")"
source pdf_watermark_env/bin/activate
./pdf_watermark_env/bin/python pdf_delete.py
