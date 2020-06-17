# args
Parse the arguments from `sys.argv` or print the usage.

## Class parameters
The only parameter of the class is `info`.

One simple example would be from my [4chan-d](https://github.com/AleK3y/4chan-d) repository:
```python
{
	"usage": "4chan-d.py [OPTIONS]",		# Executable syntax
	"description": "Download threads from 4chan.",		# New lines with "\n" are automatically formatted
	
	# Options with parameters
	"parameters": {
		"-u": {
			"required": True,		# Tell whether the option is obligatory or not
			"description": "4chan thread url",
		},
		"-o": {
			"required": False,
			"description": "output parent directory",		# " (optional)" will be appended if it isn't required
		},
	},

	# Single options
	"options": {
		"-f": {
			"required": False,
			"description": "if enabled the file names will be the uploaded ones",
		},
	}
}
```

## Example
Following the information dictionary structure you can initialize the class like this:
```python
import args

# infos = ...

parser = args.Arguments(infos)
try:
	parser.update_args()
except args.Arguments.MissingMandatoryArgument:
	parser.usage()		# Print the usage if one or more are missing
	exit()
```

## Access the arguments
You can either access the dictionary from `parser.args` or `parser.get_args()`. \
An example how its structure would be:
```python
{
	"-u": "https://boards.4channel.org/g/thread/51971506",		# For parameters
	"-f": None,		# For options, the value (None) should be ignored
}
```

## Missing required parameters
If a required parameter is missing, the `update` function will throw a `MissingMandatoryArgument` exception.
