from setuptools import setup

setup(name='botornot',
      version='0.1',
      description='Check Twitter accounts for bot behavior',
      url='https://github.com/truthy/botornot-python',
      author='Clayton A Davis',
      author_email='claydavi@indiana.edu',
      license='MIT',
      packages=['botornot'],
      install_requires=[
          'requests',
          'tweepy',
          ],
      )
