# JSPEC
![Tests](https://github.com/chrismalcolm/jspec/actions/workflows/tests.yml/badge.svg)
![CodeCov](https://github.com/chrismalcolm/jspec/actions/workflows/codecov.yml/badge.svg)

A JSPEC (**J**son **SPEC**ification) is a powerful Programming Language tool that can used to check the elements and structure of a JSON document. JSPEC documents are written using the **JSPEC Language** which uses the same syntax as JSON, but with its own file extension `.jspec` and some added features to the syntax. For example:

![](https://github.com/chrismalcolm/jspec/blob/main/images/1_jspec.png)

The example above gives a small insight into some of the features of JSPEC, such as regex, type placeholders, ellipses, comments and conditional statements. Full documentation for all of these features are given [here](#jspec-language).

## Installation and requirements
The JSPEC module is written in pure Python and only uses standard Python libraries, so there are no dependencies aside from Python and pip3. To install run:

```bash
pip3 install jspec
```

## What can this JSPEC module used for?
This module provides interfaces for parsing JSPEC documents and checking JSPEC against JSON. A check involves a JSPEC document and a JSON document, and if the JSPEC can be used to describe the JSON, it is said to be a "good match". Otherwise, it is said to be a "bad match" and a reason as to why will be provided. For example:

example.jspec

![](https://github.com/chrismalcolm/jspec/blob/main/images/2_jspec.png)

good_match.json
```json
[1, 2, 3, 4]
```

bad_match.json
```json
[1, 2, 3, 4, 5]
```

The JSPEC document `example.jspec` above describes an array, beginning with a 1 and ending with a 4, ignoring anything in between. The JSON document `good_match.json` fits this description, and would therefore be called a good match. In contrast, the `bad_match.json` does not fit this description, as the array does not end in a 4, and would be called a bad match.

## JSPEC Language

**Fundamental JSPEC terminology**
* [term](#jspec-term)
* [capture](#jspec-capture)

**Terminology shared by both JSON and JSPEC**
* [object](#object)
* [array](#array)
* [string](#string)
* [int](#int)
* [real](#real)
* [boolean](#boolean)
* [null](#null)

**Terminology unique to JSPEC**
* [wildcard](#wildcard)
* [negation](#negation)
* [macro](#macro)
* [conditional](#conditional)
* [placeholder](#placeholder)
* [object capture](#object-capture)
* [array capture](#array-capture)
* [object ellipsis](#object-ellipsis)
* [array ellipsis](#array-ellipsis)
* [comments](#comments)

### JSPEC Term
A JSPEC term can match with a single JSON element. The traditional JSON data types are all supported, alongside other JSPEC terms.

### JSPEC Capture
A JSPEC capture can match with a group of JSON elements.
Captures can only appear in objects or arrays.

### Object
A JSPEC object is a set of JSPEC object pairs and JSPEC object captures. A JSON object will match with a JSPEC object, provided it can match all the JSPEC object pairs and satisfy all JSPEC object captures. They are expressed in the same way objects are in JSON.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `{"red": "blue"}` | `{"red": "blue"}` | Good Match | Equal object paris |
| `{"red": "blue", "green": "yellow"}` | `{"green": "yellow", "red": "blue"}` | Good Match | Equal object paris |
| `{"red": "blue"}` | `{"blue": "red"}` | Bad Match | Object pairs not equal |

### Array
A JSPEC array is a list of JSPEC terms and JSPEC array captures. A JSON array will match an with a JSPEC array, provided it can match all the JSPEC terms and satisfy all JSPEC array captures. They are expressed in the same way arrays are in JSON.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `[1,2,3,4]` | `[1,2,3,4]` | Good Match | Elements at correct indices |
| `[1,2,3,4]` | `[4,3,2,1]` | Bad Match | Elements at incorrect indices |
| `[1,2,3,4]` | `[1,1,1,1]` | Bad Match | Elements do not match |
| `[1,2,3,4]` | `[1,2,3]` | Bad Match | Length of elements do not match |

### String
A JSPEC string is a regex pattern string. A JSON string will a JSPEC string, provided it satisfies the regex pattern string. They are expressed in the same way strings are in JSON.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `"cat"` | `"cat"` | Good Match | Strings are equal |
| `<\w+>` | `<word>` | Good Match | Satisfies the regex |
| `<\w+>` | `<1234>` | Bad Match | Does not satisfy the regex |

### Int
A JSPEC int is an integer. A JSON int will match an with JSPEC int, provided its integer value equals the integer value of the JSPEC int. They are expressed in the same way ints are in JSON.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `123` | `123` | Good Match | Same integer value |
| `-485` | `-485` | Good Match | Same integer value |
| `10` | `100` | Bad Match | Different integer value |

### Real
A JSPEC real is a real number. A JSON real will match an with a JSPEC real, provided its real number value equals the real number value of the JSPEC real. They are expressed in the same way reals are in JSON.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `3.141` | `3.141` | Good Match | Same float value |
| `0.9999e-10` | `0.9999e-10` | Good Match | Same float value |
| `2.1e4` | `21000` | Good Match | Same float value |
| `2.1e4` | `2100` | Bad Match | Different float value |

### Boolean
A JSPEC boolean is a boolean. A JSON boolean will match an with a JSPEC boolean, provided its boolean value equals the boolean value of the JSPEC boolean. They are expressed in the same way booleans are in JSON.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `true` | `true` | Good Match | Same boolean value |
| `false` | `false` | Good Match | Same boolean value |
| `true` | `false` | Bad Match | Different boolean value |
| `false` | `true` | Bad Match | Different boolean value |

### Null
A JSPEC null is a null. A JSON null value will match with a JSPEC null. They are expressed in the same way nulls are in JSON.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `null` | `null` | Good Match | Null |
| `null` | `1` | Bad Match | Not null |

### Wildcard
A JSPEC wildcard is the JSPEC term that will match with any JSON element. They are expressed as a wildcard character ` *`.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `*` | `123` | Good Match | Matches any element |
| `*` | `[1,2,3]` | Good Match | Matches any element |
| `*` | `{"a": "b"}` | Good Match | Matches any element |

### Negation
A JSPEC negation is a negated JSPEC term. A JSON element will match with a JSPEC negation, provided it does not match with the negated JSPEC term. They are expressed as an exclamation mark followed by the negated JSPEC term.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `!4` | `3` | Good Match | 4 != 3 |
| `!4` | `{}` | Good Match | 4 != {} |
| `![]` | `[1,2,3]` | Good Match | [] != [1,2,3] |
| `![1,2]` | `"[]"` | Good Match | [1,2] != "[]" |
| `!![1,2]` | `"[1,2]"` | Good Match | [1,2] = "[1,2]" |
| `!4` | `4` | Bad Match | 4 = 4 |
| `![1,2]` | `[1,2]` | Bad Match | [1,2] = [1,2] |

### Macro
A JSPEC macro is a variable name which can be exported as a Python native JSON constant during the matching process. These variables are environment variables. A JSON element will match with a JSPEC macro, provided that it equals the exported Python native JSON constant. They are expressed as the environment variable name, enclosed in angled parentheses.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `<ENV_VARIABLE>` | `123` | Good Match | Only when the env variable `ENV_VARIABLE` equals 123 |
| `<IMPORTANT_LIST>` | `[1,2,3]` | Good Match | Only when the env variable `IMPORTANT_LIST` equals [1,2,3] |
| `<OTHER_VARIABLE>` | `123` | Bad Match | Only when the env variable `OTHER_VARIABLE` does not equal 123 |

### Conditional
A JSPEC conditional a logical statement of JSPEC terms and logical operators (`&` AND, `|` OR, `^` XOR). A JSON element will match with a JSPEC conditional, provided it satisfies the logical statement of JSPEC terms and logical operators. They are expressed as JSPEC terms in between the logical operators, enclosed in rounded parentheses.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `(1 \| 4 \| 2)` | `1` | Good Match | Satisfied the logical statement |
| `(1 \| 4 \| 2)` | `4` | Good Match | Satisfied the logical statement |
| `(!"a" & !"b")` | `"c"` | Good Match | Satisfied the logical statement |
| `(!"a\d" ^ !"\w7")` | `"c7"` | Good Match | Satisfied the logical statement |
| `(1 \| 2 \| 3)` | `4` | Bad Match | Did not satisfied the logical statement |
|`(!"a\d" ^ !"\w7")` | `"a7"` | Bad Match | Did not satisfied the logical statement |

### Placeholder
A JSPEC placeholder is a JSON datatype name, which will match any JSON element of that datatype. The possible placeholders are `object`, `array`, `string`, `int`, `real`, `bool` and `number`. The numerical placeholders can also have an inequality attached to them, to set a range of numerical values for it to match.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `object` | `{"a": 1, "b": 2}` | Good Match | Matches any object |
| `array` | `[1,2,3]` | Good Match | Matches any array|
| `string` | `"something"` | Good Match | Matches any string |
| `int` | `3` | Good Match | Matches any int |
| `real` | `-0.90e4` | Good Match | Matches any real |
| `bool` | `true` | Good Match | Matches any boolean |
| `number` | `12` | Good Match | Matches any int or real |
| `object` | `[1,2,3]` | Bad Match | Is not an object |
| `array` | `{"a": 1, "b": 2}` | Bad Match | Is not an array|
| `number` | `"12"` | Bad Match | Is not a int or real |

### Object Capture
A JSPEC object capture is a list of JSPEC object pairs and logical operators (`&` AND, `|` OR, `^` XOR) which form a logical statement. Any JSON object pairs which can be part of the capture group must satisfy the logical statement. It also has an optional minimum and maximum number of object pairs in the capture group. They are expressed as JSPEC object pairs in between the logical operators, enclosed in rounded parentheses, with an optional multiplier range. The optional range is expressed as `xn` or `xn-m` where `n` and `m` are non-negative integers or `?` and `n` <= `m`.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `{("\w": int)x2}` | `{"a": 1, "b": 2}` | Good Match | Captures "a": 1 and "b": 2 |
| `{("\w": int \| "\w": bool)x2-5}` | `{"a": 1, "b": true, "c": false}` | Good Match | Captures "a": 1, "b": true and "c": false | Captures "a": 1, "b": true and "c": false |
| `{"c": 3, ("\w": int)x?}` | `{"a": 1, "b": 2, "c": 3}` | Good Match | Captures "a": 1 and "b": 2 | Captures  |
| `{("\w": int \| "\w": bool)x?-5}` | `{"a": 1, "b": true, "c": false}` | Good Match | Captures "a": 1 and "b": true and "c": false | Captures  |
| `{("\w": int \| "\w": bool)x2-?, "d": null}` | `{"a": 1, "b": true, "c": false, "d": null}` | Good Match | Captures "a": 1 and "b": true and "c": false | Captures  |
| `{("\w": int)x1}` | `{"a": 1, "b": 2}` | Bad Match | Not enough to satisfy capture |
| `{("\w": int)x3}` | `{"a": 1, "b": 2}` | Bad Match | Not enough capacity to match JSON object pairs |
| `{("\w": int \| "\w": bool)x2-?, "d": null}` | `{"a": 1, "b": true, "c": false}` | Bad Match | Missing "d": null |

### Array Capture
A JSPEC array capture is a list of JSPEC object pairs and logical operators (`&` AND, `|` OR, `^` XOR) which form a logical statement. Any JSON object pairs which can be part of the capture group must satisfy the logical statement. It also has an optional minimum and maximum number of object pairs in the capture group. They are expressed as JSPEC terms in between the logical operators, enclosed in rounded parentheses, with an optional multiplier range. The optional range is expressed as `xn` or `xn-m` where `n` and `m` are non-negative integers or `?` and `n` <= `m`.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `[(int)x4, (string)x1-2]` | `[1,2,3,4,"a","b"]` | Good Match | First capture is satisfied by 1,2,3,4 and second capture is satisfied by "a","b" |
| `[1,2,3,(bool)x?,5,6]` | `[1,2,3,true,true,false,5,6]` | Good Match | Capture satisfied by true,true,false |
| `[(int)x3, (string)x3]` | `[1,2,3,4,"a","b"]` | Bad Match | Second capture not satisfied |
| `[1,2,3,(bool)x?,5,6]` | `[1,2,3,4,5,6]` | Bad Match | Capture not satisfied |

### Object Ellipsis
A JSPEC object ellipsis will match with any extra object pairs that have not already been matched. It is equivalent to the wildcard object capture `(string: *)x?`.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `{"a":1,"b":2, ...}` | `{"a":1,"b":2,"c":3}` | Good Match | Ellipsis matches "c":3 |
| `{"a":1,"b":2, ...}` | `{"a":1,"b":2}` | Good Match | Ellipsis matches nothing |
| `{...}` | `{"a": "b"}` | Good Match | Ellipsis matches "a": "b" |
| `{"a":1,"b":2, ...}` | `{"a":1}` | Bad Match | The JSPEC object pair "b": 2 is not matched |

### Array Ellipsis
A JSPEC array ellipsis will match with any amount of consecutive elements in an array. It is equivalent to the wildcard array capture `(*)x?`.

| JSPEC Snippet | JSON Snippet | Result | Reason | 
|-|-|-|-|
| `[1,2,3 ... 5,6]` | `[1,2,3,4,5,6]` | Good Match | Ellipsis matches with 4 |
| `[... ,"b","c",...]` | `["a","b","c","d","e"]` | Good Match | First ellipsis macthes "a", second ellipsis matches "d","e" |
| `[1,2,3 ... 4,5]` | `[1,2,3,4,5]` | Good Match | Ellipsis matches nothing |
| `[...]` | `[{}, 1, null]` | Good Match | Ellipsis matches {}, 1, null |
| `[...]` | `[]` | Good Match | Ellipsis matches nothing |
| `[1,2,3 ... 5,6]` | `[1,2,4,3,5,6]` | Bad Match | Ellipsis cannot match anything |
| `[1,...]` | `[2,1] ` | Bad Match | Ellipsis cannot match anything |

### Comments
A JSPEC comment cannot be used to match against anything in a JSON, and only purpose is to provide documentation insights for the viewer of the JSPEC document. Both single line and multiline comments are supported in the following formats:

![](https://github.com/chrismalcolm/jspec/blob/main/images/3_jspec.png)

## Basic Python Usage
A specification can be defined using a JSPEC file or a string. Using the **jspec.load** or **jspec.loads** methods respectively, this can produce a **jspec.JSPEC** instance. This instance can also be converted back to a JSPEC file or string, using the **jspec.dump** or **jspec.dumps** methods respectively. To check a JSON against a JSPEC, use the 
**jspec.check** to check using a **jspec.JSPEC** instance, or use the **jspec.checks** to check using a string. Any JSON used for these two methods must be in a Python native format, which can be achieved using the **json.loads** method.

JSPEC file

![](https://github.com/chrismalcolm/jspec/blob/main/images/4_jspec.png)

This example describes a JSON object with an "id" field set as the environment variable MY_ID, the "timestamp" field as a number, and "data" as a list of objects, each with a "longitude" and "latitude" keys and real values.

Source
```python
import os
import jspec

os.environ["MY_ID"] = '1'
with open("./test/assets/test.jspec", "r") as f:
    spec = jspec.load(f)
element_1 = {
    "id": 1,
    "timestamp": 1530.5,
    "data": [
        {
            "longitude": 10.2,
            "latitude": 41.3,
        },
        {
            "longitude": 33.3,
            "latitude": 76.2,
        },
        {
            "longitude": 9.5,
            "latitude": 12.1,
        }
    ],
    "other": "data"
}

element_2 = {
    "id": 1,
    "bad": "fields"
}

result_1, reason_1 = jspec.check(spec, element_1)
print("1:", result_1, reason_1)

result_2, reason_2 = jspec.check(spec, element_1)
print("2:",result_2, reason_2)
```

Output
```bash
1: True, ''
2: False, 'At location $ - exhausted JSON object, failed to match the following JSPEC pairs: ["data": [({"latitude": real, "longitude": real})x?], "timestamp": number, ...]'
```

## Visual Studio Code Extension
This repository also provided a Visual Studio Code extension which is available to be downloaded from the marketplace, under the name "JSPEC". It provides syntax highlighting for the JSPEC Language.

## Contributing
Process for contributing would be creating a PR and having it reviewed and merge by @chrismalcolm. Please and your name and email to the `CONTRIBUTORS.txt` file when contributing.

### Deploying an update to the extension
The sub repository for extension source code here https://github.com/chrismalcolm/jspec/tree/main/extensions/vscode

Link to the marketplace publisher here: https://marketplace.visualstudio.com/manage/publishers/ChrisMalcolm

To deploy a new version of the Visual Studio extension, make sure `Node.js` is installed and run the following to install vsce:

```bash
npm install -g vsce
```

To create a new `.vslx` file, navigate to sub repository for the extension and run:

```bash
vsce package
```

This will create the package. This can just be drag and dropped using the UI of the marketplace publisher, to deploy a new version of the extension.

### Unit testing
The aim for this project is for code to be fully unit testable with 100% coverage for the main modules. The `coverage` module is used when running unit tests, to get a report on the coverage of the tests. If you do not have coverage installed, run `pip install coverage` and a local dependency.

```bash
# Run the unit test suite
coverage run --source=jspec -m unittest test/test.py

# Get the coverage report
coverage report -m --omit=jspec/parse.py,jspec/check.py
```