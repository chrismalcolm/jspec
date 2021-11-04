# Jspec
Jspec is a tool that can be used to check the regex and structure of JSON. This can be done by composing a .jspec file, generating a JSpec object and using it to return whether the .json file adheres to the regex and structure defined in the .jspec file.

## What is a .jspec file
A .jspec file is a document which outlines the desired regex and structure for .json files. It's format adheres to normal JSON rules, with the addition of regex, ellipsis substitution and ellipsis templating. Below is a description of all the addition rules which apply to JSPEC and an example of a .jspec file and matching .json file.

### Regex
---
In order for a JSPEC to match a JSON, the JSON has to satify all the regex conditions in the JSPEC. Regex can be used to match with elements, keys and values. They cannot be used to match brackets for arrays or objects.

| JSPEC snippet | Match example |
|-|-|
| `["\w", "\d", "b", 2]` | `["a", 1, "b", 2]` |
| `{"\w+": {"id-\d{4}": "green"}}` | `{"word": {"id-1256": "green"}}` |
| `{"timestamp": ["\d+", "\d+"], "e-[A-Za-z]{6}": "\d"}` | `{"timestamp": [1200, 3600], "e-ArHqzL": 4}` |

### Ellipsis substitution
---
Using an ellipsis in a JSPEC array will instruct the JSPEC interpreter to ignore all elements, arrays or objects in that place. If necessary, commas need to be placed before or after the ellipsis. Similarly, using a ellipsis in a JSPEC object will instruct the JSPEC interpreter to ignore all additional key-value pairs in that object. If necessary, commas need to be placed before or after the ellipsis.

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
| `{"same_\w+": ["\d{2}", ... , 14], "other": "key-[0-9a-f]{4}", ...}` | `{"same_word": [12, 13, 14], "other": "key-0af4", "extra": {}}` |

*NOTE*
*Be careful not to use ambiguous regex when matching arrays or objet fields. E.g. {"\w+": [], "other": 1} is ambiguous since other can match \w+. This is to be avoided as results would not be consistent.*

### Ellipsis Templating
---
Using a pair of ellipsis to surround an element in a JSPEC array will interpreter to only except elements which adhere to the regex in the array. Similarly, using a pair of ellipsis to surround a key-value pair will instruct the interpreter to only accept key-value pairs which adhere to the regex in the object.

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

The `JSpec` class has a `match` method which checks the JSON argument against the JSPEC. The JSON argument can be a file object, JSON string or Python native object. The function will return `Result` which has a `result()` and `message()` method. The `result()` method will return whether the JSON matched the JSON. The `message()` will return the message for why the JSON match failed if it did. Example usage is given below.

### Example 1

```python
import jspec

with open("example.jspec") as f:
    spec = jspec.load(f)

with open("example.json") as f:
    r = spec.match(f)
    print(r.result())
```
Output:
```bash
True
```

### Example 2

```python
import jspec

snippet = '{"same_\w+": ["\d{2}", ... , 14], "other": "key-[0-9a-f]{4}", ...}'
good = {"same_word": [12, 13, 14], "other": "key-0af4", "extra": {}}
bad = {"same_word": [12, 13, 14], "extra": {}}

spec = jspec.loads(snippet)

r1 = spec.match(good)
r2 = spec.match(bad)

print("r1 result:", r1.result(), "r1 message:", r1.message())
print("r2 result:", r2.result(), "r2 message:", r2.message())
```
Output:
```bash
r1 result: True r1 message: None
r2 result: False r2 message: Cannot match key regex at position '$'. Want other, same_\w+. Got same_word, extra
```

# new stuff
python3 -m unittest

to run test

add tests

add comments

| Element | JSON Native | JSPEC Native | Excepted Values |
|---------|--------------|-------------|-------------|
| Object | dict | JSPECObject | A set of key-value pairs, enclosed within curly braces |
| String | str | JSPEString | Any sequence of characters or a regex pattern, enclosed in double quotes |