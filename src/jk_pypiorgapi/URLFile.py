#
# NOTE: This is a copy of pypine.do.URLFile.
#		This copy is necessary to avoid unnecessary dependencies to 'pypine'.
# 		Package 'pypine' will always contain the most recent version of URLFile.
#





import sys
import os
import typing
import datetime
import json

import requests

import jk_furl
import jk_prettyprintobj

#from ..FileTypeInfo import FileTypeInfo





_EPOCH = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)




class URLFile(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self,
			url:str,
		):

		# normalize

		furl = jk_furl.furl(url)
		furl.path = str(furl.path).replace("//", "/")

		# ----

		self.__surl = str(furl)
		self.__furl = furl

		assert self.__furl.scheme
		assert self.__furl.host
		assert self.__furl.port

		self.__bHeadRequested = False
		self.__bContentRequested = False

		self.__httpStatusCode = -1
		self.__contentLength = None
		self.__contentCharset = None
		self.__contentMimeType = None
		self.__contentTimeStampDT = None
		self.__contentTimeStampSecs = None

		self.__bContentIsBinary = False
		self.__bContentIsText = False
		self.__bContentIsJSON = False
		self.__content = None

		# ----

		self.meta = {}
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def dataType(self) -> str:
		return "url"
	#

	@property
	def exists(self) -> bool:
		if not self.__bHeadRequested:
			self.__retrieveMetaData()
		if (self.__contentMimeType is not None) and (200 <= self.__httpStatusCode < 400):
			return True
		else:
			return False
	#

	"""
	@property
	def fileTypeInfo(self) -> FileTypeInfo:
		return self.__fileTypeInfo
	#
	"""

	@property
	def isDir(self) -> bool:
		return self.relFilePath.endswith("/")
	#

	#
	# Provides information about the remote host and how to contact it for retrieving data.
	# Returns an identifier such as "https:i.pinimg.com:443" that provides information about from where the data is retrieved.
	#
	@property
	def remoteHostLocation(self) -> str:
		return "{}:{}:{}".format(self.__furl.scheme, self.__furl.host, self.__furl.port)
	#

	@property
	def furl(self) -> jk_furl.furl:
		return self.__furl
	#

	@property
	def relDirPath(self) -> typing.Union[str,None]:
		s = str(self.__furl.path)
		if s.startswith("/"):
			s = s[1:]
		if not s.endswith("/"):
			pos = s.rfind("/")
			s = s[:pos]
		if s:
			return s
		else:
			return None
	#

	#
	# The name of this entry
	#
	@property
	def fileName(self) -> typing.Union[str,None]:
		s = str(self.__furl.path)
		if s.startswith("/"):
			s = s[1:]
		if s.endswith("/"):
			return None
		pos = s.rfind("/")
		if pos < 0:
			if s:
				return s
			else:
				return None
		else:
			ret = s[pos+1:]
			if ret:
				return ret
			else:
				return None
	#

	"""
	n/a
	#
	# This is the absolute path of this entry.
	#
	@property
	def fullPath(self) -> str:
		return None
	#
	"""

	@property
	def relFilePath(self) -> str:
		s = str(self.__furl.path)
		if s.startswith("/"):
			s = s[1:]
		return s
	#

	@property
	def url(self) -> str:
		return self.__surl
	#

	@property
	def mimeType(self) -> str:
		return self.__contentMimeType
	#

	"""
	n/a
	@property
	def absFilePath(self) -> str:
		return None
	#

	@property
	def absDirPath(self) -> str:
		return None
	#

	@property
	def isBinary(self) -> bool:
		return bool(self.__binaryData)
	#

	@property
	def isText(self) -> bool:
		return bool(self.__textData)
	#
	"""

	@property
	def isLocal(self) -> bool:
		return False
	#

	@property
	def isLocalOnDisk(self) -> bool:
		return False
	#

	@property
	def timeStampI(self) -> typing.Union[int,None]:
		return self.getTimeStampI()
	#

	@property
	def timeStamp(self) -> typing.Union[float,int,None]:
		return self.getTimeStamp()
	#

	@property
	def fileSize(self) -> typing.Union[int,None]:
		return self.getFileSize()
	#

	@property
	def httpStatus(self) -> int:
		if not self.__bHeadRequested:
			self.__retrieveMetaData()
		return self.__httpStatusCode
	#

	@property
	def contentCharset(self) -> typing.Union[str,None]:
		if not self.__bHeadRequested:
			self.__retrieveMetaData()
		return self.__contentCharset
	#

	@property
	def isJSON(self) -> bool:
		if not self.__bHeadRequested:
			self.__retrieveMetaData()
		return self.__bContentIsJSON
	#

	@property
	def isText(self) -> bool:
		if not self.__bHeadRequested:
			self.__retrieveMetaData()
		return self.__bContentIsText
	#

	@property
	def isBinary(self) -> bool:
		if not self.__bHeadRequested:
			self.__retrieveMetaData()
		return self.__bContentIsBinary
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"url",
			"remoteHostLocation",
			"dataType",
			"exists",
			"isDir",
			"relFilePath",
			"relDirPath",
			"fileName",
			"mimeType",
			"contentCharset",
			"isLocal",
			"isLocalOnDisk",
			"timeStamp",
			"timeStampI",
			"fileSize",
			"httpStatus",
			"isBinary",
			"isText",
			"isJSON",
		]
	#

	def __retrieveMetaData(self):
		self.__bContentIsBinary = False
		self.__bContentIsText = False
		self.__bContentIsJSON = False
		self.__contentMimeType = None
		self.__contentCharset = None
		self.__contentLength = None
		self.__httpStatusCode = -1

		try:
			r = requests.head(self.__surl)

			self.__httpStatusCode = r.status_code

			if r.status_code != 404:
				s = r.headers["content-type"]
				if s:
					pos = s.find(";")
					if pos < 0:
						self.__contentMimeType = s
					else:
						self.__contentMimeType = s[:pos].strip()
						s = s[pos+1:].strip()
						if s.lower().startswith("charset="):
							self.__contentCharset = s[8:].lower()
						else:
							raise Exception("?????? " + repr(s))

					# guess content type
					if self.__contentMimeType == "application/json":
						self.__bContentIsText = True
						self.__bContentIsJSON = True
					elif self.__contentMimeType.startswith("text/"):
						self.__bContentIsText = True
					else:
						self.__bContentIsBinary = True

				#self.__contentLength = r.headers["content-length"] if "content-length" in r.headers else None

				if "last-modified" in r.headers:
					self.__contentTimeStampDT = datetime.datetime.strptime(r.headers["last-modified"], "%a, %d %b %Y %H:%M:%S GMT")
					self.__contentTimeStampSecs = (self.__contentTimeStampDT - _EPOCH).total_seconds()

		except requests.ConnectionError as ee:
			self.__httpStatusCode = 404

		self.__bHeadRequested = True
	#

	def __retrieveData(self):
		self.__bContentIsBinary = False
		self.__bContentIsText = False
		self.__bContentIsJSON = False
		self.__contentMimeType = None
		self.__contentCharset = None
		self.__contentLength = None
		self.__httpStatusCode = -1
		self.__content = None

		try:
			r = requests.get(self.__surl)

			self.__httpStatusCode = r.status_code

			if r.status_code != 404:
				s = r.headers["content-type"]
				if s:
					pos = s.find(";")
					if pos < 0:
						self.__contentMimeType = s
					else:
						self.__contentMimeType = s[:pos].strip()
						s = s[pos+1:].strip()
						if s.lower().startswith("charset="):
							self.__contentCharset = s[8:].lower()
						else:
							raise Exception("?????? " + repr(s))

					# guess content type
					if self.__contentMimeType == "application/json":
						self.__bContentIsText = True
						self.__bContentIsJSON = True
					elif self.__contentMimeType.startswith("text/"):
						self.__bContentIsText = True
					else:
						self.__bContentIsBinary = True

				#self.__contentLength = r.headers["content-length"] if "content-length" in r.headers else None

				if "last-modified" in r.headers:
					self.__contentTimeStampDT = datetime.datetime.strptime(r.headers["last-modified"], "%a, %d %b %Y %H:%M:%S GMT")
					self.__contentTimeStampSecs = (self.__contentTimeStampDT - _EPOCH).total_seconds()

				if self.__bContentIsText:
					self.__content = r.text
				else:
					# binary
					self.__content = r.content
					self.__contentLength = len(self.__content)

		except requests.ConnectionError as ee:
			self.__httpStatusCode = 404

		self.__bHeadRequested = True
		self.__bContentRequested = True
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	"""
	def clone(self):
		if self.__textData is not None:
			# this file stores text data
			return InMemoryFile(self.__relFilePath, self.__fileTypeInfo, self.__textData)
		else:
			# this file stores binary data
			return InMemoryFile(self.__relFilePath, self.__fileTypeInfo, self.__binaryData)
	#"""

	def __str__(self):
		return "URLFile<({})>".format(repr(self.__surl))
	#

	def __repr__(self):
		return "URLFile<({})>".format(repr(self.__surl))
	#

	def getTimeStamp(self) -> typing.Union[float,None]:
		if self.__contentTimeStampDT:
			return self.__contentTimeStampSecs
		return None
	#

	def getTimeStampI(self) -> typing.Union[int,None]:
		ret = self.getTimeStamp()
		if ret is None:
			return ret
		return int(ret)
	#

	def getFileSize(self) -> typing.Union[int,None]:
		if not self.__bHeadRequested:
			self.__retrieveMetaData()

		if (self.__contentLength is None) and (self.__content is not None) and isinstance(self.__content, str):
			self.__contentLength = len(self.__content.encode("utf-8"))

		return self.__contentLength
	#

	"""
	def readBinary(self):
		if self.__textData is None:
			return self.__binaryData
		else:
			return self.__textData.encode("utf-8")
	#

	def readText(self):
		if self.__textData is None:
			raise Exception("Not a text file!")
		else:
			return self.__textData
	#
	"""

	def readJSON(self) -> typing.Union[str,int,float,bool,dict,list,None]:
		if not self.__bContentRequested:
			self.__retrieveData()
		if self.__bContentIsJSON:
			return json.loads(self.__content)
		else:
			return None
	#

	def readText(self) -> typing.Union[str,None]:
		if not self.__bContentRequested:
			self.__retrieveData()
		if self.__bContentIsText:
			return self.__content
		else:
			return None
	#

	def readBinary(self) -> typing.Union[bytes,None]:
		if not self.__bContentRequested:
			self.__retrieveData()
		if self.__bContentIsBinary:
			return self.__content
		elif self.__bContentIsText:
			return self.__content.encode("utf-8")
		else:
			return None
	#

#




