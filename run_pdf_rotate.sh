#!/bin/bash
# PDF旋转工具启动脚本

echo "🔄 启动PDF旋转工具..."
echo "支持旋转90°、180°、270°或自定义角度"
echo "================================"

cd "$(dirname "$0")"
source pdf_watermark_env/bin/activate
./pdf_watermark_env/bin/python pdf_rotate.py
