from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="blacksheep-sqlalchemy",
    version="0.0.2",
    description="Extension for BlackSheep to use SQLAlchemy",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Neoteroi/BlackSheep-SQLAlchemy",
    author="RobertoPrevato",
    author_email="roberto.prevato@gmail.com",
    keywords="blacksheep sqlalchemy orm database",
    license="MIT",
    packages=["blacksheepsqlalchemy"],
    install_requires=["blacksheep", "SQLAlchemy"],
    include_package_data=True,
    zip_safe=False,
)
