import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Vlad Herasymenko",
    author_email="drimacus182@gmail.com",
    name='prozorro_api',
    license="MIT",
    description='prozorro_api is a wrapper package for interaction with a well-known Ukrainian procurement database',
    version='v0.0.1',
    long_description=README,
    # url='',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['requests', 'retry'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)