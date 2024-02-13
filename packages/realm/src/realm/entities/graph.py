from itertools import combinations
from typing import Dict, List, Set, Tuple

from .project import Project

ProjectDependencies = Dict[Project, Set[Project]]


class Graph:
    def __init__(self, projects: List[Project]):
        self.projects = projects
        self.project_deps, self.projects_affected = self._build_project_deps(projects)
        self.topology = self._build_topology(self.project_deps)

    @classmethod
    def _build_project_deps(
        cls, projects: List[Project]
    ) -> Tuple[ProjectDependencies, ProjectDependencies]:
        project_deps = {p: set() for p in projects}
        projects_affected = {p: set() for p in projects}

        proj_a: Project
        proj_b: Project
        for proj_a, proj_b in combinations(projects, 2):
            if proj_a.is_dependent_on(proj_b):
                project_deps[proj_a].add(proj_b)
                projects_affected[proj_b].add(proj_a)
            elif proj_b.is_dependent_on(proj_a):
                project_deps[proj_b].add(proj_a)
                projects_affected[proj_a].add(proj_b)

        return project_deps, projects_affected

    @classmethod
    def _build_topology(cls, project_deps: ProjectDependencies) -> List[Set[Project]]:
        project_deps = dict(project_deps)
        res = [set()]
        seen_deps = set()
        while any(project_deps):
            seen_deps = seen_deps.union(res[-1])
            new = set()
            for proj, deps in list(project_deps.items()):
                if not any(deps - seen_deps):
                    new.add(proj)
                    project_deps.pop(proj)
            res.append(new)
        return res[1:]
