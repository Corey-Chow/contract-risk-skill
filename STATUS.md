# ✅ Contract Risk Agent Tool 已启用！

## 📋 当前状态

### ✅ 功能正常
- ✅ 合同文档解析（DOCX/PDF → Markdown）
- ✅ 风险审查引擎（演示模式）
- ✅ 报告生成（Markdown）
- ✅ 自动降级机制（API 失败时切换演示模式）
- ✅ opencode 集成（Custom Tool + Skill + Command）

### ⏳ 待激活
- ⏳ AI 实时审查（需要有效 API Key）
- ⏳ PDF 报告生成（需要安装 weasyprint 依赖）

---

## 🚀 立即使用

### 方式 1：CLI 命令
```bash
cd "D:\Documents\PM Skills\contract-risk-skill"
python src/agent_tool.py check-contract --file "合同文件名"
```

**示例**:
```bash
python src/agent_tool.py check-contract --file "晶合项目"
```

**输出**:
```
✓ 解析合同... 100%
⚠ AI 审查失败：Exception
  自动切换到演示模式...
✓ Markdown 报告已生成：output/risk_report_xxx.md
✓ 审查完成！
风险评分：55/100
承接建议：🟠 较高风险，需谨慎评估
```

---

### 方式 2：opencode 对话
```
/check-contract 合同文件名
```

或自然语言：
```
请帮我审查一下晶合项目的合同风险
```

---

## 📊 审查结果示例

### 综合评估
| 指标 | 结果 |
|------|------|
| 风险评分 | **55/100** |
| 承接建议 | **🟠 较高风险，需谨慎评估** |
| 高风险项 | 2 项 🔴 |
| 中风险项 | 3 项 🟡 |
| 低风险项 | 2 项 🟢 |

### 高风险项（必须修改）
1. **付款条款风险** - 无预付款，首付款 30% 在培训完成后支付
2. **付款周期风险** - 所有付款均为收到发票后 60 天内

### 谈判优先级
**第一优先级（必须修改）**
- 付款账期压缩至 30 天
- 争取 10-20% 预付款
- 违约金对等

**第二优先级（建议争取）**
- 增加交付缓冲条款
- 量化验收标准
- 质保金降至 5%

---

## 📁 报告位置

生成的报告保存在：
```
output/risk_report_[合同名].md
```

使用 Markdown 查看器打开，或直接用文本编辑器查看。

---

## ⚠️ 演示模式说明

**当前状态**: 演示模式（预设审查结果）

**原因**: API Key 未激活

**影响**: 
- ✅ 可以查看报告格式和结构
- ✅ 可以测试完整工作流程
- ❌ 无法针对具体合同内容进行 AI 分析

**解决方案**: 查看 [API_KEY_SETUP.md](API_KEY_SETUP.md) 获取有效 API Key

---

## 🔧 启用 AI 实时审查

### 步骤 1：获取 API Key

选择以下任一方式：

**方案 A**: 阿里云百炼控制台
- 访问：https://bailian.console.aliyun.com/
- 开通 Qwen3.5-Plus 模型
- 创建 API Key

**方案 B**: opencode.ai
- 访问：https://opencode.ai/auth
- 注册/登录
- 复制 API Key

### 步骤 2：更新配置

编辑 `config.yaml`:
```yaml
alibaba_cloud:
  api_key: "sk-你的新 API Key"  # 替换这里
  base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  model: "qwen3.5-plus"
```

### 步骤 3:测试

```bash
python -c "from openai import OpenAI; c = OpenAI(api_key='sk-新 Key', base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'); print('✓ API OK:', c.chat.completions.create(model='qwen3.5-plus', messages=[{'role':'user','content':'hi'}]).choices[0].message.content)"
```

### 步骤 4: 运行

```bash
python src/agent_tool.py check-contract --file "晶合项目"
```

成功后会看到：
```
✓ 解析合同... 100%
✓ AI 审查中... 100%
✓ 生成报告... 100%
✓ 审查完成！
```

不再有 "演示模式" 提示。

---

## 🛠️ 故障排除

### 问题 1: 找不到文件
```
FileNotFoundError: 找不到文件
```
**解决**: 确保合同在 `contracts/` 目录，或使用完整路径

### 问题 2: 编码错误
```
UnicodeEncodeError
```
**解决**: 已自动修复，如仍有问题请以 UTF-8 编码运行

### 问题 3: API 认证失败
```
AuthenticationError: Error code: 401
```
**解决**: 查看 [API_KEY_SETUP.md](API_KEY_SETUP.md)

### 问题 4: opencode 找不到命令
```
未知命令：/check-contract
```
**解决**: 
1. 确认配置已复制到用户目录
2. 重启 opencode
3. 运行 `opencode --version` 确认版本

---

## 📚 文档索引

- [README.md](README.md) - 项目总览
- [USAGE.md](USAGE.md) - 详细使用指南
- [IMPLEMENTATION.md](IMPLEMENTATION.md) - 实施细节
- [API_KEY_SETUP.md](API_KEY_SETUP.md) - API Key 配置指南

---

## 🎯 下一步

1. **获取 API Key** → 访问 https://bailian.console.aliyun.com/
2. **更新配置** → 编辑 `config.yaml`
3. **测试 AI 审查** → 运行 `python src/agent_tool.py check-contract ...`

---

## 📞 支持

- **阿里云百炼文档**: https://help.aliyun.com/zh/model-studio/
- **opencode 文档**: https://opencode.ai/docs/commands/
- **项目问题**: 查看文档目录或源代码

---

**创建时间**: 2026 年 2 月 27 日  
**最后更新**: 2026 年 2 月 27 日  
**状态**: ✅ 已启用（演示模式），⏳ 等待 API Key 激活
