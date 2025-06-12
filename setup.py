#!/usr/bin/env python3
"""
Setup script for HumanMouse package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from the package
def get_version():
    """Get version from the package __init__.py"""
    version_file = this_directory / "smart_mouse" / "__init__.py"
    version_content = version_file.read_text(encoding='utf-8')
    for line in version_content.split('\n'):
        if line.startswith('__version__'):
            # Extract version string from line like: __version__ = "1.0.0"
            return line.split('"')[1]
    return "1.0.0"

setup(
    name="smart-mouse",
    version=get_version(),
    author="HumanMouse Team",
    author_email="contact@humanmouse.com",
    description="Human-like mouse movement simulation using recorded patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bandit-HaxUnit/humanmouse",
    project_urls={
        "Bug Tracker": "https://github.com/Bandit-HaxUnit/humanmouse/issues",
        "Documentation": "https://github.com/Bandit-HaxUnit/humanmouse#readme",
        "Source Code": "https://github.com/Bandit-HaxUnit/humanmouse",
    },
    packages=find_packages(),
    package_data={
        "smart_mouse": ["mousedata.json"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Operating System",
        "Topic :: Desktop Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="mouse movement automation human-like simulation robotics ui testing",
    python_requires=">=3.7",
    install_requires=[
        "pynput>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.910",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            # Add CLI commands if needed in the future
        ],
    },
    zip_safe=False,
)
