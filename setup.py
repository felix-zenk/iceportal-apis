import setuptools
from iceportal_apis import __version__, __author__, __email__

with open("README.md", "r") as fh:
    long_description = fh.read()

include_files = {'iceportal_apis': ['*.json', 'mocking/sample_data/*.json']}

setuptools.setup(
    name="iceportal_apis",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="A module for interacting with the Deutsche Bahn onboard APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felix-zenk/iceportal-apis",
    project_urls={
        "Bug Reports": "https://github.com/felix-zenk/iceportal-apis/issues/new?labels=bug&template=bug_report.md&title=%5BBUG%5D%3A+",
        "Source": "https://github.com/felix-zenk/iceportal-apis",
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        'Topic :: Utilities'
    ],
    python_requires='>=3.7.2',
)