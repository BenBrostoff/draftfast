import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

requires = [
    'numpy==1.10.4',
    'terminaltables==3.1.0',
    'draft-kings-db==0.1.2',
    'ortools==6.7.4973',
]

setuptools.setup(
    name='draftfast',
    version='0.0.8',
    author='Ben Brostoff',
    author_email='ben.brostoff@gmail.com',
    description='A tool to automate and optimize DraftKings and FanDuel lineup construction.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BenBrostoff/draft-kings-fun',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=requires,
)