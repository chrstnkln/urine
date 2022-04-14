import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

tests_require = [
    'pytest>=7.0.0',
    'pytest-cov>=3.0.0',
]

lint_requires = [
    'flake8>=4.0.1',
    'isort>=5.10.1',
]

dev_requires = [
    *tests_require,
    *lint_requires,
    'tox>=3.25.0',
]


setuptools.setup(
    name='urine',
    version='0.1.0',
    author='Christian Klein',
    author_email='klein_chris@outlook.com',
    description='Simple and secure binary serialization for Python objects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chrstnkln/urine',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'lint': lint_requires,
        'dev': dev_requires
    },
    python_requires='>=3.6',
)
