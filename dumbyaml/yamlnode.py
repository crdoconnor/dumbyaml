from dumbyaml.exceptions import InvalidYAMLTypeConversion
from dumbyaml.exceptions import InvalidYAMLTypeComparison
import re


FLOAT_REGEXP = re.compile(r"^(\-|\+)?[0-9]+(\.[0-9]*)?$")
INT_REGEXP = re.compile("^(\-|\+)?[0-9]+$")


class YAMLNode(object):
    """Representation of a YAML node."""

    def __init__(self, item):
        """Initialize YAML node from document."""
        if isinstance(item, list):
            self._currentindex = 0
            if len(item) == 0:
                self.item = item
            elif type(item[0]) != YAMLNode:
                self._curindex = 0
                self.item = [YAMLNode(x) for x in item]
            else:
                self.item = item
        elif isinstance(item, dict):
            self._currentindex = 0
            if len(item) == 0:
                self.item = item
            elif type(list(item.keys())[0]) != YAMLNode:
                self._curindex = 0
                self.item = {}
                for x, y in item.items():
                    self.item[x] = YAMLNode(y)
            else:
                self.item = item
        else:
            self.item = item

    def __repr__(self):
        """String representation of YAML node."""
        if isinstance(self.item, YAMLNode):
            return self.item.__repr__()
        elif isinstance(self.item, list):
            return "[{0}]".format(", ".join([x.__repr__() for x in self.item]))
        elif isinstance(self.item, dict):
            item = {}
            for x, y in self.item.items():
                item[x] = y
            return str(item)
        elif isinstance(self.item, int):
            return str(self.item)
        else:
            return "'{0}'".format(self.item)

    def __unicode__(self):
        """If YAML node is a string, return unicode representation of it."""
        if isinstance(self.item, YAMLNode):
            return str(self.item)
        elif isinstance(self.item, str):
            return self.item
        else:
            raise InvalidYAMLTypeConversion(
                self.item.__repr__(), "unicode"
            )

    def __str__(self):
        """If YAML node is a string, return string representation of it."""
        if isinstance(self.item, YAMLNode):
            return str(self.item)
        elif isinstance(self.item, str):
            return self.item
        else:
            raise InvalidYAMLTypeConversion(
                self.item.__repr__(),
                "string {0}".format(type(self.item))
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
            if isinstance(key, slice):
                return [self[n] for n in range(*key.indices(len(self)))]
            elif isinstance(key, int):
                if isinstance(key, int) and key < len(self.item):
                    return self.item[key]
                else:
                    raise IndexError
            else:
                raise TypeError(
                    "Key {0} should be an index for list {1}".format(
                        key, self.item.__repr__()
                    )
                )
        else:
            raise InvalidYAMLTypeConversion(
                self.item.__repr__(), "list or dict"
            )

    def __len__(self):
        """If YAML node is a dict or list, return its length."""
        if isinstance(self.item, dict) or isinstance(self.item, list):
            return len(self.item)
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

    def __dict__(self):
        """If YAML node is a dict, return a dict representation of it."""
        if isinstance(self.item, dict):
            return self.item
        else:
            raise InvalidYAMLTypeConversion(
                self.item.__repr__(), "dict"
            )

    def __iter__(self):
        if isinstance(self.item, dict) or isinstance(self.item, list):
            self._currentindex = 0
            return self
        else:
            raise InvalidYAMLTypeConversion(
                self.item.__repr__(), "list or dict"
            )

    def next(self):
        if self._currentindex == len(self):
            raise StopIteration
        else:
            if isinstance(self.item, list):
                self._currentindex = self._currentindex + 1
                return YAMLNode(self[self._currentindex - 1])
            elif isinstance(self.item, dict):
                self._currentindex = self._currentindex + 1
                return self.keys()[self._currentindex - 1]
            else:
                raise InvalidYAMLTypeConversion(
                    self.item.__repr__(), "list or dict"
                )

    def __next__(self):
        return self.next()

    def keys(self):
        if isinstance(self.item, dict):
            return self.item.keys()
        else:
            raise InvalidYAMLTypeConversion(
                self.item.__repr__(), "dict"
            )

    def items(self):
        if isinstance(self.item, dict):
            return self.item.items()
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
        elif type(item) == list:
            if len(item) == len(self):
                for x, y in zip(item, self):
                    if x != y:
                        return False
                return True
            else:
                return False
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
