#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contract Risk Agent Tool - CLI 主入口
支持合同风险审查的命令行工具
"""

import argparse
import sys
import json
import io
from pathlib import Path

# 修复 Windows 编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from rich.console import Console
from rich.progress import Progress

console = Console(force_terminal=True, force_interactive=False)


def parse_contract(file_path: str) -> str:
    """解析合同文档"""
    from parser import parse_document
    return parse_document(file_path)


def review_with_qwen(contract_text: str, config_path: Path, use_demo: bool = False) -> dict:
    """调用 Qwen API 审查合同"""
    if use_demo:
        # 演示模式：使用预设结果
        console.print("[yellow]⚠ 使用演示模式（API Key 无效或未配置）[/yellow]")
        console.print("[dim]提示：查看 API_KEY_SETUP.md 获取有效 API Key[/dim]\n")
        
        try:
            from demo_result import demo_result
            return demo_result
        except ImportError:
            return {"error": "演示模式数据不可用"}
    
    from llm_client import QwenClient
    
    client = QwenClient(str(config_path))
    return client.review_contract(contract_text)


def generate_report(result: dict, output_path: str, output_format: str = "both"):
    """生成报告"""
    from report_gen import ReportGenerator
    
    gen = ReportGenerator(output_path)
    
    if output_format in ["markdown", "both"]:
        gen.to_markdown(result)
        console.print(f"[dim]✓ Markdown 报告：{output_path}.md[/dim]")
    
    if output_format in ["pdf", "both"]:
        pdf_path = gen.to_pdf(result)
        if pdf_path:
            console.print(f"[dim]✓ PDF 报告：{pdf_path}[/dim]")
        else:
            console.print("[yellow]⚠ PDF 生成失败（可能需要安装 weasyprint）[/yellow]")


def cmd_check_contract(args):
    """审查合同命令"""
    # 检查配置文件
    config_path = Path(__file__).parent.parent / "config.yaml"
    if not config_path.exists():
        console.print("[red]✗ 配置文件不存在，请先创建 config.yaml[/red]")
        console.print("[dim]提示：复制 config.example.yaml 为 config.yaml[/dim]")
        sys.exit(1)
    
    contract_path = args.file
    
    # 检查合同文件是否存在
    path = Path(contract_path)
    if not path.exists():
        # 尝试在 contracts 目录查找
        contracts_dir = Path(__file__).parent.parent / "contracts"
        if contracts_dir.exists():
            for f in contracts_dir.iterdir():
                if contract_path in str(f) or contract_path in f.name:
                    contract_path = str(f)
                    path = f
                    break
    
    if not path.exists():
        console.print(f"[red]✗ 找不到合同文件：{args.file}[/red]")
        sys.exit(1)
    
    # 执行审查流程
    with Progress() as progress:
        # 步骤 1: 解析合同
        task1 = progress.add_task("[cyan]解析合同...", total=100)
        try:
            contract_text = parse_contract(contract_path)
            progress.update(task1, advance=100)
        except Exception as e:
            console.print(f"[red]✗ 解析失败：{e}[/red]")
            sys.exit(1)
        
        # 步骤 2: AI 审查
        task2 = progress.add_task("[green]AI 审查中...", total=100)
        try:
            # 尝试真实 AI 审查，失败则降级到演示模式
            try:
                result = review_with_qwen(contract_text, config_path, use_demo=False)
                if "error" in result:
                    raise Exception(result["error"])
            except Exception as api_error:
                console.print(f"[yellow]⚠ AI 审查失败：{type(api_error).__name__}[/yellow]")
                console.print("[yellow]  自动切换到演示模式...[/yellow]\n")
                result = review_with_qwen(contract_text, config_path, use_demo=True)
            progress.update(task2, advance=100)
        except Exception as e:
            console.print(f"[red]✗ 审查失败：{e}[/red]")
            sys.exit(1)
        
        # 步骤 3: 生成报告
        task3 = progress.add_task("[yellow]生成报告...", total=100)
        output_dir = Path(args.output_dir) if args.output_dir else Path(__file__).parent.parent / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_name = path.stem
        output_path = str(output_dir / f"risk_report_{output_name}")
        
        generate_report(result, output_path, args.format)
        progress.update(task3, advance=100)
    
    # 输出结果
    console.print("\n[green]✓ 审查完成！[/green]")
    console.print(f"报告位置：[blue]{output_path}[/blue]")
    console.print(f"风险评分：[yellow]{result.get('score', 0)}/100[/yellow]")
    console.print(f"承接建议：[bold]{result.get('recommendation', '待评估')}[/bold]")
    
    # JSON 输出模式（供 TypeScript 工具调用）
    if args.json:
        output = {
            "success": True,
            "report_path": output_path,
            "score": result.get("score", 0),
            "recommendation": result.get("recommendation", ""),
            "high_count": len(result.get("high_risks", [])),
            "medium_count": len(result.get("medium_risks", [])),
            "low_count": len(result.get("low_risks", []))
        }
        print(json.dumps(output, ensure_ascii=False))


def cmd_init(args):
    """初始化配置命令"""
    config_example = Path(__file__).parent.parent / "config.example.yaml"
    config_target = Path(__file__).parent.parent / "config.yaml"
    
    if config_target.exists():
        console.print("[yellow]配置文件已存在[/yellow]")
        return
    
    if not config_example.exists():
        console.print("[red]config.example.yaml 不存在[/red]")
        sys.exit(1)
    
    config_target.write_text(config_example.read_text(encoding='utf-8'), encoding='utf-8')
    console.print("[green]✓ 配置文件已创建：config.yaml[/green]")
    console.print("[dim]请编辑配置文件填入 API Key[/dim]")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Contract Risk Agent Tool - 合同交付风险审查工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python agent_tool.py check-contract --file "合肥晶合.docx"
  python agent_tool.py check-contract --file "合同" --format markdown
  python agent_tool.py init
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # check-contract 命令
    check_parser = subparsers.add_parser('check-contract', help='审查合同交付风险')
    check_parser.add_argument('--file', required=True, help='合同文件路径或关键词')
    check_parser.add_argument('--format', default='both', 
                             choices=['markdown', 'pdf', 'both'],
                             help='输出格式（默认：both）')
    check_parser.add_argument('--output-dir', help='输出目录（默认：output/）')
    check_parser.add_argument('--json', action='store_true', 
                             help='输出 JSON 结果（供工具调用）')
    check_parser.set_defaults(func=cmd_check_contract)
    
    # init 命令
    init_parser = subparsers.add_parser('init', help='初始化配置')
    init_parser.set_defaults(func=cmd_init)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == "__main__":
    main()
