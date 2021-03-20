from typing import List

from .config import Config
from .project import Project


class RealmContext:
    def __init__(self,
                 config: Config,
                 projects: List[Project]):
        self.config = config
        self.projects = projects
        self.all_projects = projects
