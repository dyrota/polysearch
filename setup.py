from setuptools import setup, find_packages

setup(
    name='omnisearch',
    version='0.0.2',
    description='A collection of state space search algorithms.',
    author='Chase Burton Taylor',
    author_email='ctaylor@citycollege.sheffield.eu',
    url='https://github.com/chaseburton/omnisearch',
    packages=find_packages(),
    install_requires=[
        # None since heapq, abc, and time are built-in modules.
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)