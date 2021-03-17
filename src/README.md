jk_pypiorgapi
==========

Introduction
------------

This python module provides an API for accessing Python packet information hosted on pypi.org.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/....)
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

### List existing packages

If you want to retrieve information about a certain package hosted on `pypi.org`, you can use this method:

```python
jData = api.getPackageInfoJSON("jk_pypiorgapi")
```

This will look up the package `jk_pypiorgapi` and retrieve all information about it as a JSON data structure. This method directly provides the information `pypi.org` provides
via its API.

NOTE: For experimenting you might want to display this data in an easy way. [`jk_json`](https://pypi.org/project/jk-json/) provides a convenience method named `prettyPrint()` for that purpose:

```python
import jk_json
jk_json.prettyPrint(jData)
```

Author(s)
-------------------

* Jürgen Knauth: pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



