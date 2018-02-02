# git-batch

> git-batch是一个基于`GitPython`的Git仓库批处理命令行脚本，可以批量克隆项目、更新代码、切换分支、从dev分支上创建新分支，删除本地及远端的分支等。

## 安装
1. 建议安装Python3，避免中文编码等问题。

由于Mac系统默认安装的是Python 2.7，建议下载最新的Python 3.6版本。

2. clone本项目

```
$git clone ssh://git@g.hz.netease.com:22222/hzchenwei6/git-batch.git
```

3. 下载GitPython

```
$pip3 install gitpython
```

## 使用
1. 查看帮助文档

```
$python git-batch.py -h
```

2. 克隆工程

```
$python git-batch.py -f clone.txt
```

其中clone.txt 形如

```
ssh://www.github.com/user/pro1.git
ssh://www.github.com/user/pro2.git
ssh://www.github.com/user/pro3.git
```

3. 更新代码

```
$python git-batch.py pull
```

4. 切换分支

```
$python git-batch.py checkout master
$python git-batch.py co master          #与上一条作用相同
```

5. 从dev分支上创建新分支

```
$python git-batch.py new feature/v2.0
```

创建新分支，也可以提供filter文件，只对filter文件中的项目创建新的分支

```
$python git-batch.py new feature/v2.0 -f filter.txt
```

filter.txt

```
pro1
pro2
```

6. 删除分支

* 删除本地分支

```
$python git-batch.py delete feature/v1.0 -r False
$python git-batch.py delete feature/v1.0            # 与航一条作用相同
```

> 注意：删除本地分支时，可以不传入 -r 参数

* 删除远端分支

```
$python git-batch.py delete feature/v1.0 -r True
```

## 简化操作

可以通过将python脚本写入`~/.bash_profile`文件，简化输入操作

```
alias python='python3' # 默认使用Python3

alias gits='python /项目目录/git-batch/git-batch.py'
```

后续只要使用`gits`命令就可以执行该脚本。

```
$gits clone -f clone.txt -p ~/Users/netease/study-project # 克隆项目
$gits pull -p ~/Users/netease/study-project # 更新代码
$gits checkout master -p ~/Users/netease/study-project # 切换分支
$gits new release/v2.0 -p ~/Users/netease/study-project # 从dev上拉取新分支
$gits delete feature/v1.0 -p ~/Users/netease/study-project # 删除本地分支
$gits delete feature/v1.0 -r true -p ~/Users/netease/study-project # 删除远端分支
```

为了避免每次输入`-p 项目根目录`，可以先切换到项目根目录

```
$cd ~/Users/netease/study-project 
$gits clone -f clone.txt # 克隆项目
$gits pull  # 更新代码
$gits checkout master  # 切换分支
$gits new release/v2.0  # 从dev上创建新分支
$gits new release/v2.0 -f filter.txt # 创建新分支时指定项目列表
$gits delete feature/v1.0  # 删除本地分支
$gits delete feature/v1.0 -r true  # 删除远端分支
```