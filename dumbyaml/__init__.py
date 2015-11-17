"""Dumb YAML Parser"""
from dumbyaml.dumbloader import DumbLoader
from dumbyaml.yamlnode import YAMLNode
from dumbyaml import exceptions
import yaml


def load(
    document,
    allow_flow_style=False,
    allow_tag_tokens=False,
    allow_anchor_tokens=False
):
    """Return a YAMLItem object representation of a dumb yaml document"""
    for token in yaml.scan(document):
        if type(token) == yaml.tokens.FlowMappingStartToken and \
           not bool(allow_flow_style):
                raise exceptions.FlowMappingDisallowed(token)
        if type(token) == yaml.tokens.TagToken and \
           not bool(allow_tag_tokens):
            raise exceptions.TagTokenDisallowed(token)
        if type(token) == yaml.tokens.AnchorToken and \
           not bool(allow_anchor_tokens):
            raise exceptions.AnchorTokenDisallowed(token)

    return YAMLNode(yaml.load(document, Loader=DumbLoader))


def dump(data):
    """Return a YAML document."""
    return yaml.dump(data, default_flow_style=False)
