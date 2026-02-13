from setuptools import setup, find_packages

setup(
    name='Topsis-Naman-102316108',
    version='0.0.1',
    author='Naman',
    author_email='njain_be23@thapar.edu',
    description='TOPSIS implementation as a command line tool',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
        'pandas',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'topsis=Topsis-Naman-102316108.topsis:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3', 
        'Programming Language :: Python :: 3.11',
        "Operating System :: OS Independent", 
    ],
)