from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='CheckMyTex',
      version='0.0.2',
      description='A simple tool for checking complex LaTeX documents, e.g., dissertations.',
      long_description=readme(),
      long_description_content_type="text/markdown",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      keywords='LaTeX',
      url='https://github.com/d-krupke/checkmytex',
      author='Dominik Krupke',
      author_email='krupke@ibr.cs.tu-bs.de',
      license='MIT',
      packages=['checkmytex'],
      install_requires=["pyspellchecker", "flachtex", "yalafi"],
      entry_points={
          'console_scripts': ['checkmytex=checkmytex.cli:main'],
      },
      python_requires='>=3.7',
      include_package_data=True,
      zip_safe=False)
