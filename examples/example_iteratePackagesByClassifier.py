#!/usr/bin/python3


import jk_pypiorgapi





api = jk_pypiorgapi.PyPiOrgAPI()
for jData in api.iteratePackagesByClassifier(
		searchTerm="jk_pypiorgapi",
		classifiers=[ "Development Status :: 5 - Production/Stable" ]
	):

	print(jData)






