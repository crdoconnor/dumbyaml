from dumbyaml.exceptions import InvalidYAMLTypeConversion
from dumbyaml.exceptions import InvalidYAMLTypeComparison
import re


FLOAT_REGEXP = re.compile(r"^(\-|\+)?[0-9]+(\.[0-9]*)?$")
INT_REGEXP = re.compile("^(\-|\+)?[0-9]+$")


class YAMLNode(object):
    """Representation of a YAML node."""

    def __init__(self, item):
        """Initialize YAML node from document."""
        if isinstance(item, list) and type(item[0]) != YAMLNode:
            self.item = [YAMLNode(x) for x in item]
        elif isinstance(item, dict) and type(list(item.keys())[0]) != YAMLNode:
            self.item = {}
            for x, y in item.items():
                self.item[x] = YAMLNode(y)
        else:
            self.item = item

    def __repr__(self):
        """String representation of YAML node."""
        if isinstance(self.item, YAMLNode):
            return self.item.__repr__()
        elif isinstance(self.item, list):
            return str([x.__repr__() for x in self.item])
        elif isinstance(self.item, dict):
            item = {}
            for x, y in self.item.items():
                item[x] = y
            return str(item)
        else:
            return self.item

    def __unicode__(self):
        """If YAML node is a string, return unicode representation of it."""
        if isinstance(self.item, str):
            return self.item
        else:
            raise InvalidYAMLTypeConversion(
                "unicode", self.item.__repr__()
            )

    def __str__(self):
        """If YAML node is a string, return string representation of it."""
        if isinstance(self.item, str):
            return self.item
        else:
            raise InvalidYAMLTypeConversion(
                "string",
                self.item.__repr__()
            )

    def __bool__(self):
        """If YAML node is a boolean, return bool represenation of it."""
        if isinstance(self.item, str):
            if str(self.item).lower() in ["yes", "true", ]:
                return True
            elif str(self.item).lower() in ["no", "false", ]:
                return False
            else:
                raise InvalidYAMLTypeConversion(
                    self.item.__repr__(), "bool"
                )
        else:
            raise InvalidYAMLTypeConversion(
                self.item.__repr__(), "bool"
            )

    def __getitem__(self, key):
        """If YAML node is a dict or list, return item via its index."""
        if isinstance(self.item, dict):
            if key not in self.item:
                raise IndexError
            else:
                return self.item[key]
        elif isinstance(self.item, list):
            if isinstance(key, int) and key < len(self.item):
                return self.item[key]
            else:
                raise IndexError
        else:
            raise InvalidYAMLTypeConversion(
                self.item.__repr__(), "list or dict"
            )

    def get(self, key, default=None):
        """If YAML node is a dict, return item via its index."""
        if isinstance(self.item, dict):
            if key not in self.item:
                return default
            else:
                return self.item[key]
        else:
            raise InvalidYAMLTypeConversion(
                self.item.__repr__(), "dict"
            )

    def __eq__(self, item):
        """Equality operator between YAML node."""
        if type(item) == str:
            return str(self) == item
        elif type(item) == int:
            return int(self) == item
        elif type(item) == float:
            return float(self) == item
        elif type(item) == bool:
            return bool(self) == item
        else:
            raise InvalidYAMLTypeComparison(self.item, item)

    def __lt__(self, item):
        """Less than comparison between YAML node and another number."""
        if type(item) == int:
            return int(self) < int(item)
        elif type(item) == float:
            return float(self) < float(item)
        else:
            raise InvalidYAMLTypeComparison(self.item, item)

    def __gt__(self, item):
        """Greater than comparison between YAML node and another number."""
        if type(item) == int:
            return int(self) > int(item)
        elif type(item) == float:
            return float(self) > float(item)
        else:
            raise InvalidYAMLTypeComparison(self.item, item)

    def __nonzero__(self):
        """Bool representation of YAML bool node (or exception)."""
        return self.__bool__()

    def __float__(self):
        """Float representation of YAML float node (or exception)."""
        if isinstance(self.item, YAMLNode):
            raise InvalidYAMLTypeConversion(
                self.item.__repr__(), "list or dict"
            )
        elif FLOAT_REGEXP.match(str(self.item)) is None:
            raise InvalidYAMLTypeConversion(self.item.__repr__(), "float")
        else:
            return float(self.item)

    def __int__(self):
        """Integer representation of YAML integer node (or exception)."""
        if isinstance(self.item, YAMLNode):
            raise InvalidYAMLTypeConversion(self.item.__repr__(), "int")
        elif INT_REGEXP.match(str(self.item)) is None:
            raise InvalidYAMLTypeConversion(self.item.__repr__(), "int")
        else:
            return int(self.item)
