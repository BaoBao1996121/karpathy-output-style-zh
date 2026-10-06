# Karpathy Output · 中文讲解与可视化

一个面向中文讲解的社区技能：先把答案讲清楚，再用同一个例子解释机制；需要时，把过程做成图解、交互 HTML 或动画。

**非官方项目，与 Andrej Karpathy 无隶属或背书关系。** 本项目参考并改编 [ashryaagr/karpathy-output-style](https://github.com/ashryaagr/karpathy-output-style)，保留其 MIT 许可。已有相关社区作品，因此不声称首创；目前也没有足够证据宣称效果优于上游。

## 直接下载

- [技能安装包 ZIP](https://github.com/BaoBao1996121/karpathy-output-style-zh/raw/refs/heads/main/dist/karpathy-output-style-zh.zip)：技能、界面元数据、许可证和中文安装说明
- [安装说明](INSTALL.zh-CN.md)：个人技能目录、显式调用和安装检查
- [离线交互示例 HTML](https://github.com/BaoBao1996121/karpathy-output-style-zh/raw/refs/heads/main/examples/top-k/top-k-maintenance.html)：保存后在本地浏览器打开
- [66 秒演示视频 MP4](https://github.com/BaoBao1996121/karpathy-output-style-zh/raw/refs/heads/main/demo/demo.mp4)：1280×720，中文字幕，无音轨
- [测试方法与结果](evaluation/README.zh-CN.md)

[![Top-K 演示封面](demo/poster.png)](demo/demo.mp4)

视频是原创几何动画，使用与交互示例相同的模拟数据；它不是网页录屏。点击封面打开视频文件。

## 怎么用

安装后，显式调用：

```text
用 $karpathy-output-style-zh 解释移动平均。
先给结论，再用同一个例子说明输入、过程和输出。
```

需要看见变化时，继续说：

```text
可视化：让我调窗口大小，看看结果怎样变化。
```

简短改写也可以：

```text
用 $karpathy-output-style-zh 把这段话改得简短准确。
保留前提、因果和不确定性。
```

“可视化”是会话约定。技能会按问题选择适合的形式；普通问答不必生成网页，安装也不保证每次自动触发。当前工具能否生成或打开文件仍取决于运行环境。

## 这个版本增加了什么

这是可在技能正文中检查的设计差异，不是已证明的效果提升：

- **中文讲解规则**：先给结论，使用具体词语，统一术语，保留必要条件和例外。
- **一组例子贯穿过程**：让输入、状态变化和输出能对应起来，减少中途换场景。
- **按问题选择媒介**：图解适合结构，交互适合参数变化，动画适合时间过程；不强制每次制作长教程。
- **明确权限边界**：用户说“可视化”不等于同意付费、安装软件、上传资料或公开发布。
- **交付时说明检查范围**：区分静态检查、模拟 DOM 测试、真实浏览器测试和学习效果验证。

中文仅借鉴 ASD-STE100 的清晰表达思路，不声称符合官方中文标准，也不计算所谓“80% 合规率”。

## 示例：为什么 K 从 3 加到 6，仍会漏证据？

固定同一个查询和排名：A 型号的周期证据排第 1，B 型号的周期证据排第 7。取前 3 条或前 6 条都会漏掉 B；取前 7 条，在这个例子中才覆盖两个型号。

[交互示例源码](examples/top-k/top-k-maintenance.html)包含分步播放、暂停、前后切换、重置、进度条和键盘导航。所有名称、分数及维护周期都是教学模拟，不是设备维护建议；也没有模拟近似检索、过滤、分块或上下文截断。

## 验证到哪一步

2026-10-06 的小规模检查：

- 三个固定请求分别覆盖三句话解释、离线交互示例和纠正错误保证。两组文字输出都准确，没有证明中文版本在效果上胜出。
- 本版本交互示例通过 **54 项离线断言**；上游技能试用产物的对应逻辑检查也通过。两者都使用最小 DOM 替身。
- 视频参数、完整解码和抽样画面检查通过；66 秒、24 fps、H.264、无音轨。
- 最终命名的技能已被发现并显式加载；这不等于自动选择可靠性已验证。
- **真实浏览器交互与视觉 QA 尚未完成**：测试环境的浏览器启动和本地文件访问受限。没有将模拟测试或视频当成浏览器验证。

这是一轮定性试用，不是盲测或控制变量实验。两份 HTML 的模拟数据也不完全相同。完整原始回答、测试脚本、来源哈希和限制见[评估记录](evaluation/README.zh-CN.md)。

## 本地复查

需要 Node.js 才能运行以下离线逻辑测试；HTML 本身不需要 Node.js。

```sh
node examples/top-k/check-example.cjs
node evaluation/upstream/check_logic.cjs
```

视频复查与重制需要 Python 3、Pillow、FFmpeg 和中文字体，详见[视频说明](demo/README.zh-CN.md)。技能本身没有可执行安装脚本、网络依赖或 API 密钥。

## 来源与许可

- 主要上游：[Ashrya Agrawal / Karpathy Output Style](https://github.com/ashryaagr/karpathy-output-style)，MIT；保留[上游完整许可](skills/karpathy-output-style-zh/LICENSE.upstream)。
- 相关中文工作：[mzopedia/simplified-technical-chinese](https://github.com/mzopedia/simplified-technical-chinese)，仅作相关工作引用，未复制其文字、词表或检查器。
- 检索机制参考：[Elastic 的 kNN 文档](https://www.elastic.co/docs/solutions/search/vector/knn)。

本仓库采用 [MIT License](LICENSE)。不包含上游第三方参考图片；不声称拥有 Karpathy 的姓名、肖像或商标权利。
