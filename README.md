# Jspec
Jspec is a tool that can be used to check the regex and structure of JSON. This can be done by composing a .jspec file, generating a JSpec object and using it to return whether the .json file adheres to the regex and structure defined in the .jspec file.

## What is a .jspec file
A .jspec file is a document which outlines the desired regex and structure for .json files. It's format adheres to normal JSON rules, with the addition of regex, ellipsis subsitution and ellipsis templeting. Below is a description of all the addition rules which apply to JSPEC and an example of a .jspec file and matching .json file.

### Regex
---
In order for a JSPEC to match a JSON, the JSON has to satify all the regex conditions in the JSPEC. Regex can be used to match with elements, keys and values. They cannot be used to match brackets for arrays or objects.

| JSPEC snippet | Match example |
|-|-|
| `["\w", "\d", "b", 2]` | `["a", 1, "b", 2]` |
| `{"\w+": {"id-\d{4}": "green"}}` | `{"word": {"id-1256": "green"}}` |
| `{"timestamp": ["\d+", "\d+], "e-[A-Za-z]{6}": "\d"}` | `{"timestamp": [1200, 3600]}, "e-ArHqzL": 4}` |

### Ellipsis subsitution
---
Using an ellipsis in a JSPEC array will instruct the JSPEC interepter to ignore all elements, arrays or objects in that place. If necessary, commas need to be placed before or after the ellipsis. Similarly, using a ellipsis in a JSPEC object will instruct the JSPEC interepter to ignore all additional key-value pairs in that object. If necessary, commas need to be placed before or after the ellipsis.

| JSPEC snippet | Match example |
|-|-|
| `[1, 2, 3, ... ]` | `[1, 2, 3, 4, 5]` |
| `[ ... ,"d" ,"e"]` | `["a", "b", "c", "d", "e"]` |
| `[6, ... , 9, 10]` | `[6, 7, 8, 9, 10]` |
| `["a", ... ,"c", "d", ... "g"]` | `["a", "b", "c", "d", "e", "f", "g"]`|
| `[ ... ]` | `[1, 2, 3, "x", "y", "z"]` |
| `["\d+", ... ,"\w+", ... , [1, 2, "\d"]]` | `[23, 8, [4, 5], "red", "green", "blue", [1, 2, 5]]` |
| `{"a": 1, "b": 2, "c": 3, ... }` | `{"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}` |
| `{ ...,  "y": 25, "z": 26}` | `{"w": 23, "x": 24, "y": 25, "z": 26}` |
| `{ "a": 1,  "b": 2, ... ,"z": 26}` | `{"a": 1, "b": 2, "c": 3, "x": 24, "y": 25, "z": 26}` |
| `{ ... }` | `{"a": 1, "z": 26}` |
| `{"\w+": ["\d{2}", ... , 14], "other": "key-[0-9a-f]{4}", ...}` | `{"word": [12, 13, 14], "other": "key-0af4, "extra": {}}` |

### Ellipsis Templating
---
Using a pair of ellipsis to surround an element in a JSPEC array will interepter to only except elements which adhere to the regex in the array. Similarly, using a pair of ellipsis to surround a key-value pair will instruct the interepter to only accept key-value pairs which adhere to the regex in the object.

| Syntax | Match example |
|-|-|
| `[ ... 1 ... ]`  | `[1, 1, 1, 1]` |
| `[ ... "\w+" ... ]`  | `["red", "brick", "wall"]` |
| `{ ... "\w+": "\d+" ... }` | `{"a": 1, "b": 2, "y": 25, "z": 26}` |
| `{ ... "\d": "okay" ... }` | `{"1": "okay", "2": "okay", "3": "okay"}` |
| `{ ... "\w+": [ ... "\d" ... ] ... }` | `{"red": [1,2,3], "blue": [4]}`|

### Example
The example.jspec will match with example.json.

example.jspec
```
{
    ... ,
    "timestamps": [ ... "\d+" ... ],
    "query": {
        "type": "sql",
        "vals": [ ... "[a-f0-9]{8}" ... ]
    },
    "id_pairs": {
        ... "\w+": "id-\d{4,8}" ...
    },
    "list_of_lists": [
        [ ... ],
        [ ... ]
    ],
    "alphabet": ["a", "b", ... , "m", ... , "y", "z"]
    , ...
}
```

example.json
```json
{
    "extra_field_1": "blah",
    "timestamps": [1003, 1006, 2005, 4005],
    "query": {
        "type": "sql",
        "vals": [
            "af05eb41",
            "b048cda2",
            "d094eea7"
        ]
    },
    "id_pairs": {
        "red": 8374334,
        "green": 3424,
        "blue": 10923,
        "yellow": 772266
    },
    "list_of_lists": [
        [1, 2, 3],
        ["a", "b", "c"]
    ],
    "alphabet": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
}
```

## Usage
Once you have created a .jspec file, you can check to see if it matches against JSON. To load the JSPEC, uses the `jspec.load` or `jspec.loads` methods for loading file objects or JSPEC string respectively. These will return an instance of the `JSpec` class if the JSPEC is valid, else a `JSpecLoadError` will be raised. 

The `JSpec` class has a `match` method which checks the JSON arguemnt against the JSPEC. The JSON argument can be a file object, JSON string or Python native object. Example usage is given below.

```python
import jspec

with open("example.jspec") as f:
    j = jspec.load(f)

with open("example.json") as f:
    print(j.match(f))
```
Output:
```bash
True
```