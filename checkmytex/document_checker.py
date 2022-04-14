import re
import typing

from .checker import Checker, Languagetool, SiUnitx, ChkTex, CheckSpell, \
    Proselint, Cleveref, UniformNpHard
from checkmytex.latex_document import LatexDocument
from checkmytex.checker.problem import Problem
from checkmytex.whitelist import Whitelist
from .checker.spellcheck import AspellChecker
from .rules import Rule


class DocumentChecker:
    """
    Simple class to return the files and its problems of a latex document.
    """

    def __init__(self,  log=print):
        self.log = log
        self.checker = []
        self.rules = []

    def setup_default(self):
        self.log("Using default modules.")
        aspell = AspellChecker()
        if aspell.is_available():
            self.add_checker(aspell)
        else:
            print("Aspell not available. Using pyspellchecker.")
            self.add_checker(CheckSpell())
        self.add_checker(ChkTex())
        self.add_checker(Languagetool())
        self.add_checker(SiUnitx())
        self.add_checker(Proselint())
        self.add_checker(Cleveref())
        self.add_checker(UniformNpHard())
        for checker in self.checker:
            checker.log = self.log

    def add_checker(self, checker: Checker) -> None:
        """
        Add a checker if it is available.
        :param checker: The checker to be added.
        :return: None
        """
        if checker.is_available():
            self.checker.append(checker)
        else:
            print(str(checker), "is not available.")
            guide = checker.installation_guide()
            if guide:
                print(guide)

    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)

    def _filter(self, problems: typing.Iterable[Problem]):
        for rule in self.rules:
            problems = rule.filter(problems)
        return problems

    def find_problems(self,
                      latex_document: LatexDocument,
                      whitelist: Whitelist = None) \
            -> typing.Iterable[Problem]:
        """
        Finds problems of the document. Returns an iterator of file names and
         sorted problems.
        :param latex_document: The latex document to check.
        :param whitelist: The whitelist of problems to ignore.
        :return: Iterator over file name and sorted problems within this file.
        """
        for rule in self.rules:
            rule.prepare(latex_document, whitelist._path)
        return self._filter(self._find_problems(latex_document, whitelist))

    def _find_problems(self,
                       latex_document: LatexDocument,
                       whitelist: Whitelist = None) \
            -> typing.Iterable[Problem]:

        whitelist = whitelist if whitelist else Whitelist()
        for c in self.checker:
            for p in c.check(latex_document):
                if p not in whitelist:
                    yield p
