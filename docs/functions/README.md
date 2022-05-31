# JSPEC Functions
The documentation here summarizes the exported functions for the JSPEC module.

---
**`load(file, pretty=False, indent=None)`**

This function creates a JSPEC instance, generated from a JSPEC file object **file**. Set **pretty** to True for the serialization of the JSPEC instance to be in a pretty format, with new lines and indentations. Set **indent** to set the actual indent for when using the pretty formatting.

---
**`loads(document, pretty=False, indent=None)`**

This function creates a JSPEC instance, generated from a JSPEC document string **document**. Set **pretty** to True for the serialization of the JSPEC instance to be in a pretty format, with new lines and indentations. Set **indent** to set the actual indent for when using the pretty formatting.

---
**`dump(spec, file)`**

This function dumps the serialization of the JSPEC instance **spec** into the file object **file**.

---
**`dumps(spec, file)`**

This function returns the serialization of the JSPEC instance **spec**.

---
**`check(spec, element)`**

This function will run a validation check of the object **element** against the JSPEC instance **spec**. It will return a bool on whether the validation passed, as well as a reason if the validation failed.

---
**`checks(document, element)`**

This function will run a validation check of the object **element** against a JSPEC instance generated from a JSPEC document string **document**. It will return a bool on whether the validation passed, as well as a reason if the validation failed.