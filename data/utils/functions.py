import time 
import colorama
import discord
from discord.ext import commands
from termcolor import cprint as col_print
from pprint import PrettyPrinter

def prettify_string(phrase:str):
    '''just takes in something like "hi_there" and will return something like "Hi There"'''
    phrase.replace("_", " ")
    phrase.capitalize()
    return phrase

def cprint(to_print:str, color=None, on_color=None, have_to_pprint=False) -> None:
    '''This is the some to termcolor.cprint(), but prints the string line by Line'''
    if have_to_pprint:
        printer = PrettyPrinter(stream=None, indent=1, width=80, depth=None, compact=False, sort_dicts=True)
        to_log = printer.pformat(to_log)
    for line in to_print.split('\n'):
        col_print(line, color, on_color)

def console_log(to_log:str, color=None, on_color=None, have_to_pprint=False) -> None:
    '''Same as data.custom.functions.cprint(), but puts a timestamp before printing the line, and also puts the line into logs.txt'''
    logs = open("console.log", "a")
    if have_to_pprint:
        printer = PrettyPrinter(stream=None, indent=1, width=80, depth=None, compact=False, sort_dicts=True)
        to_log = printer.pformat(to_log)
    for line in to_log.split('\n'):
        to_print = f'[{time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime())}] {line}'
        col_print(to_print, color, on_color)
        logs.write(to_print+'\n')
    logs.close()
                        
def read_file(filename):
    '''Just reads a file and returns the content in it'''
    f = open(filename)
    content = f.read()
    f.close()
    return content

def get_role_from_msg(message):
    if message.content.startswith("<@&"):
        role_id = int(str(message.content)[3:-1])
        role = message.guild.get_role(role_id)
        return role
    else:
        for role in message.guild.roles:
            if role.name == message.content:
                return role