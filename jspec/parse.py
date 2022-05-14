"""Command-line tool to validate and pretty print JSPEC documents.

The --indent flag can be used to set the pretty print indentation.
Pretty printing can be set off using the --pretty flag.

Usage (1):

    python3 -m jspec.parse <infile> <outfile>
    
    -- Output the JSPEC file in pretty format to command line
    $ python3 -m jspec.parse ./test/assets/load.jspec
    {
        "key": "value"
    }

    -- Output the JSPEC file in pretty format to command line with custom indent
    $ python3 -m jspec.parse ./test/assets/load.jspec --indent='  '
    {
      "key": "value"
    }

    -- Output the JSPEC file in pretty format into file
    $ python3 -m jspec.parse ./test/assets/load.jspec test.jspec
    
Usage (2):

    echo <document> | python3 -m jspec.parse

    -- Pretty print JSPEC document string
    $ echo '{"jspec": "term", ...}' | python3 -m jspec.parse
    {
        "jspec": "term",
        ...
    }

    -- Normal print JSPEC document string
    $ echo '{"jspec": "term", ...}' | python3 -m jspec.parse --pretty=false
    {"jspec": "term", ...}

    -- Error with incorrect format
    $ echo '[1,2,,4]' | python3 -m jspec.parse
    Expecting JSPEC term in array: line 1 column 6 (char 5)
"""

def main():
    import argparse
    from pathlib import Path
    import jspec
    
    prog = 'python3 -m jspec.parse'
    description = ('A simple command line tool for the JSPEC module and pretty print JSPEC documents.')
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        'infile',
        nargs='?',
        type=argparse.FileType(encoding="utf-8"),
        default=sys.stdin,
        help='a JSPEC file to be validated or pretty printed'
    )
    parser.add_argument(
        'outfile',
        nargs='?',
        type=Path,
        default=None,
        help='write the output of infile to outfile'
    )
    parser.add_argument(
        '--pretty',
        dest='pretty',
        default=True,
        help='should the data written to outfile be pretty printed'
    )
    parser.add_argument(
        '--indent',
        dest='indent',
        default='    ',
        help='what is the tab indentation for pretty printing'
    )
    options = parser.parse_args()

    try:
        options.pretty = not options.pretty == "false"
        spec = jspec.load(options.infile, pretty=options.pretty, indent=options.indent)
        if options.outfile is None:
            outfile = sys.stdout
        else:
            outfile = options.outfile.open('w', encoding='utf-8')  
        jspec.dump(spec, outfile)
        outfile.write('\n')

    except (jspec.scanner.JSPECDecodeError, TypeError) as exc:
        raise SystemExit(exc)

if __name__ == '__main__':
    import sys
    try:
        main()
    except BrokenPipeError as exc:
        sys.exit(exc.errno)