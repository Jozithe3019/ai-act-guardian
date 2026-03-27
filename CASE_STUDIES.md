
# 🛡️ AI-Act-Guardian Case Studies / 案例分析

This document contains real-world audit examples conducted by the AI-Act-Guardian engine.

---

## Case 01: Multi-Agent Medical Assistant (General Audit)
**Target**: [GitHub Project: Multi-Agent-Medical-Assistant](https://github.com/souvikmajumder26/Multi-Agent-Medical-Assistant)

### 📊 Executive Summary
The target project exhibited significant compliance gaps. While technically sophisticated, the implementation risks fines of up to **€35M** or **7% global turnover** due to critical GDPR leaks and high-risk regulatory failures.

### 🚩 Key Findings
- **PII Leakage**: Raw patient queries and medical history are leaked into unencrypted system logs via `logging.info` in `rag_agent`.
- **Transparency Failure**: Failed to provide mandatory AI disclosure tags in output structures (Art 52).
- **Doc Gap**: Absence of mandatory Risk Management System and Technical Model Cards (Art 9 & 11).

---

## Case 02: Deep Dive - Brain Tumor Diagnostic Module
**Target**: Specific orchestration logic in `agent_decision.py`

### 📊 Critical Logic Vulnerabilities
- **Logic Void**: The core brain tumor inference engine was found to be a mocked/empty placeholder, yet it presented results as valid. (Violation of Art 11 & 15).
- **Pseudo-HITL**: The "Human-in-the-loop" mechanism allowed patients to self-validate their own cancer diagnoses. (Violation of Art 14 requirement for *professional* oversight).
- **Data Taint**: Sensitive MRI data paths were identified without corresponding encryption or masking sinks in the processing pipeline.

---

## 🛡️ 案例 01：多智能体医疗助手（全局审计）
**目标**：[GitHub 项目：Multi-Agent-Medical-Assistant](https://github.com/souvikmajumder26/Multi-Agent-Medical-Assistant)

### 📊 执行摘要
目标项目存在显著的合规性缺口。虽然在技术上非常先进，但目前的实现面临高达 **3500 万欧元**或**全球年营业额 7%** 的罚款风险，原因是致命的 GDPR 隐私泄露和高风险监管失效。

### 🚩 核心发现
- **PII 隐私泄露**：原始患者查询和医疗病史通过 `rag_agent` 中的 `logging.info` 直接泄露到未加密的系统日志中。
- **透明度失效**：未能按法案第 52 条要求，在输出结构中提供强制性的 AI 身份披露。
- **文档缺失**：缺少法定的风险管理系统和技术模型卡片 (第 9 和第 11 条)。

---

## 案例 02：深度拆解 - 脑肿瘤诊断模块
**目标**：`agent_decision.py` 中的核心路由逻辑

### 📊 致命逻辑漏洞
- **逻辑空洞**：核心脑肿瘤推理引擎被发现是 Mock 的空占位符，却将结果作为有效诊断呈现。(违反第 11 和第 15 条关于准确性的规定)。
- **虚假人类干预 (HITL)**：所谓的人类干预机制竟然允许患者自行确认其癌症诊断结果。(违反第 14 条关于“专业人员监督”的要求)。
- **数据污点**：识别出敏感的 MRI 数据路径，但在处理管线中缺乏相应的加密或脱敏处理 (Sink 缺失)。
