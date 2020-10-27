class Arguments:

	##
	# Attributes
	#

	INDENTATION = 6
	DEFAULT_NAME = "VALUE"
	MAX_USAGE_PARAMETERS = 4

	info = None
	args = {
		"positional": [],
		"parameters": [],
		"options": []
	}

	##
	# Exceptions
	#

	class MissingRequiredArgument(Exception):
		pass
	class WrongArgumentsPlacement(Exception):
		pass
	class TooFewArguments(Exception):
		pass

	##
	# Functions
	#

	def __init__(self, info):
		if "arguments" not in info:
			raise ValueError()

		self.info = info
		info_args = self.info["arguments"]

		# Add missing sections
		for arg_type in self.args.keys():
			if arg_type not in info_args:
				info_args[arg_type] = {}

		# Add missing names on parameters
		for arg, value in info_args["parameters"].items():
			if "name" not in value:
				value["name"] = self.DEFAULT_NAME

	def get_args(self):
		return self.args

	def get_info(self):
		return self.info

	def update(self):
		import sys

		info_args = self.info["arguments"]

		## Parse the arguments ##

		i = 1
		while i<len(sys.argv):
			arg = sys.argv[i]

			# Parameters
			if arg in info_args["parameters"]:
				if i+1 >= len(sys.argv):
					raise self.WrongArgumentsPlacement(arg)

				self.args["parameters"].append({arg: sys.argv[i+1]})
				i += 1

			# Options
			elif arg in info_args["options"]:
				self.args["options"].append(arg)

			# Positional parameters
			else:
				self.args["positional"].append(arg)

			i += 1

		## Check for missing parameters ##

		for arg, value in info_args["parameters"].items():
			parsed = False
			for parsed_arg in self.args["parameters"]:
				if list(parsed_arg.keys())[0] == arg:
					parsed = True
					break

			if "required" in value and value["required"] and not parsed:
					raise self.MissingRequiredArgument(arg)

		if len(self.args["positional"]) < len(info_args["positional"].keys()):
			raise self.TooFewArguments()

	def usage(self):
		import sys

		info_args = self.info["arguments"]

		## Usage ##

		try:
			usage = self.info["usage"]
		except KeyError:
			info_args = self.info["arguments"]
			usage = sys.argv[0]

			# Add options to usage
			if len(info_args["options"].keys()) > 0:
				usage += " [OPTION]"

			required_count = 0
			for arg, value in info_args["parameters"].items():
				if "required" in value and value["required"]:
					required_count += 1

			# Add required parameters to usage if they're not too many
			if required_count <= self.MAX_USAGE_PARAMETERS:
				for arg, value in info_args["parameters"].items():
					if "required" in value and value["required"]:
						usage += " " + arg + " " + value["name"].upper()

			# Add positional parameters to usage line
			for arg, value in info_args["positional"].items():
				usage += " " + arg.upper()

		print(f"Usage: {usage}")
		print(
			" "*self.INDENTATION +
			((self.info["description"] + "\n") if "description" in self.info else "")
		)

		## Arguments help ##

		for arg_type in self.args.keys():
			if len(info_args[arg_type].keys()) > 0:
				print(" "*self.INDENTATION + arg_type.title() + ":")

				# Create a list of aliases and descriptions to print
				help_args = []
				for arg, value in info_args[arg_type].items():
					help_args.append([
						(
							(", ".join([arg] + value["aliases"]) if "aliases" in value else arg) + " " +		# Arguments and aliases
							(value["name"] if "name" in value else "").upper()		# Name
						),
						value["description"] if "description" in value else ""
					])

				# Find the longest argument line
				longest_arg = 0
				for arg in help_args:
					if len(arg[0]) > longest_arg:
						longest_arg = len(arg[0])

				# Pad the argument and print them
				for arg in help_args:
					padding = self.INDENTATION*4 - len(arg[0])
					if padding <= 1:
						padding = 2

					print(
						" "*(self.INDENTATION+1) + arg[0] +		# Argument and aliases
						" "*padding + arg[1]		# Description
					)

				print()
