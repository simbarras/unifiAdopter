import setuptools

setuptools.setup(
    name='unifiAdopter',
    version='2.5.1',
    description='Python project who add automaticly all antenna from a subnet to a distant controller',
    py_modules=["unifiAdopter", "paramiko"],
    package_dir={'': 'src'},
    author="Simon Barras",
    author_email="simon.barras02@gmail.com",
    url="https://github.com/simbarras/unifiAdopter",
    scripts=['unifiAdopter.py'],
)