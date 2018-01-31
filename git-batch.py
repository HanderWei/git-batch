from git import Repo, InvalidGitRepositoryError, GitCommandError
from os import listdir
from os.path import join
import argparse


def path_to_repo(path):
    """将路径转换成Repo对象，若非Git目录，则抛出异常"""
    try:
        return Repo(path)
    except InvalidGitRepositoryError:
        return None


def not_none(obj):
    return obj is not None


def get_all_git_repos(path):
    """获取指定路径中的全部Git目录"""
    return list(filter(not_none, map(path_to_repo, map(join, [path] * len(listdir(path)), listdir(path)))))


def pull_repos(repos):
    """拉取到最新代码"""
    for repo in repos:
        git_pull_single_repo(repo)


def git_pull_single_repo(repo):
    """拉取到最新代码"""
    if repo.is_dirty():
        print(repo.git_dir + " 包含未提交文件，已暂存。\n")
        repo.git.stash('save')
    repo.remote().pull()


def get_branch_name(branch):
    return branch.name


def get_remote_branch_name(branch_name):
    return 'origin/' + branch_name


def checkout_repos(repos, branch):
    """切换分支"""
    for repo in repos:
        checkout(repo, branch)


def checkout(repo, branch):
    # 远端分支名称
    # print(branch)
    # print(list(map(get_branch_name, repo.branches)))
    # print(list(map(get_branch_name, repo.remotes.origin.refs)))
    remote_branch = get_remote_branch_name(branch)
    try:
        if branch in list(map(get_branch_name, repo.branches)):
            # 如果存在本地分支，则直接checkout到本地分支
            print(repo.git.checkout(branch))
        elif remote_branch in list(map(get_branch_name, repo.remotes.origin.refs)):
            # 如果存在远端分支，则追踪至远端分支
            print(repo.git.checkout(remote_branch, b=branch))
        else:
            print('Your repository does not have this branch.')
    except GitCommandError:
        print("TODO")

    print()


def create_branches(repos, branch):
    """拉取新分支"""
    for repo in repos:
        create_branch(repo, branch)


def create_branch(repo, branch):
    # 切换至dev分支
    checkout(repo, 'dev')
    # 创建本地分支
    repo.create_head(branch)
    # 切换至新分支
    checkout(repo, branch)
    # push到远端
    repo.git.push('origin', branch)


def handle_args():
    """解析脚本参数"""
    repos = get_all_git_repos(args.path[0])  # 获取全部仓库
    method = args.method
    if method == 'pull':
        """拉取最新代码"""
        pull_repos(repos)
    elif (method == 'checkout' or method == 'co') and args.branch != '':
        """切换到指定分支"""
        checkout_repos(repos, args.branch)
    elif method == 'new' and args.branch != '':
        """创建新分支"""
        create_branches(repos, args.branch)
    else:
        print("no method")


parser = argparse.ArgumentParser(description='Git 批处理工具')
parser.add_argument('-p', '--path', type=str, default=['.'], help='批处理目录，默认为当前目录', required=False)
parser.add_argument('method', action='store', type=str, choices=['pull', 'checkout', 'co', 'new'],
                    help='批量执行任务，pull, checkout[co], new')
parser.add_argument('-b', '--branch', help='指定target分支[选填项]', required=False)

args = parser.parse_args()

handle_args()
