from pathlib import Path
from setuptools import setup, find_packages

setup(
    name="iceportal_apis",
    version='2.0.3',
    author='Felix Zenk',
    author_email='felix.zenk@web.de',
    description="A module for interacting with the Deutsche Bahn onboard APIs",
    long_description=Path('README.md').read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    url="https://github.com/felix-zenk/iceportal-apis",
    project_urls={
        "Bug Reports": "https://github.com/felix-zenk/iceportal-apis/issues/new?labels=bug&template=bug_report.md&title=%5BBUG%5D%3A+",
        "Source": "https://github.com/felix-zenk/iceportal-apis",
    },
    packages=find_packages(include=['iceportal_apis', 'iceportal_apis.*']),
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
    python_requires='>=3.8',
)
