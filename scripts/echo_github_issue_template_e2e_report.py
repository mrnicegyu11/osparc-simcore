import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

CURRENT_FILE = Path(sys.argv[0] if __name__ == "__main__" else __name__)
CURRENT_DIR = CURRENT_FILE.resolve().parent
REPO_DIR = CURRENT_DIR.parent

ITEM_BULLET = "  - [ ]"


DEPLOY_LOCATIONS = ("master", "dalco", "aws")
DEPLOY_FLAVOURS = ("staging", "production")


@dataclass
class Config:
    repo_name: str
    test_dir_name: str


def main(config: Config):
    """
    Prints e2e_report.md using a template and the scripts available under tests/e2e

    Usage:

        cd osparc-simcore/scripts
        python echo_github_issue_template_e2e_report.py >> ../.github/ISSUE_TEMPLATE/e2e_report.md

    """
    TARGET_DIR = REPO_DIR / "tests" / "e2e" / config.test_dir_name
    CI_BASEURL_FORMAT = f"https://git.speag.com/oSparc/{config.repo_name}/-/pipelines?page=1&scope=all&ref={{branch_name}}"

    # list test scripts
    scripts = [
        script_path
        for script_path in TARGET_DIR.glob("*.js")
        if not script_path.name.endswith("Base.js")
    ]

    # create ref links
    refs = {
        f"[{p.stem}]": f"https://github.com/ITISFoundation/osparc-simcore/blob/master/{p.relative_to(REPO_DIR)}"
        for p in scripts
    }
    try:
        refs.update({"[parallel_w_jupyters]": refs["[jupyters]"]})
    except KeyError:
        pass

    # Template for e2e_report.md --------
    print(
        f"<!-- Autogenerated by {CURRENT_FILE} at {datetime.now().isoformat()} --> ",
        end="\n" * 2,
    )

    print("## what fails?")
    for r in sorted(refs.keys()):
        print(ITEM_BULLET, r)

    print()
    print("## where")
    for p in DEPLOY_LOCATIONS:
        if p != "master":
            for q in DEPLOY_FLAVOURS:
                print(ITEM_BULLET, f"[e2e/{p}/{q}]")
        else:
            print(ITEM_BULLET, f"[e2e/{p}]")

    print("## known temporary fix")

    print(end="\n" * 2)

    print("<!--Keep references at the bottom -->")
    #
    for r, v in refs.items():
        print(f"{r}:{v}")

    print(end="\n" * 2)

    # deploys
    for p in DEPLOY_LOCATIONS:
        if p != "master":
            for q in DEPLOY_FLAVOURS:
                brh = q
                if p == "aws":
                    brh += "_aws"
                print(f"[e2e/{p}/{q}]:{CI_BASEURL_FORMAT.format(branch_name=brh)}")
        else:
            print(f"[e2e/{p}]:{CI_BASEURL_FORMAT.format(branch_name=p)}")


if __name__ == "__main__":
    tutorials = Config(repo_name="e2e-testing", test_dir_name="tutorials")
    main(tutorials)

    print("-" * 10)

    portal = Config(repo_name="e2e-portal-testing", test_dir_name="portal")
    main(portal)
