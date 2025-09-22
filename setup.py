from setuptools import setup, find_packages

setup(
    name="guilite",
    version="0.1.0",
    description="A lightweight Python library for simulation and reporting.",
    author="Kjell Kolsaker",
    license="MIT",
    packages=find_packages(include=["app*", "reportgenerator*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "Flask",
        "pydantic>=1.10",
        "jinja2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
