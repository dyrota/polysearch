from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='polysearch',
    version='0.0.1',
    description='A collection of state space search algorithms.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Chase Burton Taylor',
    author_email='ctaylor@citycollege.sheffield.eu',
    url='https://github.com/chaseburton/polysearch',
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
