# bake_a_pypi
Easy setup for a PyPi package


# Usage:
- Change "packageName" in ``setup.py`` and ``_info.py`` to whatever your package name is.
- Change the "packageName" folder to this same name.
- Do code.
- In ``Settings -> Secrets``, add ``PYPI_USERNAME`` and ``PYPI_PASSWORD``
- When making a release, update ``__version__`` in ``_info.py`` This must be entirely numeric for PyPi (i.e. 1.0.0, not 1.0.b). Set the TAG to this same number EXACTLY.
- Package will be automatically generated and uploaded to PyPi whenever a release is created.
