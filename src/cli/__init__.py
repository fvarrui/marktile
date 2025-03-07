import importlib.metadata

__project_name__ = 'marktile'
__project_description__ = importlib.metadata.version(__project_name__)
__project_version__ = importlib.metadata.metadata(__project_name__).get('Summary')