"""Setup file."""

from setuptools import find_packages, setup

if __name__ == "__main__":
    with open("README.md", "r", encoding="utf-8") as readme:
        setup(
            name="gherkin-processor",
            version="0.0.1",
            author="Mark Lehoczky",
            author_email="mark.lehoczky@gmail.com",
            description="A Python package that converts Gherkin scenarios into Python `dataclass` objects.",
            long_description=readme.read(),
            long_description_content_type="text/markdown",
            url="https://github.com/MarkLehoczky/gherkin-processor",
            packages=find_packages(),
            classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],
            python_requires=">=3.10",
        )
