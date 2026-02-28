# Contract Risk Agent Tool - 使用指南

## ✅ 已完成

- [x] 目录结构创建
- [x] Python 后端开发（parser, llm_client, report_gen, agent_tool）
- [x] TypeScript 工具定义（check-contract.ts）
- [x] Agent Skills 定义（contract-review/SKILL.md）
- [x] Custom Commands 定义（check-contract.md）
- [x] opencode 配置（config.jsonc）
- [x] 依赖安装（rich, openai, PyYAML, PyPDF2, python-docx）

## ⚠️ 待完成

### 1. API Key 激活

当前 API Key (`sk-sp-79650bdac4ba4b59a20a7dbcd132913f`) 认证失败，需要：

1. 访问 [阿里云百炼控制台](https://bailian.console.aliyun.com/)
2. 确认 API Key 已激活并有额度
3. 确认模型 `qwen3.5-plus` 已开通

或者：
- 访问 [opencode.ai/auth](https://opencode.ai/auth) 获取新的 API Key
- 更新 `config.yaml` 中的 `api_key`

### 2. PDF 生成依赖（可选）

如需 PDF 报告输出，需要安装：
```bash
pip install weasyprint
```

注意：weasyprint 需要 GTK+ 运行时，Windows 安装较复杂。建议仅使用 Markdown 输出。

## 📋 使用方式

### 方式 1：CLI 直接调用（立即可用）

```bash
cd "D:\Documents\PM Skills\contract-risk-skill"

# 解析合同（测试通过）
python -c "from src.parser import parse_document; print(parse_document('contracts/【清洁版 - 终稿】合肥晶合项目 云原生合同 V3.0-by Lqy 1230-v1 (1).docx')[:500])"

# 完整审查（需要 API Key）
python src/agent_tool.py check-contract --file "合肥晶合" --format markdown
```

### 方式 2：opencode 命令调用（需要配置）

在 opencode TUI 中：

```
/check-contract 合肥晶合项目.docx
```

**配置步骤**：

1. 复制配置到 opencode 目录：
```powershell
# Windows PowerShell
Copy-Item .opencode\config.jsonc "$env:USERPROFILE\.config\opencode\config.jsonc" -Force
Copy-Item .opencode\tools\ -Destination "$env:USERPROFILE\.config\opencode\tools\" -Recurse -Force
Copy-Item .opencode\skills\ -Destination "$env:USERPROFILE\.config\opencode\skills\" -Recurse -Force
Copy-Item .opencode\commands\ -Destination "$env:USERPROFILE\.config\opencode\commands\" -Recurse -Force
```

2. 重启 opencode

3. 测试命令：
```
/check-contract 合肥晶合
```

### 方式 3：Agent 对话调用

在 opencode 对话中直接说：

```
请帮我审查一下合肥晶合项目的合同风险
```

Agent 会自动发现 `contract-review` 技能并调用。

## 📁 文件说明

```
contract-risk-skill/
├── .opencode/
│   ├── tools/check-contract.ts       # TypeScript 工具（opencode 调用）
│   ├── skills/contract-review/
│   │   └── SKILL.md                   # Agent 技能定义
│   ├── commands/check-contract.md     # 自定义命令
│   └── config.jsonc                   # opencode 配置
│
├── src/
│   ├── agent_tool.py                  # CLI 主入口
│   ├── parser.py                      # 文档解析（DOCX/PDF→Markdown）
│   ├── llm_client.py                  # Qwen API 调用
│   └── report_gen.py                  # 报告生成（MD+PDF）
│
├── contracts/                         # 合同文件
├── knowledge/risk_patterns.md         # 风险知识库
├── output/                            # 报告输出
├── config.yaml                        # 配置文件
├── requirements.txt                   # Python 依赖
└── README.md                          # 项目说明
```

## 🔧 故障排除

### Q1: API Key 认证失败
**错误**: `AuthenticationError: Error code: 401`

**解决**:
1. 检查 `config.yaml` 中 API Key 是否正确
2. 访问阿里云百炼控制台确认 API Key 已激活
3. 确认模型 `qwen3.5-plus` 已开通

### Q2: 找不到合同文件
**错误**: `FileNotFoundError`

**解决**:
1. 确保合同文件在 `contracts/` 目录下
2. 使用完整路径或文件名关键词
3. 支持中文文件名

### Q3: opencode 找不到命令
**错误**: 输入 `/check-contract` 无响应

**解决**:
1. 确认 `.opencode/` 目录已复制到用户配置目录
2. 重启 opencode
3. 检查 `~/.config/opencode/config.jsonc` 权限配置

### Q4: PDF 生成失败
**错误**: `weasyprint` 未安装

**解决**:
1. 使用 `--format markdown` 仅生成 Markdown
2. 或安装 weasyprint（复杂，Windows 需要 GTK+）
3. 建议使用 Markdown 查看器打开报告

## 📝 输出示例

### Markdown 报告

```markdown
# 合同交付风险检查报告

**审查日期**: 2026 年 02 月 27 日
**合同名称**: 合肥晶合项目
**审查人**: AI 交付风险审查专家

## 📊 综合评估

| 指标 | 值 |
|------|-----|
| 风险评分 | **55/100** |
| 高风险项 | 2 项 |
| 中风险项 | 3 项 |
| 低风险项 | 2 项 |
| 承接建议 | **🟠 较高风险，需谨慎评估** |

## 🔴 高风险项（必须谈判修改）

| 序号 | 风险维度 | 风险描述 | 涉及条款 | 应对建议 |
|------|----------|----------|----------|----------|
| 1 | 付款条款风险 | 无预付款... | 3.2 付款条款 | 争取 10-20%... |

...
```

## 🚀 下一步

1. **激活 API Key** → 访问阿里云百炼控制台
2. **配置 opencode** → 复制 `.opencode/` 到用户目录
3. **测试完整流程** → 运行 `python src/agent_tool.py check-contract ...`
4. **开始使用** → 在 opencode 中调用 `/check-contract`

## 💡 技术支持

- API Key 问题：阿里云百炼文档 https://help.aliyun.com/zh/model-studio/
- opencode 使用：https://opencode.ai/docs/commands/
- 本项目问题：查看 `src/` 源代码或修改 `knowledge/risk_patterns.md` 调整风险模式
