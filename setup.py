from setuptools import setup

setup(
    name="botometer",
    version="2.0.1",
    description="Check Twitter accounts for bot behavior",
    url="https://github.com/osome-iu/botometer-python",
    author="Kai-Cheng Yang",
    author_email="yang3kc@gmail.com",
    license="MIT",
    packages=["botometer"],
    install_requires=["requests"],
)
