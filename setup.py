from setuptools import setup, find_packages
import os

version = "1.1"

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md"), encoding="utf-8").read()

setup(
    name="lfs-samples",
    version=version,
    description="Sample management for LFS",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 5.2",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    keywords="django e-commerce online-shop",
    author="Kai Diefenbach",
    author_email="kai.diefenbach@iqpp.de",
    url="https://github.com/diefenbach/lfs-samples",
    license="BSD-3-Clause",
    packages=find_packages(exclude=["ez_setup"]),
    include_package_data=True,
    zip_safe=False,
    dependency_links=[],
    python_requires=">=3.12",
    install_requires=[
        "django-lfs>=1.0,<2",
    ],
)
