import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

requires = [
    'numpy==1.24.2',
    'terminaltables==3.1.0',
    'ortools== 9.8.3296',
]

setuptools.setup(
    name='draftfast',
    version='3.10.0',
    author='Ben Brostoff',
    author_email='ben.brostoff@gmail.com',
    description='A tool to automate and optimize DraftKings and FanDuel '
                'lineup construction.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BenBrostoff/draftfast',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=requires,
)
