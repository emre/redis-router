from distutils.core import setup

setup(
    name='redis-router',
    version='0.2',
    packages=['redis_router'],
    url='https://github.com/emre/redis-router',
    license='MIT',
    author='Emre Yilmaz',
    author_email='mail@emreyilmaz.me',
    description='A redis sharding library/api for your sharding needs.',
    install_requires = ['redis',]
)
