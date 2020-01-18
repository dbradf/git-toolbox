"""CLI interface for creating file couplings."""
import logging
import json

import click
import structlog

from gittoolbox.git.git_repo import GitRepo
from gittoolbox.coupling.coupled_files import find_couplings


@click.command("git-coupling")
@click.option("--repo-location")
@click.option("--verbose", is_flag=True)
def coupling(repo_location, verbose):
    structlog.configure(logger_factory=structlog.stdlib.LoggerFactory())
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level)

    repo = GitRepo.local_repo(repo_location)

    coupling = find_couplings(repo, None)
    # for k, v in coupling.items():
    #     count = v.count
    #     for k1, v1 in v.files.items():
    #         percent = v1 / count
    #         if percent > 0.75 and count > 5:
    #             print(f"High Coupling: {k} - {k1}: {percent} {count}")
    print(json.dumps({k: v.to_dict() for k, v in coupling.items()}, indent=4))
