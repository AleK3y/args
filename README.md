# args
Parse the arguments from `sys.argv` or print the usage.

## Class parameters
The only parameter of the class is `info`.

One simple example would be this one:
```python
{
	#"usage": "",		# A default usage will be computed if omitted
	"description": "Calculate the power.",
	"arguments": {

		# Positional arguments are always required
		"positional": {
			"BASE": {
				"description": ""
			},
			"EXPONENT": {
				"description": ""
			}
		},

		"parameters": {
			"-o": {
				"aliases": ["--output"],
				"name": "FILE",
				"description": "set the file to write to",
				"required": True,
			}
		},

		# Options are never required
		"options": {
			"-v": {
				"aliases": ["--verbose"],
				"description": "report more info about the operations",
			}
		}
	}
}
```

## Exceptions
After initializing the class you'll have to run the `update` function. The function might throw these exceptions:
- `MissingRequiredArgument`: When a required or positional parameter is missing
- `WrongArgumentsPlacement`
- `TooFewArguments`: When the amount of positional parameters is lower than the expected

## Example
Following the information dictionary structure you can initialize the class like this:
```python
from args import Arguments

# infos = ...

parser = Arguments(infos)
try:
	parser.update()
except (Arguments.MissingRequiredArgument, Arguments.WrongArgumentsPlacement, Arguments.TooFewArguments):
	parser.usage()
	exit()
```

## Access the arguments
You can either access the dictionary from `parser.args` or `parser.get_args()`. \
An example of how it would be:
```python
{
	"positional": ["2", "4"],
	"parameters": [{"-o": "file"}],
	"options": []
}
```
