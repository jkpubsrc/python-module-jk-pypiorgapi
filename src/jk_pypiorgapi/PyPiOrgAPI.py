

import re
import json
import typing
import urllib.parse

from bs4 import BeautifulSoup





from ._CachedValue import _CachedValue
from .URLFile import URLFile






class PyPiOrgAPI(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, keepSeconds:int = 120):
		self.__listAllPackages = _CachedValue(self.__listAllPackagesCallback, keepSeconds=keepSeconds)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __listAllPackagesCallback(self, log) -> list:
		url = URLFile("https://pypi.org/simple/")

		allPackages = []
		for line in url.readText().split("\n"):
			#m = re.match("<a\s+href=\"(/simple/[^/]+/)\">([^<]+)</a>", line)
			m = re.match(r"\s+<a\shref=\"(/simple/.+?/)\">(.+?)</a>", line)
			if m:
				g1 = m.groups(1)
				g2 = m.groups(2)
				if g1 != g2:
					if log:
						log.warn("Differing names: {} and {}".format(repr(g1), repr(g2)))
				else:
					allPackages.append(g1)
		return allPackages
	#

	def __saveBS4Tree(self, bs4data, fileName:str):
		with open(fileName, "w") as fout:
			for line in bs4data.prettify().split("\n"):
				m = re.match("^\s+", line)
				if m:
					s = line[:m.end()]
					fout.write(("\t" * len(s)) + line[len(s):] + "\n")
	#

	def __parsePackageSearchResultLI(self, xLI) -> list:
		packageName = xLI.a.h3.find("span", { "class": "package-snippet__name" }).text.strip()
		packageVersion = xLI.a.h3.find("span", { "class": "package-snippet__version" }).text.strip()
		packageDescription = xLI.a.find("p", { "class": "package-snippet__description" }).text.strip()
		return (packageName, packageVersion, packageDescription)
	#

	def __parsePackageSearchResultPage(self, baseURL:URLFile, xPage) -> tuple:
		xDiv = xPage.find("div", { "class": "left-layout__main" })
		xForm = xDiv.find("form", { "action": "/search/" })
		#self.__saveBS4Tree(xForm, "xForm.html")

		sResults = xForm.div.div.p.strong.text.strip()
		sResults = sResults.replace(".", "")
		sResults = sResults.replace(",", "")
		if sResults.endswith("+"):
			sResults = sResults[:-1]
		nCountResults = int(sResults)

		xPagination = xForm.find("div", { "class": "button-group--pagination" })
		nMaxPage = -1
		if xPagination:
			#self.__saveBS4Tree(xPagination, "xPagination.html")
			for xA in xPagination.findChildren("a", recursive=False):
				sHREF = xA.get("href")
				if sHREF:
					m = re.search(r"page=([0-9]+)$", sHREF)
					if m:
						nPage = int(m.group(1))
						if nPage > nMaxPage:
							nMaxPage = nPage

		packageList = []
		xUL = xForm.find("ul")
		for xChildLI in xUL.findChildren("li", recursive=False):
			n, v, d = self.__parsePackageSearchResultLI(xChildLI)
			packageList.append((n, v, d))

		return nCountResults, nMaxPage, packageList
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Retrieves a list of PyPi package names from https://pypi.org and returns it.
	#
	# Please note that this value is typically cached for 120 seconds. Retrieving this list takes quite some time as about 16 MByte of data need
	# to be transferred. Therefore caching is mandatory here. Additionally you should not download that list too often.
	#
	# @return		str[]		Returns a list of PyPi package names.
	#							This method should always return a list. This method will only return <c>None</c>
	#							if data from the server could not be retrieved.
	#
	def listAllPackages(self, log = None) -> typing.Union[list,None]:
		return self.__listAllPackages(log)
	#

	#
	# This method retrieves information about a package and returns it
	#
	# @return		dict		Returns the raw JSON data.
	#							This method should always return a dictionary. This method will only return <c>None</c>
	#							if data from the server could not be retrieved, either because of a network error or
	#							because the specified package does not exist.
	#
	def getPackageInfoJSON(self, packageName:str, log = None) -> typing.Union[dict,None]:
		url = URLFile("https://pypi.org/pypi/" + packageName +"/json")
		return url.readJSON()
	#

	#
	# Returns an iterator with all search results.
	#
	# @return		int nResultNo			The result index number. This is a counter starting at zero, enumerating all results.
	# @return		int nMaxResults			The number of results to be expected. (Don't rely on it, neither can all be iterated if this value is too large,
	#										nor does it need to remain unchanged during the iteration.)
	# @return		str pkgName				The name of the package.
	# @return		str pkgVersion			The version of the package.
	# @return		str pkgDescription		The description of the package.
	#
	def iteratePackagesByClassifier(self, searchTerm:str, classifiers:list, log = None) -> typing.Union[list,None]:
		nPage = 1
		nMaxPage = -1

		nResultNo = 0
		while True:
			surl = "https://pypi.org/search/?q=" + urllib.parse.quote_plus(searchTerm) + "&page=" + str(nPage)
			if classifiers:
				surl += "&" + "&".join([ urllib.parse.quote_plus(c) for c in classifiers ])
			#log.notice("Retrieving: " + surl)
			url = URLFile(surl)

			xPage = BeautifulSoup(url.readText(), "lxml")
			#self.__saveBS4Tree(xPage, "out.html")

			nCountResults, nMaxPage, packageList = self.__parsePackageSearchResultPage(url, xPage)
			for n, v, d in packageList:
				yield nResultNo, nCountResults, n, v, d
				nResultNo += 1

			if (nMaxPage < 0) or (nPage >= nMaxPage):
				break
			nPage += 1
	#

#








