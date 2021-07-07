# JSPEC constants for parser and regex

JSPEC_ARRAY_ELEMENT_SUBSTITUTION = "JSPEC_ARRAY_ELEMENT_SUBSTITUTION"
JSPEC_ARRAY_TEMPLATE_VALUE = "JSPEC_ARRAY_TEMPLATE_VALUE"
JSPEC_OBJECT_ITEMS_SUBSTITUTION = "JSPEC_OBJECT_ITEMS_SUBSTITUTION"
JSPEC_OBJECT_TEMPLATE_VALUE = "JSPEC_OBJECT_TEMPLATE_VALUE"

JSPEC_ELLIPSIS_SUBSTITUTIONS = {
    r"\[\s*\.\.\.\s*\]": lambda m: m.group(0).replace("...", '"%s"' % JSPEC_ARRAY_ELEMENT_SUBSTITUTION),
    r"\[\s*\.\.\.\s*[^\,\s]": lambda m: m.group(0).replace("...", '"%s",' % JSPEC_ARRAY_TEMPLATE_VALUE),
    r"[^\,\s]\s*\.\.\.\s*\]": lambda m: m.group(0).replace("...", ',"%s"' % JSPEC_ARRAY_TEMPLATE_VALUE),
    r"\[\s*[^\{]*\s*\.\.\.\s*\,": lambda m: m.group(0).replace("...", '"%s"' % JSPEC_ARRAY_ELEMENT_SUBSTITUTION),
    r"\,\s*\.\.\.\s*[^\}]*\s*\]": lambda m: m.group(0).replace("...", '"%s"' % JSPEC_ARRAY_ELEMENT_SUBSTITUTION),
    r"\{\s*\.\.\.\s*\}": lambda m: m.group(0).replace("...", '"%s": true' % JSPEC_OBJECT_ITEMS_SUBSTITUTION),
    r"\{\s*\.\.\.\s*[^\,\s]": lambda m: m.group(0).replace("...", '"%s": true,' % JSPEC_OBJECT_TEMPLATE_VALUE),
    r"[^\,\s]\s*\.\.\.\s*\}": lambda m: m.group(0).replace("...", ',"%s": true' % JSPEC_OBJECT_TEMPLATE_VALUE),
    r"\{\s*[^\[]*\s*\.\.\.\s*\,": lambda m: m.group(0).replace("...", '"%s": true' % JSPEC_OBJECT_ITEMS_SUBSTITUTION),
    r"\,\s*\.\.\.\s*[^\]]*\s*\}": lambda m: m.group(0).replace("...", '"%s": true' % JSPEC_OBJECT_ITEMS_SUBSTITUTION)
}