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
        numbers = self.get_marged_pr_numbers(commits)
        prs = self.get_prs_in_numbers(numbers)
        # テキストを作成する
        text = ""
        for pr in prs:
            text += "- %s #%d\n" % (pr.title, pr.number)
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

    def get_marged_pr_numbers(self, commits):
        "コミット一覧からマージされたプルリク番号を得る"
        numbers = []
        for commit in commits:
            message = commit.message
            if(message.startswith("Merge pull request #")):
                items = message.split()
                number = int(items[3][1:])
                numbers.append(number)
        return numbers

    def get_prs_in_numbers(self, numbers):
        "プルリク番号からプルリク一覧にする"
        prs = []
        for number in numbers:
            pr = self.repo.get_pull(number)
            prs.append(pr)
        return prs
