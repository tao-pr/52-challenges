import setuptools

with open("requirements.txt", "r") as f:
    reqs = [a.replace('\n','') for a in f.readlines()]

setuptools.setup(
    name="crawl-football-wiki",
    version="0.0.1",
    author="Tao P.R.",
    author_email="pataoengineer@gmail.com",
    description="Crawling football matches data from Wikipedia",
    long_description=long_description,
    url="https://github.com/tao-pr/52-challenges/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=reqs
)