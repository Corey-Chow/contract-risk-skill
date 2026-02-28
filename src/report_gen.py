#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成模块
支持 Markdown 和 PDF 格式
"""

import json
from pathlib import Path
from datetime import datetime


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, output_path: str):
        """
        初始化报告生成器
        
        Args:
            output_path: 输出文件路径（不含扩展名）
        """
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def to_markdown(self, result: dict) -> str:
        """
        生成 Markdown 报告
        
        Args:
            result: 审查结果字典
            
        Returns:
            生成的 Markdown 内容
        """
        now = datetime.now().strftime("%Y 年 %m 月 %d 日")
        
        # 计算风险项数量
        high_count = len(result.get("high_risks", []))
        medium_count = len(result.get("medium_risks", []))
        low_count = len(result.get("low_risks", []))
        
        # 构建 Markdown 内容
        content = f"""# 合同交付风险检查报告

**审查日期**: {now}  
**合同名称**: {self.output_path.stem.replace('risk_report_', '')}  
**审查人**: AI 交付风险审查专家

---

## 📊 综合评估

| 指标 | 值 |
|------|-----|
| 风险评分 | **{result.get('score', 0)}/100** |
| 高风险项 | {high_count} 项 |
| 中风险项 | {medium_count} 项 |
| 低风险项 | {low_count} 项 |
| 承接建议 | **{result.get('recommendation', '待评估')}** |

---

## 🔴 高风险项（必须谈判修改）

"""
        high_risks = result.get("high_risks", [])
        if high_risks:
            content += "| 序号 | 风险维度 | 风险描述 | 涉及条款 | 应对建议 |\n"
            content += "|------|----------|----------|----------|----------|\n"
            for risk in high_risks:
                content += f"| {risk.get('index', '')} | {risk.get('dimension', '')} | {risk.get('description', '')} | {risk.get('clause', '')} | {risk.get('suggestion', '')} |\n"
        else:
            content += "无\n"
        
        content += f"""
---

## 🟡 中风险项（建议争取优化）

"""
        medium_risks = result.get("medium_risks", [])
        if medium_risks:
            content += "| 序号 | 风险维度 | 风险描述 | 涉及条款 | 应对建议 |\n"
            content += "|------|----------|----------|----------|----------|\n"
            for risk in medium_risks:
                content += f"| {risk.get('index', '')} | {risk.get('dimension', '')} | {risk.get('description', '')} | {risk.get('clause', '')} | {risk.get('suggestion', '')} |\n"
        else:
            content += "无\n"
        
        content += f"""
---

## 🟢 低风险项（保持关注）

"""
        low_risks = result.get("low_risks", [])
        if low_risks:
            content += "| 序号 | 风险维度 | 风险描述 | 涉及条款 | 应对建议 |\n"
            content += "|------|----------|----------|----------|----------|\n"
            for risk in low_risks:
                content += f"| {risk.get('index', '')} | {risk.get('dimension', '')} | {risk.get('description', '')} | {risk.get('clause', '')} | {risk.get('suggestion', '')} |\n"
        else:
            content += "无\n"
        
        # 谈判优先级建议
        negotiation_tips = result.get("negotiation_tips", {})
        content += f"""
---

## 📋 谈判优先级建议

### 第一优先级（必须修改）

"""
        for item in negotiation_tips.get("must", []):
            content += f"- [ ] {item}\n"
        
        content += "\n### 第二优先级（建议争取）\n\n"
        for item in negotiation_tips.get("should", []):
            content += f"- [ ] {item}\n"
        
        content += "\n### 可接受条款\n\n"
        for item in negotiation_tips.get("acceptable", []):
            content += f"- [ ] {item}\n"
        
        # 审查说明
        content += f"""
---

## 📝 审查说明

{result.get('notes', '无')}

---

*本报告由 contract-risk-skill 自动生成*
*审查依据：knowledge/risk_patterns.md 风险模式库*
"""
        
        # 写入文件
        md_path = self.output_path.with_suffix('.md')
        md_path.write_text(content, encoding='utf-8')
        
        return content
    
    def to_pdf(self, result: dict) -> str:
        """
        生成 PDF 报告
        
        Args:
            result: 审查结果字典
            
        Returns:
            PDF 文件路径
        """
        try:
            from weasyprint import HTML, CSS
            
            # 先生成 Markdown
            md_content = self.to_markdown(result)
            
            # 转换为 HTML
            import markdown
            html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
            
            html_full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>合同交付风险检查报告</title>
    <style>
        @page {{
            size: A4;
            margin: 2.5cm;
        }}
        body {{
            font-family: "Microsoft YaHei", "SimHei", sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .high-risk {{
            color: #e74c3c;
        }}
        .medium-risk {{
            color: #f39c12;
        }}
        .low-risk {{
            color: #27ae60;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""
            
            # 生成 PDF
            pdf_path = self.output_path.with_suffix('.pdf')
            HTML(string=html_full, encoding='utf-8').write_pdf(str(pdf_path))
            
            return str(pdf_path)
            
        except ImportError:
            # weasyprint 未安装时返回 None
            return None
        except Exception as e:
            print(f"PDF 生成失败：{e}")
            return None
