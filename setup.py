# ================================================== #
#                       SETUP                        #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 09/20/2022                                #
# Last Edited: 09/20/2022                            #
# ================================================== #
#                                                    #
# ================================================== #

from setuptools import setup, find_packages

setup(
    name='Cancer Crush API',
    version='0.0.1',
    license='GPLv3',
    description='Backend API for Cancer Crush game/learning tool.',
    author='Brady Hammond, Niharika Tippabhatla',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Games/Entertainment',
    ],
    install_requires=['click>=8.1',
    'falcon>=3.1',
    'waitress>=2.1',
    'PyYaml>=6.0',
    'falcon-auth[backend-jwt]',
    'mysql-connector-python>=8.0',
    'protobuf>=3.0',
    'waitress>=2.1',
    'msgpack>=1.0',
    'bcrypt>=4.0'],
    entry_points={
        'console_scripts': ['cc-start = cancer_crush.cli:main'],
    }
)

# ================================================== #
#                        EOF                         #
# ================================================== #
