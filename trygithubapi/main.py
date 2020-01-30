import os
from github import Github

def get_version_and_tag_name():
    "バージョン名とタグ名を作る"
    major = 1
    minor = 0
    patch = 0
    with open("app/build.gradle") as f:
        for line in f.readlines():
            if(line.startswith("def major = ")):
                major = int(line.split()[-1])
            if(line.startswith("def minor = ")):
                minor = int(line.split()[-1])
            if(line.startswith("def patch = ")):
                patch = int(line.split()[-1])
    version_name = "%d.%d.%d" % (major,minor,patch)
    tag_name = "release_%d_%d_%d" % (major,minor,patch)
    return version_name, tag_name

def main():
    # アクセストークンを持ってGithubオブジェクトを作成
    access_token = os.environ['BITRISEIO_GITHUB_API_ACCESS_TOKEN']
    g = Github(access_token)
    # リポジトリを取得
    repo = g.get_user().get_repo("quickecho")
    # 閉じられたPR一覧を取得
    prs = repo.get_pulls(state='closed')
    # 新しい順に取得する
    # ループの最大回数も指定できる
    for pr in prs[:5]:
        print("#%d %s %s" %
            (pr.number, pr.title, pr.merge_commit_sha))
    # masterブランチのコミット一覧を取得
    commits = repo.get_commits()
    for commit in commits[:10]:
        gc = commit.commit
        print("%s" % gc.sha)
    # リリース一覧を取得
    rs = repo.get_releases()
    for r in rs:
        print("%s %s" % (r.title, r.tag_name))
    # タグ一覧を習得
    tags = repo.get_tags()
    for tag in tags:
        print("%s %s" % (tag.name, tag.commit.commit.sha))
    # バージョンを取得
    print(get_version_and_tag_name())
