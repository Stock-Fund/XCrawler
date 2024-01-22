import git

repo = git.Repo('.')
remote = repo.remotes['origin']
remote.fetch()
# 要比较的文件路径
file_path = "/Users/gxm/workspace/unityProject/client/uiproject/Assets/HotFix/Spine/Spine_Character_Test.atlas.txt"
repo = git.Repo("/Users/gxm/workspace/unityProject/client/uiproject")
latest_commit = remote.refs['main'].commit
diff = repo.git.diff("origin/main", "HEAD", "--", file_path)
diff1 = repo.git.diff(latest_commit, file_path)
# 获取第一个远程 tracking 分支的url
remote_url = repo.remotes[0].url
print(repo.active_branch.name)
print(remote_url)
if diff:
    print(f"输出差异:{diff}")
    with open("diff.txt", "w") as f:
        f.write(diff)
else:
    print("文件无差异")
