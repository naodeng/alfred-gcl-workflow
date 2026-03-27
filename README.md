# GCL - Alfred Workflow

**Generation for different character lengths**：支持循环数字输出和 3 种随机输出模式。

## 功能

- 关键字：`gcl`（可带空格后跟数字）
- 输入 `gcl 10` → 循环输出 `1234567890`（按长度截取）
- 输入 `gcl a 10` → 随机字母（大小写）
- 输入 `gcl an 10` → 随机数字 + 大小写字母
- 输入 `gcl ans 10` → 随机数字 + 大小写字母 + 符号
- 长度支持 1–20000，超过会提示上限

## 安装

1. **双击**本目录内的 **GCL-Generate-Number.alfredworkflow** 文件（Alfred 可识别的安装包），按提示导入；或在 Alfred 中：**Workflows** → **+** → **Import**，选择该 `.alfredworkflow` 文件。
2. 从 GitHub 下载时，可直接下载 [GCL-Generate-Number.alfredworkflow](https://github.com/naodeng/alfred-gcl-workflow/raw/main/GCL-Generate-Number.alfredworkflow) 后双击安装。

## 使用

1. 打开 Alfred（⌘ + Space 或你设置的快捷键）；
2. 选择模式并输入长度（长度范围 1–20000）：
   - `gcl 10`
   - `gcl a 10`
   - `gcl an 10`
   - `gcl ans 10`
3. 会显示对应结果，回车可复制到剪贴板；⌘L 可大号显示。

## 依赖

- macOS
- Alfred（建议 Alfred 4/5，需 Powerpack）
- 系统自带 Python 3（脚本使用 `#!/usr/bin/env python3`）

## 文件说明

| 文件 | 说明 |
|------|------|
| `GCL-Generate-Number.alfredworkflow` | 安装包（zip），双击即可导入 Alfred |
| `generate_content.py` | Script Filter 脚本：解析模式和长度，生成循环或随机结果，输出 JSON |
| `info.plist` | Workflow 配置：关键字 gcl、Script Filter、复制到剪贴板 |

## 说明

- 当前位数上限为 **20000**；极大位数时生成可能稍慢。

---

**作者**：[naodeng](https://github.com/naodeng)
