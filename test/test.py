import unittest

from test.exported.exported import JSPECTestExported

from test.scanner.array import JSPECTestScannerArray
from test.scanner.arraycapture import JSPECTestScannerArrayCapture
from test.scanner.boolean import JSPECTestScannerBoolean
from test.scanner.comment import JSPECTestScannerComment
from test.scanner.conditional import JSPECTestScannerConditional
from test.scanner.macro import JSPECTestScannerMacro
from test.scanner.int import JSPECTestScannerInt
from test.scanner.negation import JSPECTestScannerNegation
from test.scanner.null import JSPECTestScannerNull
from test.scanner.object import JSPECTestScannerObject
from test.scanner.objectcapture import JSPECTestScannerObjectCapture
from test.scanner.placeholder import JSPECTestScannerPlaceholder
from test.scanner.real import JSPECTestScannerReal
from test.scanner.string import JSPECTestScannerString
from test.scanner.wildcard import JSPECTestScannerWildcard

from test.matcher.array import JSPECTestMatcherArray
from test.matcher.arraycapture import JSPECTestMatcherArrayCapture
from test.matcher.boolean import JSPECTestMatcherBoolean
from test.matcher.conditional import JSPECTestMatcherConditional
from test.matcher.error import JSPECTestMatcherError
from test.matcher.int import JSPECTestMatcherInt
from test.matcher.macro import JSPECTestMatcherMacro
from test.matcher.null import JSPECTestMatcherNull
from test.matcher.negation import JSPECTestMatcherNegation
from test.matcher.object import JSPECTestMatcherObject
from test.matcher.objectcapture import JSPECTestMatcherObjectCapture
from test.matcher.placeholder import JSPECTestMatcherPlaceholder
from test.matcher.real import JSPECTestMatcherReal
from test.matcher.string import JSPECTestMatcherString
from test.matcher.wildcard import JSPECTestMatcherWildcard

if __name__ == "__main__":
    unittest.main()