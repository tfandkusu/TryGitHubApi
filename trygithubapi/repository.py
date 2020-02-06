class Repository:
    "リポジトリからの情報出し入れ担当"

    def __init__(self, repository):
        self.repo = repository

    def make_marged_prs(self):
        "masterブランチにマージ済みのプルリク一覧テキストを作成する"
        tag = self.get_latest_release_tag()
        if(tag is None):
            raise "最新のreleaseタグがありません。"
        commits = self.get_commits(tag.commit.commit.sha)
        prs = self.get_prs_in_commits(commits)
        text = ""
        for pr in prs:
            text += "#%d %s\n" % (pr.number, pr.title)
        return text


    def get_latest_release_tag(self):
        "一番新しいリリースタグを取得する"
        tags = self.repo.get_tags()
        latest_tag = None
        for tag in tags:
            if(tag.name.startswith("release_")):
                latest_tag = tag
                break
        return latest_tag

    def get_commits(self,sha):
        "指定したハッシュまでのコミット一覧を取得する"
        # masterブランチのコミット一覧を取得
        results = []
        commits = self.repo.get_commits()
        for commit in commits:
            gc = commit.commit
            if(gc.sha == sha):
                break
            results.append(gc)
        return results

    def get_prs_in_commits(self, commits):
        """
        閉じたプルリク一覧をcommitsに含まれないものが見つかるまで新しい順番に列挙する。
        """
        # コミット一覧をハッシュ一覧にする
        shas = map(lambda c: c.sha, commits)
        results = []
        prs = self.repo.get_pulls(state='closed')
        for pr in prs:
            if(pr.merge_commit_sha in shas):
                results.append(pr)
            else:
                break
        return results
