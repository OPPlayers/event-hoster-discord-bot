import discord
import os
import json
from discord.ext import commands
from termcolor import cprint
import colorama

client = commands.Bot(command_prefix=('z!', '.', '!', '>', '>>>', '-'), case_insensitive=True)
client.version = "v0.0.4"
client.id_list = {}
colorama.init()

def author_is_zacky(ctx) -> bool:
    return ctx.author.id == 625987962781433867

def read_file(filename):
    f = open(filename)
    content = f.read()
    f.close()
    return content

def boot_bot(blacklisted_extensions : tuple) -> None: # i am not using the on_ready event because then the on_ready event in cogs won't work, and putting it all in a function so its looking clean
    # unecessary decoration (i like it please don't attack me)
    cprint(read_file("startup_ascii.txt").format(client.version), "blue")
    # getting list of all paths to extensions
    filelist = []
    for root, dirs, files in os.walk("data/"):
        for file in files:
            filelist.append(os.path.join(root,file))

    # And then loading them    
    for file in filelist:
        if file.endswith('.py'):
            file = file.replace('/', '.').replace('\\', '.')[:-3]
            try:
                if file not in blacklisted_extensions:
                    client.load_extension(f"{file}")
                    cprint(f"Loaded extension: {file}", "yellow")
                else:
                    cprint(f"Blacklisted extension not loaded: {file}", "red")
            except Exception as e:
                print(f"Failed to load the extension: {file}, reason: {e}`")


boot_bot(blacklisted_extensions = ("data.events.database-fetcher"))
@client.event
async def on_ready():              
    cprint('\nCommands and Extensions loaded, boot successful\n', "green")
    cprint("Below are the messages from the extensions:", "cyan")
    
@client.command()
@commands.check(author_is_zacky)
async def reload_extension(ctx, extension):
    try:
        client.unload_extension(extension)
        client.load_extension(extension)
        msg = "Reloaded {} extension.".format(extension)
        print(msg)
        await ctx.send(msg)
    except Exception as e:
        await ctx.send(e)
        print("Extension Reload failed: {}".format(e))
        
@client.command()
@commands.check(author_is_zacky)
async def unload_extension(ctx, extension):
    try:
        client.unload_extension(extension)
        msg = "Unloaded {} extension".format(extension)
    except Exception as e:
        msg = "Failed to unload extension {}, {}".format(extension, e)
    
    print(msg)
    await ctx.send(msg)
    
@client.command()
@commands.check(author_is_zacky)
async def load_extension(ctx, extension):
    try:
        client.load_extension(extension)
        msg = "Loaded {} extension".format(extension)
    except Exception as e:
        msg = "Failed to load extension {}, {}".format(extension, e)
    
    print(msg)
    await ctx.send(msg)

# Everything is in the Data and Cogs only commands here are for loading and unloading those commands and the dev commands
# gonna add commands later

client.run(read_file("token.txt"))