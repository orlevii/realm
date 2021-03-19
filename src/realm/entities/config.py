class Config:
    def __init__(self,
                 root_dir='.',
                 projects=[],
                 test_env_vars={},
                 **kwargs):
        self.root_dir = root_dir
        self.projects = projects
        self.test_env_vars = test_env_vars
