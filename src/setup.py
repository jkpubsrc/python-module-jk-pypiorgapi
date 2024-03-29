################################################################################
################################################################################
###
###  This file is automatically generated. Do not change this file! Changes
###  will get overwritten! Change the source file for "setup.py" instead.
###  This is either 'packageinfo.json' or 'packageinfo.jsonc'
###
################################################################################
################################################################################


from setuptools import setup

def readme():
	with open("README.md", "r", encoding="UTF-8-sig") as f:
		return f.read()

setup(
	author = "Jürgen Knauth",
	author_email = "pubsrc@binary-overflow.de",
	classifiers = [
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python :: 3",
	],
	description = "An API for accessing Python packet information hosted on pypi.org",
	include_package_data = False,
	install_requires = [
		"bs4",
		"jk_furl",
		"jk_prettyprintobj",
	],
	keywords = [
		"pypi",
		"pypi.org",
	],
	license = "Apache2",
	name = "jk_pypiorgapi",
	package_data = {
		"": [
		],
	},
	packages = [
		"jk_pypiorgapi",
	],
	scripts = [
	],
	version = '0.2022.6.13',
	zip_safe = False,
	long_description = readme(),
	long_description_content_type = "text/markdown",
)
