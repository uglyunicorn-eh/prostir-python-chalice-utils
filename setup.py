import setuptools

with open("VERSION", "r", encoding="utf-8") as f:
    VERSION = f.read().strip()

cmdclass = {}

setuptools.setup(
    name="prostir-chalice-utils",
    url="https://github.com/uglyunicorn-eh/prostir-chalice-utils",
    maintainer="Ugly Unicorn",
    maintainer_email="info@uglyunicorn.ca",
    version=VERSION,
    cmdclass=cmdclass,
    namespace="prostir",
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
