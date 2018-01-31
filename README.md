# git-batch

> git-batch是一个基于`GitPython`的Git仓库批处理命令行脚本，可以批量更新代码、统一切换分支、从dev分支上拉取release, feature分支等。

## 安装
1. 建议安装Python3，避免中文编码等问题。

由于Mac系统默认安装的是Python 2.7，建议下载最新的Python 3.6版本。

2. clone本项目

```
$git clone https://github.com/HanderWei/git-batch.git
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

2. 更新代码

```
$python git-batch.py pull
```

3. 切换分支

```
$python git-batch.py checkout master
$python git-batch.py co master          #与上一条作用相同
```

4. 从dev分支上创建新分支

```
$python git-batch.py new feature/v2.0
```

## 简化操作

可以通过将python脚本写入`~/.bash_profile`文件，简化输入操作

```
alias python='python3' # 默认使用Python3

alias gits='python /项目目录/git-batch/git-batch.py'
```

后续只要使用`gits`命令就可以执行该脚本。

```
$gits pull
$gits checkout master -p ~/Users/netease/study-project
$gits new release/v2.0 -p ~/Users/netease/study-project
```