#!/usr/bin/env python3
"""测试合同审查流程"""

from pathlib import Path
from src.parser import parse_document
from src.report_gen import ReportGenerator

# 测试解析
contract_path = "contracts/【清洁版 - 终稿】合肥晶合项目 云原生合同 V3.0-by Lqy 1230-v1 (1).docx"
print(f"解析合同：{contract_path}")

text = parse_document(contract_path)
print(f"✓ 解析成功，文本长度：{len(text)} 字符")

# 保存解析结果
text_cache = Path("text_cache")
text_cache.mkdir(exist_ok=True)
output_file = text_cache / "contract.md"
output_file.write_text(text, encoding='utf-8')
print(f"✓ 已保存到：{output_file}")

# 创建测试报告
test_result = {
    "high_risks": [
        {
            "index": 1,
            "dimension": "付款条款风险",
            "description": "无预付款，首付款 30% 在培训完成后支付",
            "clause": "3.2 付款条款",
            "suggestion": "争取 10-20% 预付款"
        },
        {
            "index": 2,
            "dimension": "付款周期风险",
            "description": "所有付款节点均为收到发票后 60 天内",
            "clause": "3.2 付款条款",
            "suggestion": "压缩至 30 天内"
        }
    ],
    "medium_risks": [
        {
            "index": 1,
            "dimension": "交付周期风险",
            "description": "交付周期固定，未考虑甲方配合时间",
            "clause": "2.2 交付",
            "suggestion": "增加延期顺延条款"
        }
    ],
    "low_risks": [
        {
            "index": 1,
            "dimension": "质保金",
            "description": "质保金 10% 偏高",
            "clause": "3.2 付款条款",
            "suggestion": "可协商降至 5%"
        }
    ],
    "score": 55,
    "recommendation": "🟠 较高风险，需谨慎评估",
    "negotiation_tips": {
        "must": ["付款账期压缩至 30 天", "争取预付款"],
        "should": ["增加交付缓冲条款", "量化验收标准"],
        "acceptable": ["1 年质保期", "扩容阶梯价格"]
    },
    "notes": "测试报告 - 合同整体风险可控，但付款条件需要谈判"
}

# 生成报告
gen = ReportGenerator("output/test_risk_report")
md_content = gen.to_markdown(test_result)
print(f"✓ Markdown 报告已生成：output/test_risk_report.md")

# 尝试生成 PDF
try:
    pdf_path = gen.to_pdf(test_result)
    if pdf_path:
        print(f"✓ PDF 报告已生成：{pdf_path}")
    else:
        print("⚠ PDF 生成失败")
except Exception as e:
    print(f"⚠ PDF 生成失败：{e}")

print("\n测试完成！")
