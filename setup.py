from setuptools import setup

setup(
    name="Gherkin Processor",
    version="0.1.0",
    description="Gherkin Processor is a Python package that processes Gherkin files into Python dataclasses. It provides utilities for validating, processing, and saving Gherkin in both text and Json formats.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Mark Lehoczky",
    author_email="mark.lehoczky@gmail.com",
    url="https://github.com/marklehoczky/gherkin-processor",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: BDD"
    ],
    entry_points={
        "console_scripts": [
            "gherkin-processor=gherkin_processor:main",
        ]
    },
    license="MIT License",
    package_dir= {},
    python_requires=">=3.10"
)
