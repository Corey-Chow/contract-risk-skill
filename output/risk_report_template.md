# 合同交付风险检查报告

**审查日期**: {{date}}  
**合同名称**: {{contract_name}}  
**审查人**: {{reviewer}}

---

## 📊 综合评估

| 指标 | 值 |
|------|-----|
| 风险评分 | **{{score}}/100** |
| 高风险项 | {{high_count}} 项 |
| 中风险项 | {{medium_count}} 项 |
| 低风险项 | {{low_count}} 项 |
| 承接建议 | **{{recommendation}}** |

---

## 🔴 高风险项（必须谈判修改）

| 序号 | 风险维度 | 风险描述 | 涉及条款 | 应对建议 |
|------|----------|----------|----------|----------|
{{#high_risks}}
| {{index}} | {{dimension}} | {{description}} | {{clause}} | {{suggestion}} |
{{/high_risks}}

---

## 🟡 中风险项（建议争取优化）

| 序号 | 风险维度 | 风险描述 | 涉及条款 | 应对建议 |
|------|----------|----------|----------|----------|
|------|----------|----------|----------|----------|
{{#medium_risks}}
| {{index}} | {{dimension}} | {{description}} | {{clause}} | {{suggestion}} |
{{/medium_risks}}

---

## 🟢 低风险项（保持关注）

| 序号 | 风险维度 | 风险描述 | 涉及条款 | 应对建议 |
|------|----------|----------|----------|----------|
{{#low_risks}}
| {{index}} | {{dimension}} | {{description}} | {{clause}} | {{suggestion}} |
{{/low_risks}}

---

## 📋 谈判优先级建议

### 第一优先级（必须修改）
{{#must_negotiate}}
- [ ] {{item}}
{{/must_negotiate}}

### 第二优先级（建议争取）
{{#should_negotiate}}
- [ ] {{item}}
{{/should_negotiate}}

### 可接受条款
{{#acceptable}}
- [ ] {{item}}
{{/acceptable}}

---

## 📝 审查说明

{{notes}}

---

*本报告由 contract-risk-skill 自动生成*
