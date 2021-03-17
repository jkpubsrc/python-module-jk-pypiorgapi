#!/usr/bin/python3




import jk_pypiorgapi
import jk_json



api = jk_pypiorgapi.PyPiOrgAPI()

jData = api.getPackageInfoJSON("jk_pypiorgapi")

jk_json.prettyPrint(jData)








