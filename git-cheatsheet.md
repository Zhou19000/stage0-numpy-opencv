# Git 命令速查表（阶段 0 专用）

> 用途：忘了命令就来翻这里。不用背，用一周自然记住。

## 一、每天必用的 6 条（只要记住这些）

| 命令 | 作用 | 什么时候用 |
|---|---|---|
| `cd "路径"` | 进入某个文件夹 | 换位置 |
| `dir` | 看当前文件夹里有什么 | 确认自己站对地方没 |
| `git status` | 看现在有哪些文件被改过 | **忘了干啥就先敲它** |
| `git add .` | 把改动放进暂存区（注意中间有空格） | 提交前 |
| `git commit -m "说明"` | 存档，引号里写这次改了什么 | 每天收工前 |
| `git push` | 上传到 GitHub | 每天收工前 |

## 二、标准每日流程

```cmd
git status                          ← 看看改了哪些文件
git add .                           ← 全部放进暂存区
git commit -m "Day2: NumPy 数组基础"  ← 存档，写清今天干了啥
git push                            ← 上传（记得开着 Clash Verge）
```

## 三、常见报错对照表（已经踩过的坑）

| 报错 | 原因 | 怎么修 |
|---|---|---|
| `bash: xxx: command not found` | 命令拼错了，或漏了空格 | 检查拼写；`cd 路径` 中间要有空格 |
| `cd: No such file or directory` | 路径不存在或写错了 | 先 `dir` 看看真实名字；路径含空格要加英文双引号 |
| `cd: too many arguments` | 路径有空格但没加引号 | 写成 `cd "D:\sycu\AI model"` |
| `Nothing specified, nothing added` | `git add` 后面漏了 `.` | 改成 `git add .` |
| `Author identity unknown` | 没配置用户名邮箱 | `git config --global user.name "Zhou19000"` 等两条 |
| `Recv failure: Connection was reset` | 网络不通（代理没开或节点挂了） | 打开 Clash Verge，确认端口还是 7897 |
| `Updates were rejected` | 远程有本地没有的提交 | 先 `git pull --rebase origin main` 再 push |
| `nothing to commit, working tree clean` | 没有新改动，是**正常提示**不是错误 | 无需处理 |

## 四、网络与代理（重要）

- **只有跟 GitHub 打交道才需要代理**：写代码、跑代码、pip 装包都不需要。
- 代理软件：**Clash Verge，端口 7897**，git 已配置好走代理，**只要软件开着就行**。
- 如果换了代理软件 / 端口变了，重新配一句：

```cmd
git config --global http.https://github.com.proxy http://127.0.0.1:7897
```

- 要取消代理配置（比如在公司网络下）：

```cmd
git config --global --unset http.https://github.com.proxy
```

## 五、文件与目录命令

| 命令 | 含义 |
|---|---|
| `cd "路径"` | 进入文件夹 |
| `cd ..` | 返回上一级 |
| `cd ~` | 回到用户主目录 |
| `dir`（CMD） / `ls`（Git Bash） | 列出当前文件夹内容 |
| `mkdir 名字` | 新建文件夹 |
| `rmdir 名字` | 删除**空**文件夹（比 rm 安全） |
| `Tab` 键 | 自动补全路径 / 文件名（防手滑神器） |

⚠️ **安全提醒**：`rm`（Git Bash）/ `del`（CMD）是**真删除，不进回收站**。删之前先 `dir` 确认自己在哪儿。`rmdir` 只能删空文件夹，相对安全。

## 六、两种终端的区别（踩过的坑）

| | Git Bash | CMD / PowerShell |
|---|---|---|
| 路径写法 | `/d/sycu/AI model` | `D:\sycu\AI model` |
| 看目录 | `ls` | `dir`（PowerShell 里 `ls` 也能用） |
| 复制粘贴 | 选中即复制 / Shift+Insert 粘贴 | Ctrl+C / Ctrl+V |
| 中断命令 | Ctrl+C | Ctrl+C |

**建议**：日常就用 **PyCharm 内置终端**或 PowerShell，Git Bash 留着备用（阶段 3 学 Linux 时再用）。

## 七、术语速查（一句话版）

| 名词 | 一句话解释 |
|---|---|
| 工作区 | 你正在改的文件所在的地方 |
| 暂存区 | 挑出"这次要存档"的文件 |
| 本地仓库 | 你电脑上的存档库，commit 进来的都在这里 |
| 远程仓库 | GitHub 上的那一份（备份 + 展示） |
| commit | 存档，生成一个可回退的快照 |
| push | 把本地存档上传到 GitHub |
| pull | 把 GitHub 上的更新拉到本地 |
| 分支（main） | 一条独立的开发线，个人项目先用默认的 main |
| clone | 把别人的仓库整个下载到本地 |
| README.md | 仓库的"说明书封面"，面试官第一眼看的地方 |
| .gitignore | 告诉 Git "这些文件不用上传"的清单 |

## 八、连接 GitHub 的常用地址

- 你的账号：https://github.com/Zhou19000
- 本仓库：https://github.com/Zhou19000/stage0-numpy-opencv
- 本地路径：`D:\sycu\AI model\stage0-numpy-opencv`
