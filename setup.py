from setuptools import setup

setup(name='botornot',
      version='0.2',
      description='Check Twitter accounts for bot behavior',
      url='https://github.com/truthy/botornot-python',
      download_url='https://github.com/truthy/botornot-python/archive/0.2.zip',
      author='Clayton A Davis',
      author_email='claydavi@indiana.edu',
      license='MIT',
      packages=['botornot'],
      install_requires=[
          'requests',
          'tweepy',
          ],
      )
