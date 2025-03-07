import os
from toml import load
from pathlib import Path

pyproject = load(os.path.join(Path(__file__).parent.parent.parent, 'pyproject.toml'))

__project_name__ = pyproject['project']['name']
__project_description__ = pyproject['project']['description']
__project_version__ = pyproject['project']['version']