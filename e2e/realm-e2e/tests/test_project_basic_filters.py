import pytest
from tests.common import PACKAGES_REPO, create_run_in_fixture_fn

run = create_run_in_fixture_fn(PACKAGES_REPO)


def test_ls():
    output = run("realm ls").strip().split()
    assert set(output) == {"pkg@0.1.0", "pkg_with_groups@0.1.0"}


@pytest.mark.parametrize(
    "filters",
    [
        {"scope": ["p*"], "expected": ["pkg@0.1.0", "pkg_with_groups@0.1.0"]},
        {"scope": ["p*"], "ignore": ["*with*"], "expected": ["pkg@0.1.0"]},
        {"scope": ["w*"], "expected": []},
    ],
)
def test_ls_with_filters(filters: dict):
    cmd = "realm ls"
    for s in filters.get("scope", []):
        cmd += f" --scope {s}"
    for s in filters.get("ignore", []):
        cmd += f" --ignore {s}"

    output = run(cmd).strip().split()
    assert set(output) == set(filters["expected"]), cmd


def test_ls_with_match():
    cmd = "realm ls --match labels.type=package"
    output = run(cmd).strip()
    assert output == "pkg@0.1.0", cmd
