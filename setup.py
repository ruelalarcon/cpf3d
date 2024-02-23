from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
	name='cpf3d',
	version='1.0.0',
	license='MIT',
	description='A package for reading and writing 3cpf files.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	author='Ruel Nathaniel Alarcon',
	author_email='ruelnalarcon@gmail.com',
	url='https://github.com/ruelalarcon/cpf3d',
	project_urls={
		'Repository': 'https://github.com/ruelalarcon/cpf3d',
	},
	keywords=['3cpf', 'point', 'cloud', 'frames'],
	packages=find_packages(),
	install_requires=[
		'numpy',
	],
	extras_require={
		'dev': [
			'pytest',
		]
	},
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
		'Programming Language :: Python :: 3.11',
		'Programming Language :: Python :: 3.12',
	],
	python_requires='>=3.8',
)
