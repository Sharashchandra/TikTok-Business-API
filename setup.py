import os

from setuptools import find_packages, setup

setup(
    name="TikTok-Business-API",
    python_requires=">3.8",
    version="1.6",
    author="Sharashchandra Desai",
    author_email="sharashchandra.desai@gmail.com",
    url="https://github.com/Sharashchandra/TikTok-Business-API",
    description="Minimal api wrapper for the TikTok Business API",
    long_description=os.path.join(os.path.dirname(__file__), "README.md"),
    packages=find_packages(exclude=["examples", "tests"]),
    install_requires=[
        "requests",
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords="tiktok business api wrapper",
)
