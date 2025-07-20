#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF页面删除工具
功能：删除PDF文件中的指定页面
依赖：pip install PyPDF2
"""

import os
import sys
import PyPDF2

class PDFDeleteTool:
    def __init__(self):
        """初始化PDF页面删除工具"""
        self.input_pdf_path = ""
        self.output_pdf_path = ""
        
    def delete_pages_from_pdf(self, input_path, output_path, pages_to_delete):
        """
        从PDF中删除指定页面
        
        Args:
            input_path (str): 输入PDF路径
            output_path (str): 输出PDF路径
            pages_to_delete (set): 要删除的页面号集合
        """
        try:
            # 读取原始PDF
            with open(input_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                total_pages = len(pdf_reader.pages)
                print(f"正在处理PDF文件，共 {total_pages} 页...")
                
                kept_pages = 0
                deleted_pages = 0
                
                for page_num in range(1, total_pages + 1):
                    page = pdf_reader.pages[page_num - 1]
                    
                    if page_num in pages_to_delete:
                        print(f"🗑️ 删除第 {page_num} 页")
                        deleted_pages += 1
                    else:
                        pdf_writer.add_page(page)
                        print(f"✅ 保留第 {page_num} 页")
                        kept_pages += 1
                
                # 检查是否还有页面保留
                if kept_pages == 0:
                    print("❌ 错误：不能删除所有页面！")
                    return False
                
                # 保存处理后的PDF
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                    
                print(f"\n📊 处理统计：")
                print(f"原始页数: {total_pages}")
                print(f"删除页数: {deleted_pages}")
                print(f"保留页数: {kept_pages}")
                print(f"✅ PDF页面删除完成！输出文件：{output_path}")
                return True
                
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
            set: 需要删除的页面号集合
        """
        if not page_range:
            return set()
        
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
    
    def preview_deletion(self, pages_to_delete, total_pages):
        """
        预览删除操作
        
        Args:
            pages_to_delete (set): 要删除的页面
            total_pages (int): 总页数
        """
        print("\n📋 删除预览：")
        print("=" * 50)
        
        # 显示要删除的页面
        if pages_to_delete:
            delete_list = sorted(list(pages_to_delete))
            print(f"🗑️ 将删除的页面: {', '.join(map(str, delete_list))}")
        else:
            print("🗑️ 将删除的页面: 无")
        
        # 显示保留的页面
        keep_pages = set(range(1, total_pages + 1)) - pages_to_delete
        if keep_pages:
            keep_list = sorted(list(keep_pages))
            print(f"✅ 将保留的页面: {', '.join(map(str, keep_list))}")
        else:
            print("✅ 将保留的页面: 无")
        
        print(f"📊 页面统计: 删除 {len(pages_to_delete)} 页，保留 {len(keep_pages)} 页")
        print("=" * 50)
        
        # 安全检查
        if len(keep_pages) == 0:
            print("❌ 警告：这将删除所有页面！操作无法执行。")
            return False
        elif len(pages_to_delete) == 0:
            print("⚠️ 注意：未选择任何页面删除。")
            return False
        
        return True
    
    def run(self):
        """运行主程序"""
        print("=" * 60)
        print("           PDF 页面删除工具")
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
                
                # 显示页面列表
                if total_pages <= 20:
                    print(f"页面列表: {', '.join(map(str, range(1, total_pages + 1)))}")
                else:
                    print(f"页面列表: 1-{total_pages} (共{total_pages}页)")
                    
        except Exception as e:
            print(f"⚠️ 无法读取PDF信息: {e}")
            return False
        
        # 选择删除方式
        print("\n删除方式选项：")
        print("1. 删除指定页面")
        print("2. 保留指定页面（删除其他）")
        
        while True:
            choice = input("请选择删除方式 (1-2): ").strip()
            if choice in ["1", "2"]:
                break
            else:
                print("❌ 无效选择，请输入1或2！")
        
        # 获取页面范围
        print(f"\n页面范围格式说明 (总共 {total_pages} 页)：")
        print("- 单个页面: 1 或 3 或 5")
        print("- 多个页面: 1,3,5")
        print("- 页面范围: 1-5 或 2-8")
        print("- 混合格式: 1,3-5,8,10-12")
        
        if choice == "1":
            page_input = input(f"请输入要删除的页面 (1-{total_pages}): ").strip()
            pages_to_delete = self.parse_page_range(page_input, total_pages)
        else:
            page_input = input(f"请输入要保留的页面 (1-{total_pages}): ").strip()
            pages_to_keep = self.parse_page_range(page_input, total_pages)
            pages_to_delete = set(range(1, total_pages + 1)) - pages_to_keep
        
        # 预览删除操作
        if not self.preview_deletion(pages_to_delete, total_pages):
            print("❌ 操作无法执行")
            return False
        
        # 生成输出文件路径
        base_name = os.path.splitext(self.input_pdf_path)[0]
        deleted_count = len(pages_to_delete)
        kept_count = total_pages - deleted_count
        self.output_pdf_path = f"{base_name}_deleted_{deleted_count}pages_kept_{kept_count}pages.pdf"
        
        # 确认信息
        print("\n" + "=" * 60)
        print("处理信息确认：")
        print(f"输入文件: {self.input_pdf_path}")
        print(f"输出文件: {self.output_pdf_path}")
        print(f"删除页面: {sorted(list(pages_to_delete)) if pages_to_delete else '无'}")
        print(f"删除模式: {'删除指定页面' if choice == '1' else '保留指定页面'}")
        print("=" * 60)
        
        confirm = input("确认开始处理？(y/n): ").strip().lower()
        if confirm in ['y', 'yes', '是', '确认']:
            try:
                success = self.delete_pages_from_pdf(
                    self.input_pdf_path, 
                    self.output_pdf_path, 
                    pages_to_delete
                )
                return success
            except Exception as e:
                print(f"❌ 处理失败：{e}")
                return False
        else:
            print("❌ 已取消处理")
            return False

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
    tool = PDFDeleteTool()
    success = tool.run()
    
    if success:
        print("\n🎉 任务完成！")
    else:
        print("\n❌ 任务失败！")

if __name__ == "__main__":
    main()
