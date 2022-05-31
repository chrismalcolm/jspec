# JSPEC
![Tests](https://github.com/chrismalcolm/jspec/actions/workflows/tests.yml/badge.svg)
![CodeCov](https://github.com/chrismalcolm/jspec/actions/workflows/codecov.yml/badge.svg)

JSPEC is a powerful yet simple and lightweight JSON validation module.

## Installation and requirements
The JSPEC module is written in pure Python and only uses standard Python libraries, so there are no dependencies aside from Python and pip3. To install run:

```bash
pip3 install jspec
```

## At a glance
The schema used in this module is written in the JSPEC language, which is an intuitive and explicit way to describe JSON. In the example below, the schema is defined in a JSPEC file (**.jspec**). It is a schema for a JSON object satisfying two conditions; a key "name" with a string value and a key "age" with an integer value. All other keys will be ignored.

*example_00.jspec*
```
{
    "name": string, 
    "age": int,
    ...
}
```

Use the JSPEC **`load`** function to create the specification object, then use the JSPEC **`check`** function to see if a given JSON adheres to the schema in *example_00.jspec*. In the code snippet below, we are validating the schema against the JSON objects **`{"name": "Chris", "age": 26, "status": "online"}`** and **`{"name": "Bob", "age": 34.5}`**.

```python
>>> import jspec
>>> 
>>> with open("example_00.jspec") as f:
>>>     spec = jspec.load(f)
>>> 
>>> jspec.check(spec, {"name": "Chris", "age": 26, "status": "online"})
True, ''
>>> jspec.check(spec, {"name": "Bob", "age": 34.5})
False, 'at $.age expecting an int not a real'
>>> 
```

The first check for **`{"name": "Chris", "age": 26, "status": "online"}`** passes because because both the "name" and "status" conditions are satisfied, and the "status" pair is ignored. The **`check`** function returns **True** with an empty string when successful.

The second check for **`{"name": "Bob", "age": 34.5}`** failed, because even though the "name" condition is satisfied, because 34.5 is not an integer, it failed the "age" condition.  The **`check`** function returns **False** with a reason for failure when unsuccessful.

## What is the JSPEC language?
The JSPEC language is a natural and intuitive extension of JSON language that is used to explicitly describe JSON. Its name JSPEC stands for **J**SON **SPEC**IFICATION. JSPEC has its own file format **.jspec** along with its own syntax highlighter extensions supported in [VS Code](https://github.com/chrismalcolm/jspec/tree/main/extensions/vscode/) and [Vim](https://github.com/chrismalcolm/jspec/tree/main/extensions/vim/). Its usage will be explored further in the [Basic Usage](#basic-usage) and [Advanced Usage](#advanced-usage) sections below. There is also a link for official documentation for all of the features of the [JSPEC language](https://github.com/chrismalcolm/jspec/tree/main/docs/language/README.md).

## Implicit vs Explicit
Most Python JSON validation/schema modules use implicit language to describe their schema. This means that they describe the structure and properties of the JSON, encoded using some paradigm. An example of an implicit schema is given below.
```python
schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "role": {
            "type": "string",
            "allowed": [
                "agent",
                "client",
                "supplier"
            ]
        },
        "value": {
            "min": 100,
            "max": 2000
        }
    },
    "required": ["id", "role", "value"],
    "additionalProperties": True,
}
```
Upon reading this, it may become fairly clear what conditions the schema is asking for. It's for an object, with an integer "id" key, a "role" key allowing only certain values, a "value" key for a number within a threshold, and any additional keys will be ignored. However, usage of an implicit JSON schema library poses the following issues:
1. Learning the paradigm in order to create a schema
2. A schema will become harder to read and understand when you introduce many nested objects and arrays, as is common in many practical use cases.

JSPEC offers solutions to each of these issues in the following ways. 
1. There is no paradigm to learn. Since JSPEC describes JSON explicitly, if you know how to write JSON, you already know how to write JSPEC! JSPEC only offers additional syntaxes above normal JSON language, to make some generalizations easier.
2. A JSPEC file can only get as nested as the JSON you are writing the schema for. It is a lot easier to write a schema for complex nested structures.

To demonstrate this further, here is the equivalent schema of the above, written in JSPEC:
```
{
    "id": int,
    "role": "agent|client|supplier",
    "value": (number > 100 & number < 2000),
    ...
}
```
This states exactly the same information as the implicit schema, but in a much more simple, explicit and elegant way.

## Basic Usage
This section will explore how to use the JSPEC language through examples of JSPEC files and Python snippets. For all of the examples in this section, it will be assumed that the example JSPEC file has been loaded as a JSPEC instance **`spec`**. For documentation on the functions of this module. follow the link [here](https://github.com/chrismalcolm/jspec/tree/main/docs/functions/README.md).

### Example 1
The example below is a JSPEC schema, specifying that the JSON be an object with a key "name" with a string value, a key "age" with an integer value, and with no other keys allowed.

*example_01.jspec*
```
{
    "name": string,
    "age": int
}
```

Using this JSPEC file to validate **`{"name": "Alice", "age": 32}`** and **`{"name": "Connor", "age": 47, "online": True}`** produces the following result.

```python
>>> jspec.check(spec, {"name": "Alice", "age": 32})
True, ''
>>> jspec.check(spec, {"name": "Connor", "age": 47, "online": True})
False, 'unexpected key "online" at position $'
>>> 
```

The latter JSON object failed the validation check; since it contains an additional field "online", which *example_01.jspec* did not allow.

The **string** and **int** used in the JSPEC file are called **placeholders**. They allow the presence of any value of their named type. There are 7 placeholders in total, **object**, **array**, **string**, **int**, **real**, **bool** and **number**, where using **number** will allow any int or real.

### Example 2
To allow for additional fields, we can add an **object ellipsis** to our original example. An object ellipsis (...) will ignore all additional fields. Only one object ellipsis should be used per object.

*example_02.jspec*
```
{
    "name": string,
    "age": int,
    ...
}
```

Now when we use this JSPEC file to validate **`{"name": "Alice", "age": 32}`** and **`{"name": "Connor", "age": 47, "online": True}`**, it produces the following result.

```python
>>> jspec.check(spec, {"name": "Alice", "age": 32})
True, ''
>>> jspec.check(spec, {"name": "Connor", "age": 47, "online": True})
True, ''
>>> 
```

As we can see now, both JSON objects pass, as the **object ellipsis** has allowed for the "online" key to be in the object, and all other conditions are satisfied.

### Example 3
An **array ellipsis** can be used to ignore any number of JSON elements inside an array. You can use multiple array ellipses in an array, so long as they are not consecutive. The example below is a JSPEC schema for an array, beginning with a 1 and ending with a 5,

*example_03.jspec*
```
[1, ... ,5]
```

We can now use this JSPEC file to validate the three examples below.
```python
>>> jspec.check(spec, [1, 2, 3, 4, 5])
True, ''
>>> jspec.check(spec, [1, 5])
True, ''
>>> jspec.check(spec, [1, 3, 5, 7, 9])
False, 'unexpected element 7 in array at position $'
>>> 
```

The first example passes, as the array beings with 1, ends with 5, and 2, 3 and 4 are ignored. The second example passes, as the array beings with 1 and ends with 5, and there are no elements to ignore. The third example fails; since the array does not end in a 5.

### Example 4
The JSPEC language also supports **regex** for string values. The example below is a schema to match a key "name" with a value "Mike" and a key "email" with the regex pattern for an email address. 

*example_04.jspec*
```
{
    "name": "Mike",
    "email": "([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})"
}
```

To see this JSPEC validation in action, here are a couple of examples.
```python
>>> jspec.check(spec, {"name": "Mike" "email": "not_an_email_address"})
False, 'did not satisfy regex at position $.email'
>>> jspec.check(spec, {"name": "Mike" "email": "mike@example.com"})
True, ''
>>> 
```

The first example failed since the "email" value "not_an_email_address" does not satisfy the regex for an email address, as specified in *example_04.jspec*. The second example passes as the "email" and "name" conditions are both satisfied.

### Example 5
If there is an element that should not appear, a **negation** operator can be used. This is done by placing an exclamation mark before the element, to show that it should not appear there. 

It is also possible to allow for any element to appear, using the **wildcard** star character. The example below demonstrates a use for both of these.   

*example_05.jspec*
```
{
    "id": !null,
    "metadata": *
    "fraction": {
        "numerator": int,
        "denominator": (int & !0)
    },
}
```
The negation used for "id" means that its value cannot be null. 

The wildcard used for "metadata" means that its value can be anything.

The example above also introduces a **conditional** statement, i.e. **`(int & !0)`**. A conditional is a set of conditions split by the logical operators AND **&**; OR **|**; XOR **^**. In the example above, the denominator must be an int AND must be not equal to 0.

To use *example_05.jspec* to validate a few JSON examples:
```python
>>> jspec.check(spec, {"id": "abc", "fraction": {"numerator": -5, "denominator": 4}, "metadata": "data"})
True, ''
>>> jspec.check(spec, {"id": 123, "fraction": {"numerator": 12, "denominator": 0}, "metadata": [1, 2, 3]})
False, 'failed to match negation at $.fraction.denominator, expected !0'
>>> 
```

The first example passed as the denominator is non-zero and satisfied all the other conditions. The second example failed; since even though it passes all the other conditions, the denominator equals zero. Notice that the value for "metadata" could have been any value of any type, since the wildcard character can accept anything.

### Example 6
The numerical placeholder types (i.e. **int**, **real** and **number**) can also use **inequalities**. Combining this with conditional statements means that you can provide ranges for certain values.

*example_06.jspec*
```
{
    "route_id": int >= 0,
    "distance": number < 100
    "deliverables": (int >= 0 & int <= 2000),
    "height": ((real > 3 & real < 50) | (real > 650))
}
```
Breaking down the example schema above; "route_id" needs to be an int bigger than or equal to 0; "distance" needs to be an integer or real less than 100; "deliverables" needs to be an integer between 0 and 2000 inclusive; "height" needs to either be a real between 3 and 50, or a real larger than 650.

```python
>>> jspec.check(spec, {"route_id": 45108, "distance": 130.4, "deliverables": 1800, "height": 289.5})
False, 'conditional not satisfied at $.height'
>>> jspec.check(spec, {"route_id": 702, "distance": 7.8, "deliverables": 2021, "height": 13.4})
False, 'conditional not satisfied at $.height'
>>> jspec.check(spec, {"route_id": 3.3, "distance": 88.9, "deliverables": 300, "height": 750})
False, 'expecting an int at $.route_id'
>>> jspec.check(spec, {"route_id": 15, "distance": 22.5, "deliverables": 1400, "height": 49.5})
True, ''
>>> 
```

All the examples that failed above were due to being outside of the required ranges for some of their values, or incorrect types.

## Advanced Usage

### Example 7
An **array capture** can be used to match multiple elements in an array. The syntax for an array capture is the same as a conditional, but it is also followed by a count or range. 

A count is written as **xn** where n can be either an integer or ?. If it is an integer n, the array capture will expect n elements satisfying the criteria in the array capture. If it is a "?", the array will accept any number of elements satisfying the criteria in the array capture.

A range can be written in 3 different ways. As **xn-m** where n and m are integers n < m, means the array capture will expect n to m elements satisfying the criteria in the array capture. As **xn-?** where n is an integer, means the array capture will expect at least n elements to satisfy the criteria in the array capture. As x?-n where n is an integer, means the array capture will expect at most n elements to satisfy the criteria in the array capture.

The example below gives a field for each of these scenarios.

*example_07.jspec*
```
{
    "five_positive_ints": [(int > 0)x5],
    "any_number_of_strings": [(string)x?],
    "range_of_bools": [(bool)x2-4],
    "string_or_ints": [(string | int)x1-?],
    "say_one": [("one" | "ONE" | 1 | 1.0)x?-3] 
}
```

An example of a good match for validation.
```python
>>> ex1 = {
>>>     "five_positive_ints": [1, 2, 3, 4, 5],
>>>     "any_number_of_strings": ["first", "second"],
>>>     "range_of_bools": [True, False, True],
>>>     "string_or_ints": ["a", 1, "b", 2, 3, "x"],
>>>     "say_one": ["ONE", 1] 
>>> }
>>> jspec.check(spec, ex1)
True, ''
>>> 
```

### Example 8
An **object capture** works exactly the same way as an array capture, except the rule applies to the key-value pair.

*example_08.jspec*
```
{
    ("data_\d+": int)x5
}
```

The schema above is requiring an object with exactly 5 key-value pairs, with the keys satisfying the regex "\w+_\d+" and values being integers. Note that for object captures, the keys have to be a string.

An example of a good match for validation.
```python
>>> ex2 = {
>>>     "data_2": 3,
>>>     "data_5": 1,
>>>     "data_8": 4,
>>>     "data_1": 4,
>>>     "data_9": 7,
>>> }
>>> jspec.check(spec, ex2)
True, ''
>>> 
```

### Example 9
A macro is a variable name that can be exported as a Python native JSON constant during the matching process. These variables are environment variables. A JSON element will match with a JSPEC macro, provided that it equals the exported Python native JSON constant. They are expressed as the environment variable name, enclosed in angled parentheses.

*example_09.jspec*
```
{
    "test_object": <TEST_OBJECT>,
    "test_array": <TEST_ARRAY>,
    "test_string": <TEST_STRING>
}
```

To create an example, we need to set the environment variables in the schema.
```python
>>> os.environ["TEST_OBJECT"] = '{"hello": "world"}'
>>> os.environ["TEST_ARRAY"] = '["hello", "world", 123]'
>>> os.environ["TEST_STRING"] = '"Hello World!"'
>>> jspec.check(spec, {"test_object": {"hello": "world"}, "test_array": ["hello", "world", 123], "test_string": "Hello World!"})
>>> True, ''
>>> 
```

### Example 10
Single line and multiline **comments** are also supported in the JSPEC language. Single line comments are written using **//** and extend to the end of the line. Multiline comments begin with **/\*** and end with **\*/**. They can be placed in any whitespace. Both comment types are demonstrated below.

```
{
    // Single line comments start with a double forward slash
    // They can be placed at the end of a line
    "key": "value", // even after other JSPEC entities like this
    "other": [1, ... ,5],
    /* Multiline comments start with a forward slash and star
    and are terminated by a star and forward slash.*/
    "red": "car",
    /*
     * Comments can be place anywhere where there is whitespace
     */
    "versions": [1, 2, /*like here*/ 3, 4 /*and here*/, 5]
}
```
## Contributing
I am open to any suggestions on how this project can be improved. The process for contributing would be creating a PR and having it reviewed and merged by @chrismalcolm. Please add your name and email to the `CONTRIBUTORS.txt` file when contributing.

## Unit testing
The aim of this project is for code to be fully unit testable with 100% coverage for the main modules **scanner**, **entity** and **matcher**. The command-line helpers **parse** and **check** are also included in the unit tests, but there is no requirement for these to be included in the coverage report. The `coverage` module is used when running unit tests, to get a report on the coverage of the tests. If you do not have coverage installed, run `pip install coverage` and a local dependency.

```bash
# Run the unit test suite
coverage run --source=jspec -m unittest test/test.py

# Get the coverage report
coverage report -m --omit=jspec/parse.py,jspec/check.py
```