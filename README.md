# Bake a PyPi
Easy setup for an automated PyPi package

# Usage:
- [ ] Change "packageName" in ``setup.py`` and ``_info.py`` to whatever your package name is.
- [ ] Change the "packageName" folder to this same name.
- [ ] In ``Settings -> Secrets``, add ``PYPI_USERNAME`` and ``PYPI_PASSWORD``.
- [ ] Do code.
- [ ] When making a release, set the TAG to the new version number. This must be entirely numeric for PyPi (i.e. 1.0.0, not 1.0.b). This will be used during the package generation process.
- [ ] Package will be automatically generated and uploaded to PyPi whenever a release is created.
