import io
import re

from setuptools import setup


with io.open('README.md', encoding='utf-8') as f:
    readme = f.read()


with io.open('snaut.py', encoding='utf-8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(
    name='snaut',
    version=version,
    description='Artifact upload tool for Sonatype Nexus 3',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/perewall/snaut',
    install_requires=[
        'click >=7.0, <8.0',
        'requests >=2.0, <3.0',
        'python_dotenv >=0.10, <1.0'
    ],
    setup_requires=['wheel', 'setuptools >=40'],
    tests_require=['responses >=0.10, <1.0'],
    entry_points={'console_scripts': ['snaut = snaut:upload']},
    py_modules=['snaut'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
