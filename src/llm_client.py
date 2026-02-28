#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen API 客户端
调用阿里云百炼 Qwen3.5-Plus 进行合同风险审查
"""

import json
import yaml
from pathlib import Path
from openai import OpenAI


class QwenClient:
    """Qwen API 客户端"""
    
    def __init__(self, config_path: str = None):
        """初始化客户端"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        aliyun_config = self.config['alibaba_cloud']
        
        self.client = OpenAI(
            api_key=aliyun_config['api_key'],
            base_url=aliyun_config['base_url'],
        )
        self.model = aliyun_config['model']
        
        # 加载风险模式知识库
        self.risk_patterns = self._load_risk_patterns()
    
    def _load_risk_patterns(self) -> str:
        """加载风险模式知识库"""
        patterns_path = Path(__file__).parent.parent / "knowledge" / "risk_patterns.md"
        if patterns_path.exists():
            return patterns_path.read_text(encoding='utf-8')
        return ""
    
    def _build_system_prompt(self) -> str:
        """构建系统 Prompt"""
        return """你是合同交付风险审查专家，拥有 10+ 年项目交付管理经验。

请严格按照以下规则审查合同：

1. 从 6 大维度分析风险：
   - 交付周期风险：时间表、里程碑、关键路径
   - 人员风险：资质、配置、稳定性
   - 验收标准风险：量化标准、SLA、测试环境
   - 付款条款风险：节点、账期、质保金
   - 变更管理风险：流程、定价、审批
   - 法律合规风险：IP、保密、违约责任

2. 风险等级判定标准：
   - 高风险 (🔴)：可能导致项目失败、重大损失或法律纠纷，必须谈判修改
   - 中风险 (🟡)：可能影响项目利润、进度或客户满意度，建议争取优化
   - 低风险 (🟢)：影响可控，可接受或通过内部管理消化

3. 风险评分计算：
   - 高风险项 × 20 分 + 中风险项 × 10 分 + 低风险项 × 5 分 = 风险总分

4. 承接建议标准：
   - 0-20 分：🟢 低风险，可承接
   - 21-40 分：🟡 中风险，建议谈判后承接
   - 41-60 分：🟠 较高风险，需谨慎评估
   - 61+ 分：🔴 高风险，不建议承接

5. 输出要求：
   - 必须基于合同原文分析，不得臆造条款
   - 引用风险点时需注明条款位置
   - 高风险项必须提供应对建议
   - 严格按 JSON 格式输出

请参考以下风险模式知识库：
""" + self.risk_patterns
    
    def _build_user_prompt(self, contract_text: str) -> str:
        """构建用户 Prompt"""
        return f"""请审查以下合同内容：

---
{contract_text[:15000]}
---

请按以下 JSON 格式输出审查结果（不要输出其他内容）：

{{
  "high_risks": [
    {{
      "index": 1,
      "dimension": "风险维度",
      "description": "风险描述",
      "clause": "涉及条款",
      "suggestion": "应对建议"
    }}
  ],
  "medium_risks": [...],
  "low_risks": [...],
  "score": 0,
  "recommendation": "承接建议",
  "negotiation_tips": {{
    "must": ["必须修改的条款"],
    "should": ["建议争取的条款"],
    "acceptable": ["可接受的条款"]
  }},
  "notes": "审查说明和建议"
}}

注意：
1. 所有字段必须填写
2. 风险项数组可以为空但不能缺失
3. score 必须是数字（0-100）
4. recommendation 必须是以下之一："🟢 低风险，可承接"、"🟡 中风险，建议谈判后承接"、"🟠 较高风险，需谨慎评估"、"🔴 高风险，不建议承接"
"""
    
    def review_contract(self, contract_text: str, max_retries: int = 3) -> dict:
        """
        审查合同
        
        Args:
            contract_text: 合同文本
            max_retries: 最大重试次数
            
        Returns:
            审查结果字典
        """
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(contract_text)
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"},
                )
                
                result = json.loads(response.choices[0].message.content)
                
                # 验证必要字段
                required_fields = ["high_risks", "medium_risks", "low_risks", 
                                   "score", "recommendation", "negotiation_tips", "notes"]
                for field in required_fields:
                    if field not in result:
                        raise ValueError(f"缺少必要字段：{field}")
                
                return result
                
            except json.JSONDecodeError as e:
                if attempt < max_retries - 1:
                    continue
                raise ValueError(f"API 返回格式错误：{e}")
            except Exception as e:
                error_msg = str(e)
                if attempt < max_retries - 1:
                    continue
                # 包装错误信息避免编码问题
                raise Exception(f"API 调用失败 ({type(e).__name__})")
        
        raise Exception("达到最大重试次数，审查失败")
