from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in frappe_example/__init__.py
from frappe_example import __version__ as version

setup(
	name='frappe_example',
	version=version,
	description='Librarian Management System',
	author='Author',
	author_email='test@example.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
