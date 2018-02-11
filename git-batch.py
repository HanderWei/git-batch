from git import Repo, InvalidGitRepositoryError, GitCommandError, Git
from os import listdir
from os.path import join
import argparse

# 暂存列表
stash_repos = []


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
    stashed = False
    if repo.is_dirty():
        print(repo.git_dir + " 包含未提交文件，已暂存。")
        repo.git.stash('save')
        stash_repos.append(repo)
        stashed = True
    repo.remote().pull()
    print(repo.working_dir.split('/')[-1] + ' pull finished.')
    if stashed:
        try:
            repo.git.stash('pop')
            print(repo.git_dir + " stash pop finished.")
        except GitCommandError:
            print(repo.git_dir + " merge conflict, please merge by yourself.")


def get_branch_name(branch):
    return branch.name


def get_remote_branch_name(branch_name):
    return 'origin/' + branch_name


def checkout_repos(repos, branch):
    """切换分支"""
    for repo in repos:
        checkout(repo, branch)


def get_all_local_branches(repo):
    """获取本地分支"""
    return list(map(get_branch_name, repo.branches))


def get_all_remote_branches(repo):
    """获取远端分支"""
    return list(map(get_branch_name, repo.remotes.origin.refs))


def checkout(repo, branch, log=True):
    # 远端分支名称
    remote_branch = get_remote_branch_name(branch)
    try:
        if branch in get_all_local_branches(repo):
            # 如果存在本地分支，则直接checkout到本地分支
            repo.git.checkout(branch)
            if log:
                print(get_repo_dir_name(repo) + ' checkout finished.')
        elif remote_branch in get_all_remote_branches(repo):
            # 如果存在远端分支，则追踪至远端分支
            repo.git.checkout(remote_branch, b=branch)
            if log:
                print(get_repo_dir_name(repo) + ' checkout finished.')
        else:
            if log:
                print(get_repo_dir_name(repo) + ' does not have this branch.')
    except GitCommandError:
        print("TODO")


def create_branches(repos, branch, filter_file):
    """拉取新分支"""
    if filter_file:
        # 传入过滤文件，则仅从过滤文件中拉取新分支
        handle_dirs = []
        with open(filter_file, 'r') as f:
            for handle_dir in f:
                handle_dirs.append(handle_dir.replace('\n', ''))
        for repo in repos:
            if get_repo_dir_name(repo) not in handle_dirs:
                return
            create_branch(repo, branch)
    else:
        for repo in repos:
            create_branch(repo, branch)


def create_branch(repo, branch):
    # 切换至dev分支
    checkout(repo, 'dev', log=False)
    # 创建本地分支
    repo.create_head(branch)
    # 切换至新分支
    checkout(repo, branch, log=False)
    # push到远端
    repo.git.push('origin', branch)
    print(get_repo_dir_name(repo) + ' create new branch and push to origin.')


def get_repo_dir_name(repo):
    """返回仓库文件夹名称"""
    return repo.working_dir.split('/')[-1]


def delete_branches(repos, branch, remote=False):
    """删除分支"""
    for repo in repos:
        delete_branch(repo, branch, remote)


def delete_branch(repo, branch, remote=False):
    """删除分支"""
    if remote:
        delete_remote_branch(branch, repo)
    else:
        delete_local_branch(branch, repo)


def delete_local_branch(branch, repo):
    """删除本地分支"""
    if repo.active_branch.name == branch:
        print(get_repo_dir_name(repo))
        print('Cannot delete the branch which you are currently on.')
        print()
    elif branch not in get_all_local_branches(repo):
        print(get_repo_dir_name(repo) + ' branch not found.')
        print()
    else:
        repo.delete_head(branch)
        print(get_repo_dir_name(repo) + ' delete ' + branch + ' finished.')
        print()


def delete_remote_branch(branch, repo):
    """删除远端分支"""
    remote_branch = get_remote_branch_name(branch)
    if remote_branch not in get_all_remote_branches(repo):
        print(get_repo_dir_name(repo) + ' branch not found.')
        print()
    else:
        remote = repo.remote(name='origin')
        remote.push(refspec=(':' + branch))
        print(get_repo_dir_name(repo) + ' delete ' + branch + ' finished.')
        print()


def clone_repos(path, clone_file):
    with open(clone_file, 'r') as f:
        for repo_url in f:
            clone_repo(path, repo_url.replace('\n', ''))


def clone_repo(path, repo_url):
    """克隆仓库"""
    try:
        Git(path).clone(repo_url)
        print('Clone ' + repo_url + ' finished.')
    except GitCommandError:
        print('Clone ' + repo_url + ' failed.')


def handle_args():
    """解析脚本参数"""
    method = args.method
    if method == 'clone':
        if args.filter:
            clone_repos(args.path, args.filter)
            return
        else:
            print("克隆工程需要filter文件，指定克隆项目列表")
            return

    repos = get_all_git_repos(args.path)  # 获取全部仓库
    if method == 'pull':
        """拉取最新代码"""
        pull_repos(repos)
    elif (method == 'checkout' or method == 'co') and args.branch != '':
        """切换到指定分支"""
        checkout_repos(repos, args.branch)
    elif method == 'new' and args.branch != '':
        """创建新分支"""
        create_branches(repos, args.branch, args.filter)
    elif method == 'delete' and args.branch != '':
        """删除分支"""
        delete_branches(repos, args.branch, args.remote)
    else:
        print("Not support method")


parser = argparse.ArgumentParser(description='Git 批处理工具')
parser.add_argument('-p', '--path', type=str, default='.', help='批处理目录，默认为当前目录', required=False)
parser.add_argument('-r', '--remote', type=bool, default=False, help='是否操作远端分支，默认为False', required=False)
parser.add_argument('-f', '--filter', type=str, help='克隆项目目标文件', required=False)
parser.add_argument('method', action='store', type=str, choices=['clone', 'pull', 'checkout', 'co', 'new', 'delete'],
                    help='批量执行任务, clone, pull, checkout[co], new, delete')
parser.add_argument('branch', nargs='?', action='store', type=str, default='', help='指定target分支')

args = parser.parse_args()

handle_args()
