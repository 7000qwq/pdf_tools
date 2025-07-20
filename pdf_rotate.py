#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF旋转工具
功能：旋转PDF文件的页面
依赖：pip install PyPDF2
"""

import os
import sys
import PyPDF2

class PDFRotateTool:
    def __init__(self):
        """初始化PDF旋转工具"""
        self.input_pdf_path = ""
        self.output_pdf_path = ""
        
    def rotate_pdf(self, input_path, output_path, rotation_angle, page_range=None):
        """
        旋转PDF页面
        
        Args:
            input_path (str): 输入PDF路径
            output_path (str): 输出PDF路径
            rotation_angle (int): 旋转角度 (90, 180, 270, -90, -180, -270)
            page_range (str): 页面范围，如 "1-3" 或 "1,3,5" 或 "all"
        """
        try:
            # 读取原始PDF
            with open(input_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                total_pages = len(pdf_reader.pages)
                print(f"正在处理PDF文件，共 {total_pages} 页...")
                
                # 解析页面范围
                pages_to_rotate = self.parse_page_range(page_range, total_pages)
                
                for page_num in range(1, total_pages + 1):
                    page = pdf_reader.pages[page_num - 1]
                    
                    if page_num in pages_to_rotate:
                        # 旋转指定页面
                        page.rotate(rotation_angle)
                        print(f"旋转第 {page_num} 页 {rotation_angle}°")
                    else:
                        print(f"保持第 {page_num} 页不变")
                    
                    pdf_writer.add_page(page)
                
                # 保存旋转后的PDF
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                    
                print(f"✅ PDF旋转完成！输出文件：{output_path}")
                
        except Exception as e:
            print(f"❌ 处理PDF时出错：{e}")
            raise
    
    def parse_page_range(self, page_range, total_pages):
        """
        解析页面范围
        
        Args:
            page_range (str): 页面范围字符串
            total_pages (int): 总页数
            
        Returns:
            set: 需要旋转的页面号集合
        """
        if not page_range or page_range.lower() == "all":
            return set(range(1, total_pages + 1))
        
        pages = set()
        
        # 处理逗号分隔的页面
        parts = page_range.split(',')
        
        for part in parts:
            part = part.strip()
            
            if '-' in part:
                # 处理范围，如 "1-5"
                try:
                    start, end = part.split('-')
                    start = int(start.strip())
                    end = int(end.strip())
                    
                    # 确保范围在有效范围内
                    start = max(1, min(start, total_pages))
                    end = max(1, min(end, total_pages))
                    
                    if start <= end:
                        pages.update(range(start, end + 1))
                    else:
                        pages.update(range(end, start + 1))
                        
                except ValueError:
                    print(f"⚠️ 无效的页面范围: {part}")
                    continue
            else:
                # 处理单个页面
                try:
                    page_num = int(part)
                    if 1 <= page_num <= total_pages:
                        pages.add(page_num)
                    else:
                        print(f"⚠️ 页面号超出范围: {page_num}")
                except ValueError:
                    print(f"⚠️ 无效的页面号: {part}")
                    continue
        
        return pages
    
    def run(self):
        """运行主程序"""
        print("=" * 60)
        print("           PDF 旋转工具")
        print("=" * 60)
        
        # 获取输入PDF路径
        while True:
            input_path = input("请输入PDF文件路径: ").strip().strip('"\'')
            if os.path.exists(input_path) and input_path.lower().endswith('.pdf'):
                self.input_pdf_path = input_path
                break
            else:
                print("❌ 文件不存在或不是PDF文件，请重新输入！")
        
        # 显示PDF信息
        try:
            with open(self.input_pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                print(f"\n📄 PDF信息：共 {total_pages} 页")
        except Exception as e:
            print(f"⚠️ 无法读取PDF信息: {e}")
            total_pages = 0
        
        # 选择旋转角度
        print("\n旋转角度选项：")
        print("1. 顺时针旋转90°")
        print("2. 旋转180°")
        print("3. 逆时针旋转90° (顺时针270°)")
        print("4. 自定义角度")
        
        while True:
            try:
                choice = input("请选择旋转角度 (1-4): ").strip()
                if choice == "1":
                    rotation_angle = 90
                    break
                elif choice == "2":
                    rotation_angle = 180
                    break
                elif choice == "3":
                    rotation_angle = 270
                    break
                elif choice == "4":
                    angle_input = input("请输入旋转角度 (正数顺时针，负数逆时针): ").strip()
                    rotation_angle = int(angle_input)
                    # 规范化角度到0-360范围
                    rotation_angle = rotation_angle % 360
                    break
                else:
                    print("❌ 无效选择，请输入1-4之间的数字！")
            except ValueError:
                print("❌ 请输入有效的数字！")
        
        # 选择页面范围
        print(f"\n页面范围选项 (总共 {total_pages} 页)：")
        print("1. 所有页面")
        print("2. 指定页面")
        
        while True:
            choice = input("请选择页面范围 (1-2): ").strip()
            if choice == "1":
                page_range = "all"
                break
            elif choice == "2":
                print("\n页面范围格式说明：")
                print("- 所有页面: all 或直接回车")
                print("- 单个页面: 1 或 3 或 5")
                print("- 多个页面: 1,3,5")
                print("- 页面范围: 1-5 或 2-8")
                print("- 混合格式: 1,3-5,8,10-12")
                
                page_range = input(f"请输入页面范围 (1-{total_pages}): ").strip()
                if not page_range:
                    page_range = "all"
                break
            else:
                print("❌ 无效选择，请输入1或2！")
        
        # 生成输出文件路径
        base_name = os.path.splitext(self.input_pdf_path)[0]
        angle_desc = f"{rotation_angle}deg" if rotation_angle != 0 else "0deg"
        self.output_pdf_path = f"{base_name}_rotated_{angle_desc}.pdf"
        
        # 确认信息
        print("\n" + "=" * 60)
        print("处理信息确认：")
        print(f"输入文件: {self.input_pdf_path}")
        print(f"输出文件: {self.output_pdf_path}")
        print(f"旋转角度: {rotation_angle}°")
        print(f"页面范围: {page_range}")
        print("=" * 60)
        
        confirm = input("确认开始处理？(y/n): ").strip().lower()
        if confirm in ['y', 'yes', '是', '确认']:
            try:
                self.rotate_pdf(
                    self.input_pdf_path, 
                    self.output_pdf_path, 
                    rotation_angle,
                    page_range
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
        import PyPDF2
    except ImportError as e:
        print("❌ 缺少必要的依赖库！")
        print("请运行以下命令安装：")
        print("pip install PyPDF2")
        sys.exit(1)
    
    # 创建工具实例并运行
    tool = PDFRotateTool()
    success = tool.run()
    
    if success:
        print("\n🎉 任务完成！")
    else:
        print("\n❌ 任务失败！")

if __name__ == "__main__":
    main()
