import setuptools

with open("VERSION", "r", encoding="utf-8") as f:
    VERSION = f.read().strip()

cmdclass = {}

setuptools.setup(
    name="chalice_utils",
    url="https://github.com/uglyunicorn-eh/prostir-chalice-utils",
    maintainer="Ugly Unicorn",
    maintainer_email="info@uglyunicorn.ca",
    version=VERSION,
    cmdclass=cmdclass,
    packages=setuptools.find_packages(exclude=["*tests*"]),
    install_requires=[
        "graphene>=3.0",
        "sentry-sdk[chalice]",
    ],
    extras_require={
        "develop": [
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
