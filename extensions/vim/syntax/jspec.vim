" Vim syntax file
" Language:    JSPEC
" Maintainer:  Chris Malcolm <malcochris123@hotmail.co.uk>
" Last Change: 20/05/2022
" Version:     0.1.0

if exists("b:current_syntax")
  finish
endif

" JSPEC single line comment
syn region jspecComment   start="\/\/" end="\n"

" JSPEC multiline comment
syn region jspecComment   start="\/\*" end="\*\/"

" JSPEC operators
syn match jspecOperator   ">=\|<=\|=\|>\|<\|&\||\|\^\|!"

" JSPEC macro
syn match jspecMacro      "<.*>"

" JSPEC string
syn match jspecString     "\".*\""

" JSPEC object key
syn match jspecObjectKey  "\"[^\"]*\"\s*:"

" JSPEC number
syn match jspecNumber     "\d\|e\|E\|-\|\."

" JSPEC multiplier
syn match jspecMultiplier "x\|?"

" JSPEC constant
syn match jspecConstant   "true\|false\|object\|array\|string\|int\|real\|number\|bool\|null\|*\|\.\.\."

" JSPEC braces
syn match jspecBraces     "[{}\[\]\(\)]"

command -nargs=+ HiLink hi def link <args>
HiLink jspecComment Comment
HiLink jspecOperator Special
HiLink jspecMacro Constant
HiLink jspecString String
HiLink jspecObjectKey Operator
HiLink jspecNumber Function
HiLink jspecMultiplier Function
HiLink jspecConstant Function
HiLink jspecBraces Special
delcommand HiLink