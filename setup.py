from setuptools import setup, find_packages

with open('requirements.txt') as fp:
    install_requires = fp.read().splitlines()


def get_version():
    try:
        return open('version.txt').read().strip()
    except IOError:
        return ''


setup(
    name='shore_app',
    version=get_version() or '0.0-dev',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=[
        'setuptools_git==1.1',  # anything tracked in git gets packaged
        'wheel==0.24.0',
    ],
    zip_safe=False,
)
