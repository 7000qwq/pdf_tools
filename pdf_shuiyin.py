#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF水印添加工具
功能：为PDF文件的每一页添加铺满的水印
依赖：pip install reportlab PyPDF2
"""

import os
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import PyPDF2
import io
import math

class PDFWatermarkTool:
    def __init__(self):
        """初始化PDF水印工具"""
        self.watermark_text = ""
        self.input_pdf_path = ""
        self.output_pdf_path = ""
        
    def create_watermark_pdf(self, text, page_width, page_height, opacity=0.3, font_size=50):
        """
        创建水印PDF
        
        Args:
            text (str): 水印文字
            page_width (float): 页面宽度
            page_height (float): 页面高度
            opacity (float): 透明度 (0-1)
            font_size (int): 字体大小
            
        Returns:
            bytes: 水印PDF的字节数据
        """
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
        # 设置透明度
        can.setFillColorRGB(0.5, 0.5, 0.5, opacity)
        
        # 设置字体 - 优先使用支持中文的字体
        try:
            # macOS系统的中文字体路径
            chinese_font_paths = [
                '/System/Library/Fonts/PingFang.ttc',  # 苹方字体
                '/System/Library/Fonts/STHeiti Light.ttc',  # 黑体
                '/System/Library/Fonts/STSong.ttc',  # 宋体
                '/System/Library/Fonts/Hiragino Sans GB.ttc',  # 冬青黑体
                '/Library/Fonts/Arial Unicode MS.ttf',  # Arial Unicode MS
                '/System/Library/Fonts/Apple SD Gothic Neo.ttc',  # Apple SD Gothic Neo
            ]
            
            # Windows和Linux的中文字体路径
            other_font_paths = [
                'C:/Windows/Fonts/simsun.ttc',  # Windows 宋体
                'C:/Windows/Fonts/simhei.ttf',  # Windows 黑体
                'C:/Windows/Fonts/msyh.ttc',   # Windows 微软雅黑
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
                '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'  # Linux
            ]
            
            all_font_paths = chinese_font_paths + other_font_paths
            
            font_registered = False
            for font_path in all_font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                        can.setFont('ChineseFont', font_size)
                        font_registered = True
                        print(f"✅ 使用字体: {font_path}")
                        break
                    except Exception as font_error:
                        print(f"⚠️ 字体 {font_path} 加载失败: {font_error}")
                        continue
            
            if not font_registered:
                print("⚠️ 未找到支持中文的字体，使用默认字体（可能无法显示中文）")
                can.setFont('Helvetica', font_size)
                
        except Exception as e:
            print(f"❌ 字体设置失败，使用默认字体: {e}")
            can.setFont('Helvetica', font_size)
        
        # 计算文字尺寸
        text_width = can.stringWidth(text, can._fontname, font_size)
        text_height = font_size
        
        # 测试字体是否能正确显示中文
        test_char = '中'
        if test_char in text:
            test_width = can.stringWidth(test_char, can._fontname, font_size)
            if test_width == 0:
                print("⚠️ 警告：当前字体可能无法正确显示中文字符")
            else:
                print("✅ 中文字符显示测试通过")
        
        # 计算需要多少行和列来铺满页面
        diagonal_length = math.sqrt(page_width**2 + page_height**2)
        spacing_x = text_width + 50  # 水印间距
        spacing_y = text_height + 30
        
        # 计算旋转角度（对角线方向）
        angle = math.degrees(math.atan2(page_height, page_width))
        
        # 保存当前画布状态
        can.saveState()
        
        # 在整个页面铺满水印
        start_x = -diagonal_length
        start_y = -diagonal_length
        
        y = start_y
        while y < diagonal_length * 2:
            x = start_x
            while x < diagonal_length * 2:
                can.saveState()
                can.translate(x, y)
                can.rotate(angle)
                can.drawString(0, 0, text)
                can.restoreState()
                x += spacing_x
            y += spacing_y
        
        # 恢复画布状态
        can.restoreState()
        can.save()
        
        packet.seek(0)
        return packet.getvalue()
    
    def add_watermark_to_pdf(self, input_path, output_path, watermark_text, opacity=0.3, font_size=50):
        """
        为PDF添加水印
        
        Args:
            input_path (str): 输入PDF路径
            output_path (str): 输出PDF路径
            watermark_text (str): 水印文字
            opacity (float): 透明度
            font_size (int): 字体大小
        """
        try:
            # 读取原始PDF
            with open(input_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                total_pages = len(pdf_reader.pages)
                print(f"正在处理PDF文件，共 {total_pages} 页...")
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    print(f"处理第 {page_num}/{total_pages} 页...")
                    
                    # 获取页面尺寸
                    page_width = float(page.mediabox.width)
                    page_height = float(page.mediabox.height)
                    
                    # 创建该页面的水印
                    watermark_bytes = self.create_watermark_pdf(
                        watermark_text, page_width, page_height, opacity, font_size
                    )
                    
                    # 读取水印PDF
                    watermark_pdf = PyPDF2.PdfReader(io.BytesIO(watermark_bytes))
                    watermark_page = watermark_pdf.pages[0]
                    
                    # 将水印应用到原页面
                    page.merge_page(watermark_page)
                    pdf_writer.add_page(page)
                
                # 保存带水印的PDF
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                    
                print(f"✅ 水印添加完成！输出文件：{output_path}")
                
        except Exception as e:
            print(f"❌ 处理PDF时出错：{e}")
            raise
    
    def run(self):
        """运行主程序"""
        print("=" * 60)
        print("           PDF 水印添加工具")
        print("=" * 60)
        
        # 获取输入PDF路径
        while True:
            input_path = input("请输入PDF文件路径: ").strip().strip('"\'')
            if os.path.exists(input_path) and input_path.lower().endswith('.pdf'):
                self.input_pdf_path = input_path
                break
            else:
                print("❌ 文件不存在或不是PDF文件，请重新输入！")
        
        # 获取水印内容
        while True:
            watermark_text = input("请输入水印内容: ").strip()
            if watermark_text:
                self.watermark_text = watermark_text
                break
            else:
                print("❌ 水印内容不能为空，请重新输入！")
        
        # 生成输出文件路径
        base_name = os.path.splitext(self.input_pdf_path)[0]
        self.output_pdf_path = f"{base_name}_watermarked.pdf"
        
        # 获取可选参数
        print("\n可选参数设置（直接回车使用默认值）：")
        
        # 透明度设置
        try:
            opacity_input = input("水印透明度 (0.1-1.0, 默认0.3): ").strip()
            opacity = float(opacity_input) if opacity_input else 0.3
            opacity = max(0.1, min(1.0, opacity))
        except:
            opacity = 0.3
        
        # 字体大小设置
        try:
            font_size_input = input("字体大小 (20-100, 默认50): ").strip()
            font_size = int(font_size_input) if font_size_input else 50
            font_size = max(20, min(100, font_size))
        except:
            font_size = 50
        
        # 确认信息
        print("\n" + "=" * 60)
        print("处理信息确认：")
        print(f"输入文件: {self.input_pdf_path}")
        print(f"输出文件: {self.output_pdf_path}")
        print(f"水印内容: {self.watermark_text}")
        print(f"透明度: {opacity}")
        print(f"字体大小: {font_size}")
        print("=" * 60)
        
        confirm = input("确认开始处理？(y/n): ").strip().lower()
        if confirm in ['y', 'yes', '是', '确认']:
            try:
                self.add_watermark_to_pdf(
                    self.input_pdf_path, 
                    self.output_pdf_path, 
                    self.watermark_text,
                    opacity,
                    font_size
                )
            except Exception as e:
                print(f"❌ 处理失败：{e}")
                return False
        else:
            print("❌ 已取消处理")
            return False
        
        return True

def main():
    """主函数"""
    # 检查依赖
    try:
        import reportlab
        import PyPDF2
    except ImportError as e:
        print("❌ 缺少必要的依赖库！")
        print("请运行以下命令安装：")
        print("pip install reportlab PyPDF2")
        sys.exit(1)
    
    # 创建工具实例并运行
    tool = PDFWatermarkTool()
    success = tool.run()
    
    if success:
        print("\n🎉 任务完成！")
    else:
        print("\n❌ 任务失败！")

if __name__ == "__main__":
    main()