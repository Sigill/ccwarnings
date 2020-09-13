import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
        name="gcc-warnings",
        version="0.0.1",
        author="Cyrille Faucheux",
        author_email="cyrille.faucheux@gmail.com",
        description="Utility to process warnings produced by GCC (and other tools producing GCC-like output).",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/Sigill/gcc-warnings",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Programming Language :: C",
            "Programming Language :: C++",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        python_requires='>=2.6',
        install_requires=requirements,
        scripts=['bin/gcc-warnings.py'],
        )
