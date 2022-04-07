import json
import shutil
import typing

from checkmytex.checker.abstract_checker import Checker
from checkmytex.latex_document import LatexDocument
from checkmytex.problem import Problem


class Languagetool(Checker):
    def __init__(self, ):
        self._lang = "en-US"
        self.disable_rules = ["MORFOLOGIK_RULE_EN_US",
                              # disable spell checking because it is very slow.
                              "WHITESPACE_RULE",
                              # The whitespaces will be off due to detexing.
                              "COMMA_PARENTHESIS_WHITESPACE"
                              # Also not reliable in detexed text.
                              ]

    def check(self, document: LatexDocument) -> typing.Iterable[Problem]:
        print("Running Langugagetool...")
        result, err, ex = self._run(
            f"{shutil.which('languagetool')} --json -l {self._lang} "
            f"--disable {','.join(self.disable_rules)}",
            input=document.get_text())
        data = json.loads(result)
        for problem in data["matches"]:
            try:
                look_up_url = problem["rule"]["urls"][0]["value"]
            except KeyError:
                look_up_url = None
            origin = document.get_origin_of_text(problem["offset"],
                                                 problem["offset"] +
                                                 problem["length"])
            yield Problem(origin=origin,
                          context=problem["context"]["text"],
                          message=problem["message"],
                          long_id=problem["message"]
                                  + problem["context"]["text"],
                          rule=problem["rule"]["id"],
                          tool="languagetool",
                          look_up_url=look_up_url)

    def is_available(self) -> bool:
        return bool(shutil.which("languagetool"))

    def needs_detex(self):
        return True

    def installation_guide(self) -> str:
        return "You can probably install install languagetool directly" \
               " with your package manager.\n" \
               " e.g. brew install languagetool\n" \
               "      apt-get install languagetool\n" \
               "      pacman -S languagetool\n" \
               "...\n" \
               "Otherwise, you can install it by hand:" \
               " https://github.com/languagetool-org/languagetool"