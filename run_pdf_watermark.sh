#!/bin/bash
# PDF水印工具启动脚本 - 修复中文显示问题

echo "🚀 启动PDF水印工具..."
echo "✅ 已修复中文字体显示问题"
echo "================================"

cd "$(dirname "$0")"
source pdf_watermark_env/bin/activate
./pdf_watermark_env/bin/python pdf_shuiyin.py
