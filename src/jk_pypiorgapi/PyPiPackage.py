


import collections



#
# Instances of this class represent pypi.org search results.
#
# @field	int nResultNo			The result index number. This is a counter starting at zero, enumerating all results.
# @field	int nMaxResults			The number of results to be expected. (Don't rely on it, neither can all be iterated if this value is too large,
#									nor does it need to remain unchanged during the iteration.)
# @field	str pkgName				The name of the package.
# @field	str pkgVersion			The version of the package.
# @field	str pkgDescription		The description of the package.
#
PyPiPackage = collections.namedtuple("PyPiPackage", [
	"nResultNo",
	"nMaxResults",
	"pkgName",
	"pkgVersion",
	"pkgDescription",
])






