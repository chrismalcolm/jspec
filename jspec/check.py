"""Command-line tool to check if a JSON file matches a JSPEC document.

Usage:

    $ python3 -m jspec.check <jspec_file> <json_file>
    
    -- Checking again a JSON that matches against the JSPEC
    $ python3 -m jspec.check ./test/assets/load.jspec ./test/assets/load.json

    The flags --raw-json and --raw-jspec can also be used to represent the JSON
    or JSPEC raw document instead of giving a file path
  
    -- Checking again a JSON that doesn't match against the JSPEC
    $ python3 -m jspec.check ./test/assets/load.jspec --raw-json='{"key": 2}'
    At location $.key - expected a string, got '2'

    -- Checking again a JSON that matches against the JSPEC
    python3 -m jspec.check --raw-json='[1,2,3,4]' --raw-jspec=[1,...,4]
"""

def main():
    import argparse
    import json
    from pathlib import Path
    import jspec
    
    prog = 'python3 -m jspec.check'
    description = ('A simple command line tool to check if a JSON file matches a JSPEC document')
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        'jspec_file',
        nargs='?',
        type=argparse.FileType(encoding="utf-8"),
        default=None,
        help='a JSPEC file to be checked against'
    )
    parser.add_argument(
        'json_file',
        nargs='?',
        type=Path,
        default=None,
        help='a JSPEC file to be checked'
    )
    parser.add_argument(
        '--raw-jspec',
        dest='jspec_raw',
        default=None,
        help='raw JSPEC document, if none is provided in the other args'
    )
    parser.add_argument(
        '--raw-json',
        dest='json_raw',
        default=None,
        help='raw JSON document, if none is provided in the other args'
    ) 
    options = parser.parse_args()

    try:
        if options.jspec_file is None:
            if options.jspec_raw is None:
                raise ValueError("The --raw-jspec flag value is not a valid JSPEC")
            spec = jspec.loads(options.jspec_raw)
        else:
            spec = jspec.load(options.jspec_file)
        if options.json_file is None:
            if options.json_raw is None:
                raise ValueError("The --raw-json flag value is not a valid JSON")
            element = json.loads(options.json_raw)
        else:
            element = json.load(open(options.json_file, 'r', encoding='utf-8'))
        
        matched, message = jspec.check(spec, element)
        if not matched:
            sys.stdout.write(message)
            sys.stdout.write('\n')

    except (jspec.scanner.JSPECDecodeError, ValueError) as exc:
        raise SystemExit(exc)

if __name__ == '__main__':
    import sys
    try:
        main()
    except BrokenPipeError as exc:
        sys.exit(exc.errno)