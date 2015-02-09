# from distutils.core import setup
from setuptools import find_packages, setup

setup(
    # Metadata
    name="wcal",
    version="0.1",
    description="workout calendar",
    url="",
    author="Erik Gafni",
    author_email="egafni@gmail.com",
    maintainer="Erik Gafni",
    maintainer_email="egafni@gmail.com",
    license="GPLv2",
    install_requires=["flask", "flask-bootstrap", "flask-failsafe", "sqlalchemy", "flask-sqlalchemy", "wtforms",
                      "python-dateutil", "flask-admin", "python-dateutil"],
    scripts=["bin/wcal"],
    # Packaging Instructions
    packages=find_packages(),
    include_package_data=True
)


