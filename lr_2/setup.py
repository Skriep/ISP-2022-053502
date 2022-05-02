from setuptools import find_packages, setup


if __name__ == '__main__':
    setup(name='myserializer',
          version='1.0.0.dev1',
          description='JSON, YAML & TOML serializer',
          author='Skriep',
          packages=find_packages(
              where='src',
              include=['myserializer', 'myserializer.*']),
          package_dir={'': 'src'},
          python_requires='>=3.8.0'
          )
