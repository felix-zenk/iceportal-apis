import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iceportal_apis",
    version="1.0.8",
    author="Felix Zenk",
    author_email="",
    description="A module for interacting with the Deutsche Bahn onboard APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felix-zenk/iceportal-apis",
    project_urls={
        "Bug Reports": "https://github.com/felix-zenk/iceportal-apis/issues/new?labels=bug&template=bug_report.md&title=%5BBUG%5D%3A+",
        "Documentation": "https://iceportal-apis.readthedocs.io/en/latest/",
        "Source": "https://github.com/felix-zenk/iceportal-apis",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires='>=3.6',
)