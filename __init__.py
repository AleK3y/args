import sys
from copy import deepcopy

class Arguments:

	##
	# Attributes
	#

	INDENTATION = 6
	MAX_USAGE_PARAMETERS = 4

	info = None
	args = {
		"positional": [],
		"parameters": {},
		"options": []
	}

	##
	# Exceptions
	#

	class ParseException(Exception):
		pass
	class WrongInfoFormat(ParseException):
		pass
	class MissingRequiredArgument(ParseException):
		pass
	class WrongArgumentsPlacement(ParseException):
		pass
	class WrongArgumentsNumber(ParseException):
		pass

	##
	# Methods
	#

	def __init__(self, info):
		if "arguments" not in info:
			raise WrongInfoFormat()

		self.info = deepcopy(info)		# Allow for modifications
		self.info_args = self.info["arguments"]

		# Add missing sections
		for required_arg_type, container in self.args.items():
			if required_arg_type not in self.info_args:
				self.info_args[required_arg_type] = container.copy()

		# Add missing names on parameters
		for value in self.info_args["parameters"].values():
			if "name" not in value:
				value["name"] = ""

	def get_args(self):
		return self.args

	def get_argv(self):
		return sys.argv

	def get_info(self):
		return self.info

	def __get_valid_aliases(self, args_definition):
		valid_aliases = list(args_definition.keys())
		for value in args_definition.values():
			if "aliases" in value:
				valid_aliases += value["aliases"]

		return valid_aliases

	def __get_unaliased_argument(self, alias, args_definition):
		unaliased_arg = None
		for key, value in args_definition.items():
			if "aliases" in value and alias in value["aliases"]:
				unaliased_arg = key
				break

		return unaliased_arg if unaliased_arg else alias

	def parse(self):

		## Parse every argument ##

		parameters = self.info_args["parameters"]
		options = self.info_args["options"]
		i = 1
		while i < len(sys.argv):
			arg = sys.argv[i]

			# Parameters
			if arg in self.__get_valid_aliases(parameters):
				if i+1 >= len(sys.argv):
					raise self.WrongArgumentsPlacement(arg)

				key = self.__get_unaliased_argument(arg, parameters)
				if key not in self.args["parameters"]:
					self.args["parameters"][key] = []

				self.args["parameters"][key].append(sys.argv[i+1])		# Add argument to the list of this parameter
				i += 1

			# Options
			elif arg in self.__get_valid_aliases(options):
				self.args["options"].append(self.__get_unaliased_argument(arg, options))

			# Positional parameters
			else:
				self.args["positional"].append(arg)

			i += 1

		## Check for missing arguments ##

		if len(self.args["positional"]) != len(self.info_args["positional"].keys()):
			raise self.WrongArgumentsNumber()

		for key, value in parameters.items():
			if (
				key not in self.args["parameters"] and
				"required" in value and value["required"]
			):
				raise self.MissingRequiredArgument(key)

	def usage(self, output_stream=sys.stderr):

		## Usage ##

		if "usage" not in self.info:
			usage = sys.argv[0]

			# Add options to usage
			if len(self.info_args["options"].keys()) > 0:
				usage += " [OPTION]"

			required_params = []
			for key, value in self.info_args["parameters"].items():
				if "required" in value and value["required"]:
					required_params.append([key, value["name"]])

			# Add required parameters if they're not too many
			if len(required_params) <= self.MAX_USAGE_PARAMETERS:
				for param in required_params:
					usage += " " + param[0] + " " + param[1].upper()

			# Also add positional parameters
			for key in self.info_args["positional"].keys():
				usage += " " + key.upper()

			self.info["usage"] = usage

		output_stream.write("Usage: " + self.info["usage"] + "\n")
		if "description" in self.info:
			output_stream.write(
				" "*self.INDENTATION +
				self.info["description"] + "\n"
			)
		output_stream.write("\n")

		## Arguments help ##

		for arg_type in self.args.keys():
			args_definition = self.info_args[arg_type]

			# Skip sections with no arguments
			if len(args_definition.keys()) == 0:
				continue

			output_stream.write(" "*self.INDENTATION + arg_type.title() + ":\n")

			help_texts = []
			for key, value in args_definition.items():
				name = key

				if "aliases" in value:
					name = ", ".join([name] + value["aliases"])

				if "name" in value:
					name += " " + value["name"]

				help_texts.append([
					name,
					value["description"] if "description" in value else ""
				])

			# Pad the argument and print them
			for line in help_texts:
				padding = self.INDENTATION*5 - len(line[0])

				# Push the description if the name is too long
				if padding <= 1:
					padding = 2

				output_stream.write(
					" "*(self.INDENTATION+1) + line[0] +
					" "*padding + line[1] + "\n"
				)

			output_stream.write("\n")
