from yaml.reader import Reader
from yaml.scanner import Scanner
from yaml.parser import Parser
from yaml.composer import Composer
from yaml.constructor import SafeConstructor
from yaml.resolver import BaseResolver


class DumbLoader(
    Reader, Scanner, Parser, Composer, SafeConstructor, BaseResolver
):

    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        SafeConstructor.__init__(self)
        BaseResolver.__init__(self)
