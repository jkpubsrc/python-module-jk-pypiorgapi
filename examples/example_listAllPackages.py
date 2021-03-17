#!/usr/bin/python3




import jk_pypiorgapi



api = jk_pypiorgapi.PyPiOrgAPI()

n = len(api.listAllPackages())

print("Number of packages on pypi.org:", n)








