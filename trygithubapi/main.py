import os
from github import Github


def main():
    access_token = os.environ['BITRISEIO_GITHUB_API_ACCESS_TOKEN']
    g = Github(access_token)
    repo = g.get_user().get_repo("quickecho")
    print(repo.name)
    print("Hello World")
