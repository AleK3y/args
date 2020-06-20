#!/usr/bin/python3

import sys

class Arguments:

	INDENTATION = 4

	# Exceptions
	class MissingMandatoryArgument(Exception):
		def __init__(self, arg):
			self.strerror = arg
			self.args = {arg}

	info = {}
	args = {}

	def __init__(self, info):
		self.info = info

	def get_args(self):
		return self.args

	def update_args(self):
		"""
		Update the arguments from sys.argv.
		"""

		i = 0
		while i<len(sys.argv):

			# Check for the options with parameters
			if sys.argv[i] in self.info["parameters"]:
				self.args[sys.argv[i]] = sys.argv[i+1]
				i += 1		# Skip the parameter

			# Check for single options
			elif sys.argv[i] in self.info["options"]:
				self.args[sys.argv[i]] = None		# Options which are supposed to go alone don't have parameters

			i += 1

		# Check if there are mandatory arguments missing
		for arg in self.info["parameters"]:
			if arg not in self.args and self.info["parameters"][arg]["required"]:
				raise self.MissingMandatoryArgument(f"'{arg}' is missing")

		# obligatory args on options is kinda useless
		for arg in self.info["options"]:
			if arg not in self.args and self.info["options"][arg]["required"]:
				raise self.MissingMandatoryArgument(f"'{arg}' is missing")

	def usage(self):
		"""
		Print the usage with descriptions.
		"""

		print("Usage: " + self.info["usage"])
		
		for line in self.info["description"].split("\n"):
			print(" "*self.INDENTATION + line)
		
		print()

		params = self.info["parameters"]
		opts = self.info["options"]
		merged = dict(list(params.items()) + list(opts.items()))

		for arg in merged:
			print(
				" "*(self.INDENTATION+1) + arg +
				" "*self.INDENTATION*2 + merged[arg]["description"]
			, end="")

			if not merged[arg]["required"]:
				print(" (optional)", end="")

			print()
