from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="zero-scale",
    version="0.0.1",
    author="Adam Cathersides",
    author_email="a.cathersides@livelinktechnology.net",
    description=("Scale deploy to zero"),
    url='',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=['click==8.1.3',
                      'click-log==0.4.0',
                      'kubernetes==26.1.0',
                      'tenacity==7.0.0'
                      ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
    entry_points={
          'console_scripts': [
              'zero-scale = zero_scale.cli:run',
          ]
      }
)
