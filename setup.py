import sys
from distutils.core import setup
import pathlib

version = "0.1.0"
if "--version" in sys.argv:
    index = sys.argv.index("--version")
    version = sys.argv[index + 1]
    sys.argv.pop(index)
    sys.argv.pop(index)


with pathlib.Path("requirements.txt").open() as requirements_file:
    install_requires = [
        line.strip()
        for line in requirements_file
        if (line.strip() and not line.startswith("#") and not line.startswith("--"))
    ]


setup(
    name="telescope",
    version=version,
    license="MIT",
    description="Your VCs best friend",
    author="Alberto Rincones",
    author_email="alberto.rincones@code4road.com",
    url="https://github.com/c4road/telescope",
    download_url="",
    keywords=["finance", "investment", "vc", "venture capital"],
    install_requires=install_requires,
    packages=["company", "telescope"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
)
