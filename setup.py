from setuptools import setup


with open('README.md', encoding='utf-8') as readme:
    long_description = readme.read()

INSTALL_REQUIRE = []
TESTS_REQUIRE = ["twine>=3.2.0"]

setup(
    author="Christopher Malcolm",
    author_email="chris.c.malcolm.96@gmail.com",
    name="jspec",
    version="2.1.3",
    description="JSPEC is a powerful yet simple and lightweight JSON validation module",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/chrismalcolm/jspec",
    packages=["jspec"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=INSTALL_REQUIRE,
    tests_require=TESTS_REQUIRE
)