import os
from github import Github
from trygithubapi.repository import Repository

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
    gr = g.get_user().get_repo("quickecho")
    # Organizationを使っている場合
    # gr = g.get_organization("organization_name").get_repo("repository_name")
    # インスタンスにする
    r = Repository(gr)
    # masterブランチにマージ済みプルリク一覧テキストを作成する
    text = r.make_marged_prs()
    print(text)
