import pytest
from realm.cli.application import Application
from realm.entities.config import Config
from realm.entities.context import RealmContext

from tests.common import get_tests_root_dir

REPO_DIR = get_tests_root_dir().joinpath("fixtures/test_workspace")


@pytest.fixture(scope="module")
def config():
    return Config.from_file(realm_json_file=str(REPO_DIR.joinpath("realm.json")))


@pytest.fixture(scope="module")
def projects(config):
    return Application.get_projects(config)


@pytest.fixture
def realm_context(config, projects):
    return RealmContext(config=config, projects=list(projects))
