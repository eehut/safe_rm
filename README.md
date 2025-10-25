# 🧹 srm — 安全删除工具（Safe Remove）

`srm` 是一个 **Linux 命令行安全删除脚本**，它模拟 `rm` 的使用习惯（支持 `-r`、`-f` 参数），但不会真正删除文件，而是将文件或目录移动到用户主目录下的回收站 `~/.trash`，从而防止误删。

## ✨ 特性

* 🧩 兼容 `rm` 的常用参数（`-r`, `-f`, `--help`, `--version`）
* 🗑️ 删除操作将文件移动到 `~/.trash`，可手动恢复
* 🔗 支持文件、目录、符号链接的安全删除
* 🛡️ `-f` 参数可忽略不存在的文件或只读文件的错误提示
* 📂 `-r` 参数支持递归删除目录

## ⚙️ 使用方法

```bash
srm [OPTION] ... [FILE] ...
```

**示例：**

```bash
srm test.txt              # 将 test.txt 移动到 ~/.trash
srm -r folder/            # 递归删除目录
srm -rf /tmp/data         # 强制删除目录及内容，不提示错误
```

## 🧰 安装

**Install to /usr/bin**

```sh
sudo cp rm.py /usr/bin
cd /usr/bin && ln -s rm.py srm
```

## 🪶 示例输出

```
rm: move 'test.txt' -> '/home/user/.trash/20231025-test.txt'
```






