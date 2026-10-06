# Karpathy Output · 中文讲解与可视化：本地安装说明

技能名：`karpathy-output-style-zh`

这个包用于把同一套讲解规则带到你自己的本地 Codex。下载或解压 ZIP 本身不会安装技能，也不会让它在每次对话中自动加载。

## 最省事的安装方法

把这个 ZIP 下载到本地，交给能访问该文件的本地 Codex，并发送：

> 请安装这个包里的 karpathy-output-style-zh 技能。先检查本机 Codex 的版本、实际技能发现路径和已有同名技能，再把完整技能文件夹放入本机支持的个人技能目录。保留许可证和已有文件；若有不同内容的同名技能，先给我看差异，不要直接覆盖。只安装这个技能，不修改 AGENTS.md 或其他设置。最后验证文件完整、名称可发现，并显式调用一次，分别说明哪些检查完成、哪些尚未验证。

截至 2026-10-05，官方本地技能文档列出的个人目录是 `$HOME/.agents/skills`，项目目录是 `.agents/skills`。Windows 原生环境与 WSL 的用户目录可能不同；让本地 Codex 确认当前环境的实际路径，再操作。不要因为看到了另一台机器的示例路径就照抄。

安装目标应有以下结构：

```text
karpathy-output-style-zh/
  SKILL.md
  LICENSE.upstream
  agents/
    openai.yaml
```

`INSTALL.zh-CN.md` 是给人看的安装说明，不需要放进技能目录。

## 怎么用

可靠的显式调用：

`用 $karpathy-output-style-zh 解释移动平均。先给结论，再用同一个例子说明输入、过程、输出。`

接着说：

`可视化：让我调窗口大小，看看结果怎样变化。`

在支持技能选择器的界面中，也可以先选择“Karpathy Output · 中文讲解与可视化”。本技能保留默认的自动匹配能力；但“已安装”“这次被加载”“这次输出有效”是三个不同的检查，不能相互替代。“可视化”是会话约定，不是后台开关。

## 可选：把清晰表达作为日常默认

如果你希望普通对话也总是采用清晰表达，可以另行让本地 Codex 展示一个 AGENTS.md 的追加方案，确认后再写入。先读取原有内容和实际生效的文件，不覆盖现有配置，也不自行新建优先级更高的覆盖文件。

可供你审核的短片段：

> 解释概念与方案时，先给答案，使用简单具体的语言和一致术语，保留前提、因果、例外与不确定性。复杂过程尽量用同一个例子贯穿输入、过程和输出；简单问题直接回答。我明确说“可视化”时，使用 karpathy-output-style-zh 技能，并按问题选择最有帮助的视觉形式。不强制每次建网页、做视频或测验。

这一步是可选配置，需要你另外同意；安装技能本身不包含这项修改。

## 来源与范围

本技能参考并改编了 Ashrya Agrawal 的 MIT 项目 [Karpathy Output Style](https://github.com/ashryaagr/karpathy-output-style)，并保留其许可。它把清晰表达与视觉讲解适配为中文对话、统一触发和轻量媒介选择，不声称这些思路是首创或已经证明优于其他技能。

- [Karpathy 原帖](https://x.com/karpathy/status/2105819303471976479)
- [上游项目说明](https://github.com/ashryaagr/karpathy-output-style/blob/main/README.md)
- [上游现有演示视频](https://github.com/ashryaagr/karpathy-output-style/blob/main/examples/diffusion/video/explainer.mp4)：这是上游作者的作品，不是本技能的测试视频。
- [相关中文项目](https://github.com/mzopedia/simplified-technical-chinese)：这里仅列为相关工作，未复制它的文字、词表或检查器。
- [官方技能发现文档](https://learn.chatgpt.com/docs/build-skills)
- [官方 AGENTS.md 文档](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

包中只有技能说明、界面元数据和上游许可，不包含上游脚本、服务连接配置、API 密钥、推文图片或视频文件。视觉效果取决于当前环境可用工具；技能不会自行授予付费服务、软件安装、上传或公开发布的权限。
