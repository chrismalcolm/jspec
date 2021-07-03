# .jspec constants for parser and regex

JSPEC_ARRAY_ELEMENT_SUBSITUTION = "JSPEC_ARRAY_ELEMENT_SUBSITUTION"
JSPEC_ARRAY_TEMPLATE_VALUE = "JSPEC_ARRAY_TEMPLATE_VALUE"
JSPEC_OBJECT_ITEMS_SUBSITUTION = "JSPEC_OBJECT_ITEMS_SUBSITUTION"
JSPEC_OBJECT_TEMPLATE_VALUE = "JSPEC_OBJECT_TEMPLATE_VALUE"

JSPEC_ELLIPSIS_SUBSITUTIONS = {
    r"\[\s*\.\.\.\s*\]": lambda m: m.group(0).replace("...", '"%s"' % JSPEC_ARRAY_ELEMENT_SUBSITUTION),
    r"\[\s*\.\.\.\s*[^\,\s]": lambda m: m.group(0).replace("...", '"%s",' % JSPEC_ARRAY_TEMPLATE_VALUE),
    r"[^\,\s]\s*\.\.\.\s*\]": lambda m: m.group(0).replace("...", ',"%s"' % JSPEC_ARRAY_TEMPLATE_VALUE),
    r"\[\s*[^\{]*\s*\.\.\.\s*\,": lambda m: m.group(0).replace("...", '"%s"' % JSPEC_ARRAY_ELEMENT_SUBSITUTION),
    r"\,\s*\.\.\.\s*[^\}]*\s*\]": lambda m: m.group(0).replace("...", '"%s"' % JSPEC_ARRAY_ELEMENT_SUBSITUTION),
    r"\{\s*\.\.\.\s*\}": lambda m: m.group(0).replace("...", '"%s": true' % JSPEC_OBJECT_ITEMS_SUBSITUTION),
    r"\{\s*\.\.\.\s*[^\,\s]": lambda m: m.group(0).replace("...", '"%s": true,' % JSPEC_OBJECT_TEMPLATE_VALUE),
    r"[^\,\s]\s*\.\.\.\s*\}": lambda m: m.group(0).replace("...", ',"%s": true' % JSPEC_OBJECT_TEMPLATE_VALUE),
    r"\{\s*[^\[]*\s*\.\.\.\s*\,": lambda m: m.group(0).replace("...", '"%s": true' % JSPEC_OBJECT_ITEMS_SUBSITUTION),
    r"\,\s*\.\.\.\s*[^\]]*\s*\}": lambda m: m.group(0).replace("...", '"%s": true' % JSPEC_OBJECT_ITEMS_SUBSITUTION)
}