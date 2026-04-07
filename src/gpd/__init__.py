"""GPD -- Get Physics Done: unified physics research orchestration."""

from importlib import import_module

from gpd._python_compat import require_supported_python

require_supported_python()

__version__ = import_module("gpd.version").__version__

__all__ = ["__version__"]
