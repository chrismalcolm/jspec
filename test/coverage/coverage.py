"""Simple script to update the code-coverage badge for the README.md.
"""

import json

with open("./test/coverage/coverage.json", "r") as coverage:
    percentage = int(json.load(coverage)["totals"]["percent_covered"])

with open("./README.md", "r+") as readme:
    data = readme.readlines()
    data[1] = '![check-code-coverage](https://img.shields.io/badge/code--coverage-%i%%-brightgreen)\n\n' % percentage
    readme.seek(0)
    readme.writelines(data)
    readme.truncate()

