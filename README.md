# 🎉 PDF Tools Collection

A collection of powerful PDF processing tools with GUI interfaces, designed for watermarking, rotating, and deleting pages from PDF files.

## 📦 Tools Overview

### 🏷️ PDF Watermark Tool (`pdf_shuiyin.py`)
- **Function**: Add watermarks to every page of a PDF
- **Features**: Chinese character support, adjustable transparency, customizable font size
- **Output**: `original_name_带水印.pdf`

### 🔄 PDF Rotation Tool (`pdf_rotate.py`)
- **Function**: Rotate PDF pages (90°, 180°, 270°, or custom angles)
- **Features**: Flexible page selection, batch processing, intelligent page parsing
- **Output**: `original_name_旋转X度.pdf`

### 🗑️ PDF Page Deletion Tool (`pdf_delete.py`)
- **Function**: Delete specified pages from PDF files
- **Features**: Dual deletion modes, safety protection, detailed operation preview
- **Output**: `original_name_删除X页_保留Y页.pdf`

## 🚀 Quick Start

### Unified Launcher
```bash
./pdf_tools.sh
```
Simply select the tool you need from the menu.

### Individual Tool Usage
Each tool can be run independently:
```bash
python pdf_shuiyin.py    # Watermark tool
python pdf_rotate.py     # Rotation tool  
python pdf_delete.py     # Page deletion tool
```

## 📁 Project Structure
```
pdf_tools/
├── pdf_shuiyin.py      # Watermark tool main program
├── pdf_rotate.py       # Rotation tool main program
├── pdf_delete.py       # Page deletion tool main program
├── pdf_tools.sh        # Unified launcher ⭐
├── 项目总结.md          # Project summary (Chinese)
├── README.md           # This file
└── .gitignore          # Git ignore file
```

## ✅ Feature Comparison

| Feature | Watermark Tool | Rotation Tool | Page Deletion Tool |
|---------|---------------|---------------|-------------------|
| Page Processing | All pages | Selected pages | Selected pages |
| Chinese Support | ✅ Full support | N/A | N/A |
| Custom Parameters | Transparency, font size | Rotation angle | Delete/keep modes |
| Safety Mechanism | Font detection | Angle validation | Prevent deleting all pages |

## 💡 Usage Tips

### Watermark Tool
- Chinese watermarks: recommended transparency 0.2-0.4
- Font size 30-60 works well for most documents
- For long text, consider line breaks

### Rotation Tool
- Page ranges support mixed formats: `1,3-5,8,10-12`
- Common angles: 90° (right), 270° (left), 180° (upside down)
- Test single page rotation first

### Page Deletion Tool
- Two modes: Delete specified pages OR Keep only specified pages
- Safety check prevents deleting all pages
- Preview shows exactly what will happen

## 🔧 Requirements
- macOS system
- Python 3.x
- Required packages: `reportlab`, `PyPDF2`

### Installation
```bash
pip install reportlab PyPDF2
```

## 🎯 Use Cases

### Watermark Tool
- Document copyright protection
- Confidential file marking
- Personal information identification
- Anti-theft watermarking

### Page Deletion Tool
- Document cleanup and organization
- Remove blank or advertisement pages
- Extract specific sections
- File size optimization
- Sensitive information removal

### Rotation Tool
- Fix incorrectly scanned documents
- Standardize page orientations
- Prepare documents for printing

## 🔄 Workflow Combinations

### Common Processing Pipeline
1. **Deletion Tool** → Remove unwanted pages
2. **Rotation Tool** → Adjust page orientation
3. **Watermark Tool** → Add copyright information

## 🚀 Features

- **User-friendly GUI**: Intuitive interfaces for all tools
- **Chinese Support**: Perfect Chinese character handling in watermarks
- **Flexible Input**: Support for various page selection formats
- **Safety First**: Multiple validation checks to prevent data loss
- **Batch Processing**: Handle multiple operations efficiently
- **Cross-platform**: Works on macOS (with potential for other platforms)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📞 Support

If you encounter any problems:
1. Check the Chinese documentation in `项目总结.md`
2. Run the test scripts to verify setup
3. Ensure virtual environment is activated
4. Verify file paths are correct

## 🎉 Summary

You now have three fully-featured PDF processing tools:
- **Watermark Tool**: Perfect Chinese support with customizable watermarks
- **Rotation Tool**: Flexible page rotation with batch and precise control
- **Page Deletion Tool**: Safe page deletion with multiple deletion modes

All tools are thoroughly tested, have unified interfaces, and are simple to operate. They can be used individually or in combination to meet various PDF processing needs!
