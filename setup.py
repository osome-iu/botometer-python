from setuptools import setup

setup(name='botometer',
      version='1.6',
      description='Check Twitter accounts for bot behavior',
      url='https://github.com/IUNetSci/botometer-python',
      download_url='https://github.com/IUNetSci/botometer-python/archive/1.0.zip',
      author='Clayton A Davis, Kai-Cheng Yang',
      author_email='claydavi@indiana.edu,yangkc@iu.edu',
      license='MIT',
      packages=['botometer'],
      install_requires=[
          'requests',
          'tweepy >= 3.5.0',
          ],
      )
