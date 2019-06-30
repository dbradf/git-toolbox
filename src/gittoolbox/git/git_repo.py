
from pygit2 import Repository, GIT_SORT_TOPOLOGICAL


class GitRepo(object):
    """A git repository."""
    def __init__(self, repo: Repository):
        """
        Create a new GitRepo.
        :param repo: pygit2 Repository representing repo.
        """
        self._repo = repo

    @classmethod
    def local_repo(cls, path):
        """
        Create a GitRepo for a local repository.
        :param path: Path to local repository.
        :return: GitRepo for local repository.
        """
        return cls(Repository(path))

    def head(self):
        return self._repo.head.target

    def walk_commits(self, start_commit):
        """
        Walk the commits in the repository.

        :param start_commit: Commit to start walking.
        :return: Generator that walks commits.
        """
        for commit in self._repo.walk(start_commit, GIT_SORT_TOPOLOGICAL):
            yield GitCommit(commit)


class GitCommit(object):
    """A git commit object."""
    def __init__(self, commit):
        """
        Create an object representing a commit.

        :param commit: pygit2 commit object.
        """
        self._commit = commit

    def summary(self):
        """
        Get a summary of the commit message.
        :return: Summary of commit message.
        """
        return self._commit.message.splitlines()[0]

    @property
    def commit_time(self):
        """
        Get the time the commit was created.
        :return: commit time.
        """
        return self._commit.commit_time

    @property
    def parent(self):
        """
        Get the parent for this commit.

        Returns the first commit if this is a merge commit.
        :return: Parent of commit.
        """
        return self._commit.parents[0]

    def diff_to_parent(self):
        """
        Compare this commit to its parent.

        :return:
        """
        return GitDiff(self._commit.tree.diff_to_tree(self.parent.tree))


class GitDiff(object):
    """A Git diff object."""
    def __init__(self, diff):
        """
        Create an object representing a diff.
        :param diff: pygit2 diff object.
        """
        self._diff = diff

    def new_file_iter(self):
        """
        Iterate over file for added changes in the diff.

        :return: Iterator for added files.
        """
        for patch in self._diff:
            yield patch.delta.new_file.path
