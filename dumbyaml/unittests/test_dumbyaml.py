import dumbyaml
import yaml
import pytest


def test_no_implicit_numbers():
    assert dumbyaml.load("x: 3.5") == {"x": "3.5", }
    assert dumbyaml.load("x: +3.5") == {"x": "+3.5", }
    assert dumbyaml.load("x: +1") == {"x": "+1", }
    assert dumbyaml.load("x: 0") == {"x": "0", }
    assert yaml.load("x: 3.5") == {"x": 3.5, }
    assert yaml.load("x: 0") == {"x": 0, }


def test_no_implicit_bools():
    assert dumbyaml.load("x: yes") == {"x": "yes", }
    assert dumbyaml.load("x: NO") == {"x": "NO", }
    assert dumbyaml.load("x: false") == {"x": "false", }
    assert yaml.load("x: yes") == {"x": True, }
    assert yaml.load("x: false") == {"x": False, }


def test_no_implicit_nulls():
    assert dumbyaml.load("x:") == {"x": "", }
    assert dumbyaml.load("x: null") == {"x": "null", }
    assert yaml.load("x:") == {"x": None, }
    assert yaml.load("x: null") == {"x": None, }


def test_tag_token_disallowed():
    with pytest.raises(dumbyaml.TagTokenDisallowed):
        assert dumbyaml.load("""x: !!bool "true"\n""")
    assert yaml.load("""x: !!bool "true"\n""") == {"x": True}


def test_node_anchors_and_references_disallowed():
    with pytest.raises(dumbyaml.AnchorTokenDisallowed):
        assert dumbyaml.load("x: &x 12\ny: *x\n")
    with pytest.raises(dumbyaml.AnchorTokenDisallowed):
        assert dumbyaml.load("x: &x\n")
    assert yaml.load("x: &x 12\ny: *x\n") == {'x': 12, 'y': 12}


def test_flow_style_disallowed():
    with pytest.raises(dumbyaml.FlowMappingDisallowed):
        dumbyaml.load("x: {a: 1, b: 2}")
    assert yaml.load("x: {a: 1, b: 2}") == {"x": {"a": 1, "b": 2}, }
