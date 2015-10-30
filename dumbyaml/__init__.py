"""Dumb YAML Parser"""
from dumbyaml.dumbloader import DumbLoader
from yaml.error import YAMLError
import yaml


class DisallowedToken(YAMLError):
    def __init__(self, token):
        self.token = token


class FlowMappingDisallowed(DisallowedToken):
    pass


class TagTokenDisallowed(DisallowedToken):
    pass


class AnchorTokenDisallowed(DisallowedToken):
    pass


def load(document):
    """Loads a 'dumb' yaml document."""
    for token in yaml.scan(document):
        if type(token) == yaml.tokens.FlowMappingStartToken:
            raise FlowMappingDisallowed(token)
        if type(token) == yaml.tokens.TagToken:
            raise TagTokenDisallowed(token)
        if type(token) == yaml.tokens.AnchorToken:
            raise AnchorTokenDisallowed(token)

    return yaml.load(document, Loader=DumbLoader)
