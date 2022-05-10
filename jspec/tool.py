"""Command-line tool to validate and pretty-print JSON
Usage::
    $ python -m jspec.scanner <.jspec file or string>
? pretty print?
    $ python -m jspec.matcher .jspec .json

    returns true (nothing) or false with error

    $ echo '{"json":"obj"}' | python -m json.tool
    {
        "json": "obj"
    }
    $ echo '{ 1.2:3.4}' | python -m json.tool
    Expecting property name enclosed in double quotes: line 1 column 3 (char 2)
"""
import jspec

def main():
    import argparse
    import sys
    import json
    prog = 'python -m jspec.tool'
    description = ('A simple command line interface for the jspec module to validate JSPEC documents.')
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument('infile', nargs='?',
                        type=argparse.FileType(encoding="utf-8"),
                        help='a JSON file to be validated or pretty-printed',
                        default=sys.stdin)
    
    options = parser.parse_args()


    dump_args = {}
    with options.infile as infile:
        try:
            infile = '{"HE":[] /* as */ //other\n//other\n, "SHE": <MACRO_1>, /*gtg*/ "gig": [1,2,(3 | 4 | {})]}'
            document = """
{//Comment 1
    "A field for object": {
        "hello": "world"
    },
    "B field for array": [
        1,
        3,
        5
    ],
    "C field for string": "\w\d",
    "D field for int": 3,
    "E field for real": 10.01,
    "F field for boolean": true,
    "G field for null": null,
    "H field for wildcard": *,
    "I field for negation": !4,
    "J field for macro": <ENV_1>,
    "K field for conditional": (1 | 3 ^ 4 & 2),
    "L field for placeholders": [
        object,
        array,
        string, //Comment 2
        bool,
        int,
        real,
        number
    ],
    "M field for array capture": [
        1,
        "a",
        (1 | 7),
        (2 | 3)x?,
        (6 | 5)x4,
        (5 | 7)x2-?,
        (8 | 0)x?-3,
        (2 | 4)x?-?,
        (1 | 8)x6-7
    ],
    "N field for array ellipsis": [
        3,
        4,
        ...
    ],
    "O field for object capture": {
        "red": "brick",
        "blue": "sky",
        ("a": 1 | "b": 8),
        ("b": 2 | "b": 8)x?,
        ("c": 3 | "b": 8)x4,
        ("d": 4 | "b": 8)x2-?,
        ("e": 5 | "b": 8)x?-3,
        ("f": 6 | "b": 8)x?-?,
        ("g": 7 | "b": 8)x6-7
    },//Comment 4
    "P field for object ellipsis": {
        "red": "brick",
        "blue": "sky",
        ...
    },
    "Q field for different variations of reals": [
        1e-10,
        1.00001,
        1.9E7,
        1.0E4,
        1000.0
    ],
    /*
    Comment 5
    */ "R field for inequalities": [
        int < 5,
        int > 6,
        int <= 5,
        int >= 6,
        real < 5.2,
        real > 6.2,
        real <= 5.2,
        real >= 6.2,
        number < 5,
        number > 6,
        number <= 5,
        number >= 6
    ]
}   
        """
            spec, doc = jspec.scanner.Scanner().scan_pretty(document)
            print(doc)
            exit(0)
            # how to deal with comments
            #spec2 = jspec.loads(document)

            s = str(spec)

            i = 0
            t = ""
            tab = '  '
            in_string = False
            in_macro = False
            for num, c in enumerate(s):
                if c == '"' and not in_macro:
                    in_string = not in_string
                if c == '<' and not in_string:
                    in_macro = True
                elif c == '>' and not in_string:
                    in_macro = False
                if in_string or in_macro:
                    t += c
                elif c in ['{', '[']:
                    # get rid of [], {}, () if s[num:num+1] in 
                    t += c
                    i += 1
                    t += '\n' + tab * i
                elif c in ['}', ']']:
                    i -= 1
                    t += '\n' + tab * i
                    t += c
                elif c in [',']:
                    t += c
                    t += '\n' + tab * i + '\b'
                else:
                    t += c

            #print(t)
            spec2 = jspec.loads(s)

            print(s)


            # if options.outfile is None:
            #     out = sys.stdout
            # else:
            #     out = options.outfile.open('w', encoding='utf-8')
            # with out as outfile:
            #     for obj in objs:
            #         json.dump(obj, outfile, **dump_args)
            #         outfile.write('\n')
        except jspec.scanner.JSPECDecodeError as jde:
            raise SystemExit(jde)

if __name__ == "__main__":
    main()