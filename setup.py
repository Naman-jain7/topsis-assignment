from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")
setup(
    name="topsis-naman-102316108",
    version="0.0.2",
    author="Naman",
    author_email="njain_be23@thapar.edu",
    description="TOPSIS implementation as a command line tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=["pandas", "numpy"],
    entry_points={"console_scripts": ["topsis=Topsis_Naman_102316108.topsis:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
)
