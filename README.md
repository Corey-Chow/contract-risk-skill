# Contract Risk Agent Tool

合同交付风险审查 Agent 工具，支持通过 opencode 对话调用。

## ⚡ 快速开始

### 1. AI 实时审查（已激活 ✅）

```bash
cd "D:\Documents\PM Skills\contract-risk-skill"
python src/agent_tool.py check-contract --file "合同文件名"
```

**API 配置**:
- 端点：`https://coding.dashscope.aliyuncs.com/v1` ✅
- 模型：`qwen3.5-plus`
- 状态：**实时 AI 审查已激活**

### 2. 在 opencode 中调用

```
/check-contract 合同文件名
```

或自然语言：
```
请帮我审查一下这个合同的 risk
```

- ✅ **6 大风险维度审查**：交付周期、人员、验收标准、付款条款、变更管理、法律合规
- ✅ **风险等级评估**：高/中/低三级分类
- ✅ **智能评分系统**：自动计算风险评分（0-100）
- ✅ **结构化报告**：Markdown + PDF 双格式输出
- ✅ **谈判建议**：自动生成谈判优先级清单

## 调用方式

### 方式 1：opencode 命令调用（推荐）

在 opencode TUI 中输入：

```
/check-contract 合同文件名
```

示例：
```
/check-contract 合肥晶合项目.docx
```

### 方式 2：Agent 对话调用

直接对 Agent 说：

```
请帮我审查一下合肥晶合项目的合同风险
```

Agent 会自动调用 `contract-review` 技能执行审查。

### 方式 3：CLI 直接调用

```bash
cd "D:\Documents\PM Skills\contract-risk-skill"
python src/agent_tool.py check-contract --file "合肥晶合项目.docx"
```

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Node.js 依赖（用于 opencode 工具）

```bash
bun install
```

### 3. 配置 API Key

编辑 `config.yaml`，确保 API Key 正确：

```yaml
alibaba_cloud:
  api_key: "sk-sp-79650bdac4ba4b59a20a7dbcd132913f"
```

### 4. 复制 opencode 配置到用户目录

```bash
# Windows PowerShell
Copy-Item .opencode/config.jsonc $env:USERPROFILE\.config\opencode\config.jsonc -Force
```

或者在 opencode 中运行：
```
/opencode config
```

然后添加配置内容。

## 目录结构

```
contract-risk-skill/
├── .opencode/
│   ├── tools/
│   │   └── check-contract.ts      # TypeScript 工具定义
│   ├── skills/
│   │   └── contract-review/
│   │       └── SKILL.md           # Agent 技能定义
│   ├── commands/
│   │   └── check-contract.md      # 自定义命令
│   └── config.jsonc               # opencode 配置
│
├── src/
│   ├── agent_tool.py              # Python CLI 入口
│   ├── parser.py                  # 文档解析模块
│   ├── llm_client.py              # Qwen API 封装
│   └── report_gen.py              # 报告生成模块
│
├── contracts/                     # 合同文件
├── knowledge/
│   └── risk_patterns.md           # 风险模式知识库
├── output/                        # 报告输出
├── config.yaml                    # 配置文件
└── README.md
```

## 输出示例

### 风险评分
```
风险评分：55/100
承接建议：🟠 较高风险，需谨慎评估
```

### 风险清单
```
🔴 高风险项（2 项）
- 付款账期 60 天，现金流压力大
- 无预付款，启动资金压力

🟡 中风险项（3 项）
- 交付周期无缓冲
- 验收标准主观
- 违约金不对等
```

### 谈判建议
```
第一优先级（必须修改）
- [ ] 付款账期压缩至 30 天
- [ ] 争取 10-20% 预付款

第二优先级（建议争取）
- [ ] 增加交付缓冲条款
- [ ] 量化验收标准
```

## 常见问题

### Q: 提示找不到文件？
A: 确保合同文件在 `contracts/` 目录下，或使用完整路径。

### Q: PDF 生成失败？
A: 安装 weasyprint：`pip install weasyprint`（需要额外依赖）

### Q: API 调用失败？
A: 检查 `config.yaml` 中的 API Key 是否正确，网络是否通畅。

### Q: opencode 找不到命令？
A: 确保 `.opencode/` 目录存在，且已重启 opencode。

## 扩展开发

### 添加新的风险模式

编辑 `knowledge/risk_patterns.md`，按现有格式添加新条目。

### 修改报告模板

编辑 `src/report_gen.py` 中的 `to_markdown()` 方法。

### 自定义 Prompt

编辑 `src/llm_client.py` 中的 `_build_system_prompt()` 方法。

## 技术栈

- **Python**: 文档解析、API 调用、报告生成
- **TypeScript**: opencode 工具定义
- **Qwen3.5-Plus**: AI 风险审查
- **OpenAI 兼容 API**: 阿里云百炼平台

## License

MIT
