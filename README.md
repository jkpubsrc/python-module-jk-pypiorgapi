jk_pypiorgapi
==========

Introduction
------------

This python module provides an API for accessing Python packet information hosted on pypi.org.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-pypiorgapi)
* [pypi.python.org](https://pypi.python.org/pypi/jk_pypiorgapi)

Why this module?
----------------

Apparently quite some people would like to retrieve information from `pypi.org`. As I was not able to find a suitable package quickly that already implemented
such behavior I decided to implement an own one and provide it publically.

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
import jk_pypiorgapi
```

### Instantiate the API object

In order to access the API you have to instantiate an API object. This is done as shown here:

```python
api = jk_pypiorgapi.PyPiOrgAPI()
```

NOTE: The reason behind that is simple: Code flexibility.
This way modifications and extensions will be possible if some things change with `pypi.org`.
So please first instantiate an API object, then you can use it.

### List existing packages

If you want to access a list of all packages hosted on `pypi.org`, you can use this method:

```python
packageNames = api.listAllPackages()
```

Please be aware that invoking this method **is expensive**. The reason why calling is method is expensive is that the package index nowadays has over 16 MBytes in size.
Please use this method wisely to avoid server load on `pypi.org` and do not download the package index too frequently!

### Search for packages

Here is an example how to search for specific packages:

```python
for jData in api.iteratePackagesByClassifier(
		searchTerm="jk_pypiorgapi",
		classifiers=[
			"Development Status :: 5 - Production/Stable",
			"Development Status :: 6 - Mature",
		]
	):

	print(jData)		# do something with the search result here
```

As the method `iteratePackagesByClassifier()` returns an iterator you need to loop through the results. The objects returned by `iteratePackagesByClassifier()` is an instance of `PyPiPackage` which provides the following properties:

| Data Type		| Name				| Description		|
| ---			| ---				| ---				|
| int			| nResultNo			| The result index number. This is a counter starting at zero, enumerating all results.	|
| int			| nMaxResults		| The number of results to be expected. (Don't rely on it, neither can all be iterated if this value is too large, nor does it need to remain unchanged during the iteration.)	|
| str			| pkgName			| The name of the package.			|
| str			| pkgVersion		| The version of the package.		|
| str			| pkgDescription	| The description of the package.	|

### Get information about an existing packages

If you want to retrieve information about a certain package hosted on `pypi.org`, you can use this method:

```python
jData = api.getPackageInfoJSON("jk_pypiorgapi")
```

This will look up the package `jk_pypiorgapi` and retrieve all information about it as a JSON data structure. This method directly provides the information `pypi.org` provides
via its API.

NOTE: For experimenting purposes you might want to display this data in an easy way. [`jk_json`](https://pypi.org/project/jk-json/) provides a convenience method named `prettyPrint()` for that purpose:

```python
import jk_json

jk_json.prettyPrint(jData)
```

Dependencies
-------------------

This module has the following dependencies:

* [bs4](https://pypi.org/project/beautifulsoup4/) for HTML parsing
* [jk_furl](https://github.com/jkpubsrc/python-module-jk-furl) for more convenient URL handling
* [jk_prettyprintobj](https://github.com/jkpubsrc/python-module-jk-prettyprintobj) for pretty printing objects for debugging

Author(s)
-------------------

* Jürgen Knauth: pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



