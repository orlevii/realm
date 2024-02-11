from typing import List

from .config import Config
from .graph import Graph
from .project import Project


class RealmContext:
    def __init__(self, config: Config, projects: List[Project]):
        self.config = config
        self.projects = projects
        self.all_projects = projects
        self.dependency_graph = Graph(projects)
