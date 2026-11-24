# 行为评测

每个 JSON 对应一个 Skill。task 是任务意图，fixture 描述输入或仓库状态，expect 和 forbid 定义可接受行为及禁止行为。这些是评测定义，不是已执行测试。

执行时使用临时 Git 仓库或独立材料，为每个用例构建 fixture，记录 Skill 版本、模型及工具调用。Git 场景比较执行前后的 HEAD、Index、工作区、远端和 hooks 状态；写作场景人工或独立评审事实保留及任务边界。

每个 expect 均满足且无 forbid 行为才通过；提交消息按语义评估，不要求字符串完全匹配。记录 PASS / FAIL / BLOCKED 及证据。静态脚本仅检查用例数据格式，不调用模型。
