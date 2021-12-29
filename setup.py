from setuptools import setup


with open('README.md', encoding='utf-8') as readme:
    long_description = readme.read()

INSTALL_REQUIRE = []
TESTS_REQUIRE = ["twine>=3.2.0"]

setup(
    author="Christopher Malcolm",
    author_email="chris.c.malcolm.96@gmail.com",
    name="jspec",
    version="2.0.1",
    description="A JSPEC is a tool that can used to check the elements and structure of a JSON.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/chrismalcolm/jspec",
    packages=["jspec"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=INSTALL_REQUIRE,
    test_require=TESTS_REQUIRE
)