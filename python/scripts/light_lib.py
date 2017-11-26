import os

env_or_else = lambda env, or_else: os.environ[env] if env in os.environ else or_else
