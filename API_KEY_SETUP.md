# 🔑 API Key 配置指南

## 当前状态

## 解决方案

### 方案 1：阿里云百炼控制台（推荐）

1. **访问控制台**
   - 网址：https://bailian.console.aliyun.com/
   
2. **登录/注册**
   - 使用阿里云账号登录
   
3. **开通模型服务**
   - 进入"模型广场"
   - 搜索并开通：**Qwen3.5-Plus**
   
4. **创建 API Key**
   - 进入"API-KEY 管理"
   - 点击"创建新的 API-KEY"
   - 复制生成的 Key（格式：`sk-xxxxxxxxxxxxxxxx`）

5. **更新配置**
   ```bash
   # 编辑 config.yaml
   notepad config.yaml
   
   # 替换第 5 行的 api_key 值
   alibaba_cloud:
     api_key: "sk-新的 API Key"
   ```

6. **测试连接**
   ```bash
   python -c "from openai import OpenAI; c = OpenAI(api_key='sk-新 Key', base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'); print(c.chat.completions.create(model='qwen3.5-plus', messages=[{'role':'user','content':'hi'}]).choices[0].message.content)"
   ```

---

### 方案 2：opencode.ai（快速）

1. **访问认证页面**
   - 网址：https://opencode.ai/auth
   
2. **注册/登录**
   - 使用 GitHub 或邮箱注册
   
3. **获取 API Key**
   - 登录后进入 Dashboard
   - 复制 API Key
   
4. **更新配置**
   ```bash
   notepad config.yaml
   ```
   将 `api_key` 替换为新的 Key

---

### 方案 3：使用演示模式（临时）

如果暂时不需要 AI 实时审查，可以继续使用演示模式。

编辑 `demo_review.py` 中的 `demo_result` 变量，预设您想要的审查结果。

---

## 验证成功

运行以下命令测试：
```bash
cd "D:\Documents\PM Skills\contract-risk-skill"
python src/agent_tool.py check-contract --file "合肥晶合"
```

成功的输出应该包含：
```
✓ 解析合同... 100%
✓ AI 审查中... 100%
✓ 生成报告... 100%
✓ 审查完成！
```

---

## 常见问题

### Q: API Key 格式不对？
A: 正确格式：`sk-` 开头，后跟 32 位字母数字组合

### Q: 提示模型未开通？
A: 需要在阿里云百炼控制台开通 Qwen3.5-Plus 模型

### Q: 有免费额度吗？
A: 新用户通常有免费试用额度，具体查看控制台

### Q: 费用如何计算？
A: 按 Token 计费，Qwen3.5-Plus 约 0.004 元/千 Token（输入）+ 0.012 元/千 Token（输出）
   单次合同审查约 1-2 元

---

## 获取帮助

- 阿里云百炼文档：https://help.aliyun.com/zh/model-studio/
- API 错误码：https://help.aliyun.com/zh/model-studio/developer-reference/error-code
- 本项目问题：查看 `USAGE.md`
