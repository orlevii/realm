import json
import pathlib


class Config:
    def __init__(self,
                 root_dir='.',
                 projects=[],
                 **kwargs):
        self.root_dir = root_dir
        self.projects = projects

    @classmethod
    def from_file(cls, realm_json_file):
        p = pathlib.Path(realm_json_file)
        with open(realm_json_file, 'r') as f:
            cfg_json = json.load(f)

            return cls(root_dir=str(p.parent),
                       **cfg_json)
