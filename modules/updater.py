import git
import typing
import os
import atexit
import sys
import subprocess
from git import Repo


def get_current_commit() -> typing.Union[bool, str]:
    """Get current commit"""

    try:
        repo = git.Repo()
        return repo.heads[0].commit.hexsha
    except Exception:
        return False


def check_update() -> bool:
    """Check update for botnet"""

    try:
        repo = git.Repo(os.getcwd())
    except git.exc.GitError:
        repo = Repo.init(os.getcwd())
        origin = repo.create_remote("origin", "https://github.com/json1c/telegram-raid-botnet")
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    
    upcoming_commit = git.Remote(repo, "origin").fetch()[0].commit.hexsha
    current_commit = get_current_commit()

    if current_commit != upcoming_commit:
        return True

    return False


def update_requirements(console):
    with console.status("Installing new requirements..."):
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                os.path.join(
                    os.getcwd(),
                    "requirements.txt",
                ),
                "--user",
            ],
            check=True,
        )

    console.print("[bold green]New requirements installed successfully.")


def on_exit():
    os.execl(
        sys.executable,
        sys.executable,
        *sys.argv
    )


def restart_botnet():
    atexit.register(on_exit)
    exit(0)


def update(console):
    try:
        with console.status("Updating..."):
            repo = Repo(os.getcwd())
            origin = repo.remote("origin")
            r = origin.pull()
        
        console.print("[bold green]Updated successfully!")

        new_commit = repo.head.commit

        for info in r:
            if info.old_commit:
                for d in new_commit.diff(info.old_commit):
                    if d.b_path == "requirements.txt":
                        update_requirements(console)
        
        restart_botnet()
    except git.exc.InvalidGitRepositoryError:
        repo = Repo.init(os.getcwd())
        origin = repo.create_remote("origin", "https://github.com/json1c/telegram-raid-botnet")
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
