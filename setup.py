from setuptools import setup
from setuptools import find_packages

install_requires = [
    'six==1.11.0',
    'pyyaml==3.12',
    'ipaddress==1.0.19',
    'tinydb==3.7.0',
    'beautifultable==0.3.0',
    'logger==1.4',
    'flask==0.12.2',
    'jsonschema==2.6.0',
    'mCli'
]
dependency_links = [
     "git+http://github.com/sureshkvl/mCli#egg=mCli-1.0"
    ]
test_requires = []

setup(
    name='KNet',
    version='1.0',
    description="Virtual Network Topology Builder",
    author="KNet Solutions",
    author_email="knetsolutions2@gmail.com",
    url="knetsolutions.in",
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    scripts=[],
    license="Apache",
    entry_points={
        'console_scripts': ['knet-cli=KNet.cli:main'],
    },
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: Apache License',
        'Programming Language :: Python :: 2.7'
    ]
)
