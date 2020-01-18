"""Find coupled files based on git history."""
import json
from collections import namedtuple, defaultdict
from datetime import datetime
from itertools import combinations
from typing import Dict

from gittoolbox.git.git_repo import GitRepo

Commit = namedtuple("Commit", ["id", "author", "date", "summary"])


class FileCount(object):
    def __init__(self, count: int = 0, files: Dict = None):
        self.count = count
        if not files:
            files = defaultdict(int)
        self.files = files

    def to_dict(self):
        return {"count": self.count, "files": self.files}


def add_files_to_map(seen_files: Dict[str, FileCount], commit_files):
    for f in commit_files:
        seen_files[f].count += 1
    for a, b in combinations(commit_files, 2):
        seen_files[a].files[b] += 1
        seen_files[b].files[a] += 1


def find_couplings(repo: GitRepo, since: datetime):
    logs = repo.file_log(since)
    seen_files = defaultdict(FileCount)
    commit = None
    commit_files = set()
    for line in logs.split("\n"):
        if not line:
            commit = None
            add_files_to_map(seen_files, commit_files)
            commit_files = set()
            continue

        if not commit:
            data = [item.strip() for item in line.strip('"').split("|")]
            commit = Commit(data[0], data[1], data[2], data[3])
            continue

        filename = line.split()[2].strip()
        if filename.startswith("src/mongo"):
            commit_files.add(filename)

    return seen_files
