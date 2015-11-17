from yaml.error import YAMLError


class InvalidYAMLTypeComparison(YAMLError):
    """Comparison between two incompatible types."""
    def __init__(self, item1, item2):
        super(YAMLError, self).__init__((
            "Comparison not possible between {0} of type {1} "
            "and {2} of type {3}"
        ).format(
            item1.__repr__(), type(item1), item2.__repr__(), type(item2))
        )


class InvalidYAMLTypeConversion(YAMLError):
    """Invalid attempte YAML type conversion from one type to another."""
    def __init__(self, item_type, item_representation):
        super(YAMLError, self).__init__((
            "Conversion not possible of {0} to {1}"
        ).format(item_type, item_representation))


class DisallowedToken(YAMLError):
    """YAML token disallowed in dumbyaml"""
    def __init__(self, token):
        self.token = token


class FlowMappingDisallowed(DisallowedToken):
    pass


class TagTokenDisallowed(DisallowedToken):
    pass


class AnchorTokenDisallowed(DisallowedToken):
    pass
