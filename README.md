# args
Parse the arguments from `sys.argv` or print the usage.

## Class parameters
The only required parameter of the class is `info`, and it contains all the details about the arguments to parse.

One simple example would be this one:
```python
{
	#"usage": "",		# A default usage will be automatically computed if omitted
	"description": "Calculate the power.",
	"arguments": {

		# Positional arguments are considered always required
		"positional": {
			"BASE": {
				"description": "The part that is multiplied by itself."
			},
			"EXPONENT": {}
		},

		# Can be both required or not
		"parameters": {
			"-r": {
				"aliases": ["--round"],
				"name": "PLACE",
				"description": "set the decimal place to round to",
				"required": True,
			},
			"-o": {
				"aliases": ["--output", "--output-file"],
				"name": "FILE",
				"description": "set the output file",
				"required": False,
			}
		},

		# Options are never required
		"options": {
			"-v": {
				"aliases": ["--verbose"],
				"description": "report more info about the calculations",
			},
			"-t": {
				"description": "run the calculations in multiple threads"
			}
		}
	}
}
```

## Exceptions
After initializing the class you'll have to run the `parse` function and it might throw these exceptions:
- `ParseException`: Includes all the following exceptions
- `WrongInfoFormat`
- `MissingRequiredArgument`: When a required or positional parameter is missing
- `WrongArgumentsPlacement`
- `WrongArgumentsNumber`: When the amount of positional parameters is not the expected

## Example
With the info dictionary structure you can initialize the class like this:
```python
from args import Arguments

# infos = ...

parser = Arguments(infos)
try:
	parser.parse()
except Arguments.ParseException:
	parser.usage()
	exit()
```

## Access the arguments
You can either access the dictionary from `parser.args` or `parser.get_args()`. \
An example of what it would return:
```python
{
	"positional": ["2", "4"],
	"parameters": [{"-r": ["0"], "-o": ["file1", "file2"]}],
	"options": ["-t"]
}
```
