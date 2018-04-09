import argparse
import json
import logging
import functools
import operator
import os

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.history import FileHistory

from lark import Lark, UnexpectedInput, InlineTransformer
from lark.reconstruct import Reconstructor

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

from pygments.token import Token
from prompt_toolkit.styles import style_from_dict

default_style = style_from_dict({
    Token.Name: 'bold #009AC7',
    Token.Symbol: 'bold #00FF00',
    Token.Mode: 'bold #dadada',
    Token.ModeSymbol: '#ffaf00',
    Token.Menu.Completions.Completion: 'bg:#74B3CC #204a87',
    Token.Menu.Completions.Completion.Current: 'bold bg:#274B7A #ffffff',
    Token.Menu.Completions.Meta: 'bg:#2C568C #eeeeee',
    Token.Menu.Completions.Meta.Current: 'bold bg:#274B7A #ffffff',
    Token.Menu.Completions.MultiColumnMeta: 'bg:#aaaaaa #000000',
    Token.Menu.Completions.ProgressBar: 'bg:#74B3CC',
    Token.Menu.Completions.ProgressButton: 'bg:#274B7A',
    Token.Toolbar: '#ffffff bg:#333333',
})


# We explicitly define all terminal in order to predict their name for
# the completion mapping
knet_grammar = """
start : createtopo                     -> createtopo
      | _DELETE_TOPO                   -> deletetopo
      | ping                           -> ping
      | _PINGALL                       -> pingall
      | _EXIT 						   -> exit
      | _HELP                    	   -> help

createtopo     : _CREATE_TOPO " "  FILENAME
ping           : _PING " " HOSTNAME " " HOSTNAME

FILENAME : STRING
HOSTNAME : STRING

%import common.ESCAPED_STRING   -> STRING
%import common.NUMBER
"""

knet_tokens = """
_CREATE_TOPO : "createtopo"
_DELETE_TOPO : "deletetopo"
_HELP : "?" | "help"
_EXIT : "exit"
_PINGALL : "pingall"
_PING : "ping"
"""

larkParser = Lark(knet_grammar + knet_tokens)

# From the tokens string, generates a completion dict
def token_to_completions(tokens):
    c = {}
    for i in tokens.split("\n"):
        t = i.replace(" ", "").replace('"', '').split(":")
        if len(t) == 2:
            c.update({t[0]: t[1]})
    return c

# This is to generate completions based on parsing errors
token_mapping = {"__COMMA": ",",
                 "__RPAR": ")",
                 "__LPAR": "(",
                 "__DOT": "."}

token_mapping.update(token_to_completions(knet_tokens))


def help():
    msg = (
        "--- The KNet Shell help ---\n"
        "  ?                    help command\n"
        "  createtopo           create a new topology\n"
        "  deletetopo           delete the topology\n"
        "  gettopo              get the topology details\n"
        "  pingall              ping all the systems \n"
        "  ping                 ping between two systems \n"
        "  tcptest              tcptest between two hosts \n"
        "  udptest              udptest between two hosts \n"
        "  execute              execute the commands in the hosts \n"
        "  version              version \n"
        "  exit                 exit from the shell \n"
    )
    print(msg)


def get_host_list():
    return ["a1", "a2", "a3"]

def get_completions(query):
    completions = []
    position = 0
    try:
        larkParser.parse(query + "\0")
    except UnexpectedInput as e:
        logging.debug("UnexpectedInput: %s" % e)
        partial = ""
        position = e.column - len(query)
        if "HOSTNAME" in e.allowed:
            completions = get_host_list()
        else:
            partial = query[e.column:]
            completions = [token_mapping[c] for c in e.allowed
                           if token_mapping.get(c)]
        completions = [c for c in completions if c.startswith(partial)]
    return position, sorted(set(completions))


class KNetValidator(Validator):
    def validate(self, document):
        if document.text == "":
            raise ValidationError(message='Input cannot be empty!',
                                  cursor_position=len(document.text))
        try:
            larkParser.parse(document.text)
        except:
            raise ValidationError(message='This is a non valid command',
                                  cursor_position=len(document.text))


class KNetCompleter(Completer):
    def __init__(self):
        pass

    def get_completions(self, document, complete_event):
        position, c = get_completions(document.text_before_cursor)
        return [Completion(i, start_position=position) for i in c]





class ShellTree(InlineTransformer):
    formatter = "json"

    def exit(self, *args):
        return ("exit", None)

    def help(self, *args):
        return ("help", None)

    def createtopo(self, *args):
        return ("createtopology", args[0])

    def deletetopo(self, *args):
        return ("deletetopology", None)

    def pingall(self, *args):
        return ("pingall", None)

    def ping(self, *args):
        return ("ping", args)


def get_default_prompt_tokens(cli):
    return [
        (Token.Name, "KNet-Cli"),
        (Token.Symbol, "#")
        ]

def main():
    parser = argparse.ArgumentParser(
         description='KNet Network Topology Builder Shell')
    parser.add_argument('--debug', default=False,
                        action="store_true",
                        help='Enable debug mode')
    parser.add_argument('--disable-validation', default=False,
                        action="store_true",
                        help='Disable Gremlin query validation')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    #print("Using Skydive Analyzer %s:%s" % (args.host, args.port))

    hdr = '''
    ****************************************************************
    *                                                               *
    *    Knet Virtual Network Topology Builder -   Interactive CLI  *
    *                                                               *
    *                                                               *
    *    Author:  KNet Solutions (knetsolutions2@gmail.com)         *
    *                                                               *
    *    License : Apache                                           *
    *****************************************************************
    '''
    print(hdr)
    conf_dir = os.path.expanduser('~/.config/knet-cli/')
    os.makedirs(conf_dir, exist_ok=True)
    history = FileHistory(os.path.os.path.join(conf_dir, "history"))

    validator = KNetValidator()
    if args.disable_validation:
        print("WARINING: ':set' commamnds are not supported when 'disable-validation' is set")
        validator = None

    # formatFunctionName = format_json
    while True:
        query = prompt(get_prompt_tokens=get_default_prompt_tokens,
                       style=default_style,
                       completer=KNetCompleter(),
                       validator=validator,
                       history=history,
                       complete_while_typing=True)

        tree = larkParser.parse(query)
        logging.debug("Tree: %s" % tree)
        action, arg = ShellTree().transform(tree)

        print(action)
        if action == "help":
            help()
        elif action == "exit":
            exit(0)
        elif action == "createtopo":
            print("createtopology called with arg", arg)
        elif action == "deletetopo":
            print("deletetopology called ")
        elif action == "pingall":
            print("pingall called")
        elif action == "ping":
            print("ping called")
        else:
            pass

main()
