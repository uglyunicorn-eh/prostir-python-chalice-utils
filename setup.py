import setuptools


def read_from_file(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().strip()


VERSION = read_from_file("VERSION")
PACKAGE = read_from_file("PACKAGE")
NAMESPACE = "prostir"

cmdclass = {}

setuptools.setup(
    name=f"prostir-{PACKAGE}",
    url=f"https://github.com/uglyunicorn-eh/prostir-{PACKAGE}",
    maintainer="Ugly Unicorn",
    maintainer_email="info@uglyunicorn.ca",
    version=VERSION,
    cmdclass=cmdclass,
    namespace=NAMESPACE,
    packages=setuptools.find_namespace_packages(exclude=["*tests*"]),
    install_requires=[
        "graphene>=3.0",
        "sentry-sdk",  # do not include [chalice], that would add boto3 to the final package due to dependecies
    ],
    extras_require={
        "develop": [
            "black",
            "coverage",
            "pylint",
            "pytest-cov",
            "pytest",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
            "myst-parser",
        ],
    },
)
