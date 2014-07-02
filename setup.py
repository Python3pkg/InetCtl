from setuptools import setup

setup(name='inetctl',
      version='0.1',
      description='Network control made easy',
      url='https://github.com/drobban/InetCtl',
      author='drobban',
      author_email='david.robertsson@gmail.com',
      license='MIT',
      packages=['inetctl'],
      install_requires=[
          'netifaces',
      ],
      zip_safe=False)
