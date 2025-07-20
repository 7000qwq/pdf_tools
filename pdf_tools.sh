#!/bin/bash
# PDF工具集合 - 统一启动脚本

echo "🛠️  PDF处理工具集合"
echo "================================"
echo "1. PDF水印添加工具 (支持中文)"
echo "2. PDF旋转工具"
echo "3. PDF页面删除工具"
echo "4. 退出"
echo "================================"

while true; do
    read -p "请选择工具 (1-4): " choice
    
    case $choice in
        1)
            echo "🏃 启动PDF水印工具..."
            ./run_pdf_watermark.sh
            break
            ;;
        2)
            echo "🔄 启动PDF旋转工具..."
            ./run_pdf_rotate.sh
            break
            ;;
        3)
            echo "🗑️ 启动PDF页面删除工具..."
            ./run_pdf_delete.sh
            break
            ;;
        4)
            echo "👋 再见！"
            exit 0
            ;;
        *)
            echo "❌ 无效选择，请输入1-4之间的数字"
            ;;
    esac
done
