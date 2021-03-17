



import time




class _CachedValue(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, valueProviderCallback, keepSeconds:int = 60, autoRenewKeep:bool = True):
		assert callable(valueProviderCallback)
		assert isinstance(keepSeconds, int)
		assert isinstance(autoRenewKeep, bool)

		# ----

		self.__keepSeconds = keepSeconds
		self.__autoRenewKeep = autoRenewKeep
		self.__valueProviderCallback = valueProviderCallback

		self.__value = None
		self.__t = 0
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __call__(self, *args, **kwargs):
		t = time.time()
		if (t - self.__t > self.__keepSeconds):
			self.__value = self.__valueProviderCallback(*args, **kwargs)
			if self.__autoRenewKeep:
				self.__t = t
		return self.__value
	#

	def invalidate(self):
		self.__value = None
		self.__t = 0
	#

#





