import json
import requests
import urllib3
import random
import os
import asyncio
import time
import discord

from discord.ext import commands
os.chdir("/home/ryon/code/python/owoifier/")

client = commands.Bot(command_prefix = 'owo ')

bypass = True

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please send all the required arguments. type `owo help` for more information")

@client.event
async def on_message(message):
    await client.process_commands(message)

    with open("channels.json", "r") as f:
        data = json.load(f)

    try: #may be useless... possibly check
        if data[str(message.channel.id)]:
            can_post = True
    except:
        can_post = False


    try: #trying to see if channel has all messages set to true
        if data[str(message.channel.id)]["if_all"] == "false":
            can_post = False

            if str(message.author.id) in data[str(message.channel.id)]["allowed_members"]:
                can_post = True
            
            for role in message.author.roles:
                for role2 in data[str(message.channel.id)]["roles"]:
                    if int(role.id) == int(role2):
                        if not data[str(message.channel.id)]["roles"][role2]["exempt"]:
                            can_post = True
    except:
        pass
    
    if str(message.channel.id) in data: #solely for passives
        if data[str(message.channel.id)]["passive"]["enabled"]: #updates passives if there is a passive
            if random.random() < data[str(message.channel.id)]["passive"]["chance"]:
                if not str(message.author.id) in data[str(message.channel.id)]["passive"]["members"]: #checking to see if person is already in passive
                    if data[str(message.channel.id)]["passive"]["TBA"] != 0:
                        data[str(message.channel.id)]["passive"]["members"][str(message.author.id)] = round(time.time())  #puts person in list with time that it was put in list for
                    else:
                        can_post = True
            for member in data[str(message.channel.id)]["passive"]["members"]:
                if str(member) == str(message.author.id):
                    can_post = True
            with open('channels.json', 'w') as f:
                json.dump(data, f)
            

    if can_post:

        if message.author.bot:
            return

        try:
            for role in message.author.roles:
                for role2 in data[str(message.author.id)]["roles"]:
                    if int(role.id) != int(role2):
                        if data[str(message.author.id)]["roles"][role2]["exempt"]:
                            return
        except:
            pass


        url = data[str(message.channel.id)]["webhook"]

        stuffs = []
        try:
            for stuff in files:
                stuffs.append(stuff)
        except:
            pass

        data = {} #creating the message
        data["content"] = furryto(str(message.content))
        data["username"] = str(message.author.display_name)
        data["avatar_url"] = str(message.author.avatar_url)

        #if message.author.id == 277250557696147457:
        #    return

        result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})  #posting the message

        await message.delete() #deleting OG message
    else:
        pass


def furryto(message):

    
    message = message.replace("r", "w"); message = message.replace("R", "W"); message = message.replace("🇷", "🇼")
    message = message.replace("v", "w"); message = message.replace("V", "W"); message = message.replace("🇻", "🇼")
    message = message.replace("l", "w"); message = message.replace("L", "W"); message = message.replace("🇱", "🇼")
    message = message.replace("ought", "ot"); message = message.replace("OUGHT", "OT")
    message = message.replace("'", "")
    
    message2 = ""
    for letter in message:
        if letter == "o":
            letter = random.choice(["o", 'o', 'o', 'o', 'owo'])
        if letter == "u":
            letter = random.choice(["u", 'u', 'u', 'u', 'uwu'])
        message2 += letter
    message = message2

    message += random.choice(["", "", "", "", " owo", " uwu", " X3"])
    return message

@client.command()
async def aboutme(ctx):
    await ctx.send("PLACEHOLDER"  )




@client.command()
async def ping(ctx):
    await ctx.send("Pong! `{}".format(round(client.latency * 1000)) + "ms`")

@client.command()
@commands.has_permissions(manage_webhooks = True)
async def setup_channel(ctx, channel: discord.TextChannel):


    channel = channel.id

    with open("channels.json", "r") as f:
        data = json.load(f)

    for chanid in data:
        if str(channel) == str(chanid):
            await ctx.send("This channel has already been configured before. ")
            return

    channelnum = channel
    channel = client.get_channel(int(channel))

    try:
        webhook = await channel.create_webhook(name=channel)
    except:
        await ctx.send("Make sure you send a valid channel ID to configure")
        return
    
    data[str(channelnum)] = {}
    data[str(channelnum)]["allowed_members"] = {}
    data[str(channelnum)]["roles"] = {}
    data[str(channelnum)]["if_all"] = True
    data[str(channelnum)]["webhook"] = str(webhook.url)
    data[str(channelnum)]["passive"] = {"enabled": False, "chance": 0, "TBA": 0, "members": {}}

    with open('channels.json', 'w') as f:
        json.dump(data, f)

    await ctx.send("All configured! May the hell commence.")

@client.event
async def on_ready():
    print("bot ready")
    bypass = False

@client.command(manage_webhooks = True)
@commands.has_permissions(manage_webhooks = True)
async def remove_channel(ctx, channel: discord.TextChannel):


    channel = channel.id

    with open("channels.json", "r") as f:
        data = json.load(f)
    
    url = data[str(channel)]["webhook"]
    result = requests.delete(url)

    del data[str(channel)]

    with open("channels.json", "w") as f:
        json.dump(data, f)

    await ctx.send("Successfully removed webhook. Was it not fun for you?")

@client.command(manage_webhooks = True)
@commands.has_permissions(manage_webhooks = True)
async def update_channel(ctx, channel: discord.TextChannel, _if_all):

    channel = channel.id

    with open("channels.json", "r") as f:
        data = json.load(f)
    
    if _if_all == ("true" or "True"):
        _if_all = True
    elif _if_all == ("false" or "False"):
        _if_all = "false"
    else:
        await ctx.send("Please make sure you type either false or true for the if_all boolean")
        return

    if str(channel) in data:
        pass
    else:
        await ctx.send("Make sure you have a valid channel ID and that you first configure your channel using `owo setup_channel [channel]`")
        return
    
    data[str(channel)]["if_all"] = _if_all

    with open("channels.json", "w") as f:
        json.dump(data, f)

    await ctx.send("Successfully updated settings for this channel")

@client.command(manage_webhooks = True)
@commands.has_permissions(manage_webhooks = True)
async def update_roles(ctx, channel: discord.TextChannel, exempt, *, role: discord.Role):
    with open("channels.json", "r") as f:
        data = json.load(f)

    channel = channel.id

    if str(exempt) == "true":
        exempt = True
    elif str(exempt) == "false":
        exempt = False
    else:
        await ctx.send("Make sure the exempt boolean is either True or False! If set to False, it will make the role owo-ified. If set to True, it will make the role immune to owospeak.")
        return

    if str(channel) in data:
        pass
    else:
        await ctx.send("Make sure you have a valid channel and that you first configure your channel using `owo setup_channel [channel]`")
        return

    rolz = []
    for rol in ctx.guild.roles:
        rolz.append(rol)

    passrole = False
    for role2 in rolz:
        if str(role2) == str(role):
            passrole = True
    
    if passrole:
        if not role in data[str(channel)]["roles"]:
            data[str(channel)]["roles"][role.id] = {}
            data[str(channel)]["roles"][role.id]["exempt"] = exempt
            await ctx.send("Added the role to that channel. May that role prosper / suffer")
        else:
            data[str(channel)]["roles"][role.id]["exempt"] = exempt
            await ctx.send("Updated the roles to that channel. May that role prosper / suffer")

        with open("channels.json", "w") as f:
            json.dump(data, f)

    else:
        await ctx.send("Make sure you enter a valid role that your server already has!")
        return

@client.command(manage_webhooks = True)
@commands.has_permissions(manage_webhooks = True)
async def remove_roles(ctx, channel: discord.TextChannel, *, role: discord.Role):
    with open("channels.json", "r") as f:
        data = json.load(f)
    if not role == "all":
        role = str(role)

    channel = channel.id

    if str(channel) in data:
        pass
    else:
        await ctx.send("Make sure you have a valid channel that is configured with the `owo setup_channel command`.")
        return
    
    if not role == "all":
        if not role in data[str(channel)]["roles"]:
            await ctx.send("This role has not been detected with the specified channel. Setup roles with the `owo update_role` command first")
        else:
            del data[str(channel)]["roles"][role.id]
            await ctx.send("Removed the role to that channel. May that role prosper / suffer")
    elif role == "all":
        for rol in data[str(channel)]["roles"]:
            del data[str(channel)]["roles"][role.id]
            await ctx.send("Removed all the roles to that channel. May those role prosper / suffer")

    with open("channels.json", "w") as f:
        json.dump(data, f)

@client.command(manage_webhooks = True)
@commands.has_permissions(manage_webhooks = True)
async def update_members_for(ctx, channel: discord.TextChannel, *people: discord.Member):

    channel = channel.id

    persons = []
    for person in people:
        persons.append(str(person.id))

    people = persons
    with open("channels.json", "r") as f:
        data = json.load(f)

    if str(channel) in data:
        pass
    else:
        await ctx.send("Make sure you have a valid channel ID and that you first configure your channel using `owo setup_channel [channel]")
        return
    
    for person in people:
        if client.get_user(int(person)) == None:
            await ctx.send("Please enter valid user IDs")
            return
        
        data[str(channel)]["allowed_members"][str(person)] = str(person)
    
    data[str(channel)]["if_all"] = "false"

    with open("channels.json", "w") as f:
        json.dump(data, f)
    
    await ctx.send("Successfully updated allowed people for this channel")

@client.command()
@commands.has_permissions(manage_webhooks = True)
async def remove_members_for(ctx, channel: discord.TextChannel, *people: discord.Member):


    channel = channel.id

    persons = []
    for person in people:
        persons.append(str(person.id))

    people = persons

    with open("channels.json", "r") as f:
        data = json.load(f)

    if str(channel) in data:
        pass
    else:
        await ctx.send("Make sure you have a valid channel ID and that you first configure your channel using `owo setup_channel [channel]`")
        return
    
    for person in people:
        if client.get_user(int(person)) == None:
            await ctx.send("Please enter valid user IDs")
            return

        del data[str(channel)]["allowed_members"][(str(person))]
    
    with open("channels.json", "w") as f:
        json.dump(data, f)
    
    await ctx.send("Successfully updated allowed people for this channel")

@client.command()
@commands.has_permissions(manage_webhooks = True)
async def check_integrity(ctx, channel: discord.TextChannel):
    with open("channels.json", "r") as f:
        data = json.load(f)

    if str(channel.id) in data:
        try:
            url = data[str(channel.id)]["webhook"]
            data = {} #creating the message
            data["content"] = "Channel is functional"
            data["username"] = "OwOifier"
            data["avatar_url"] = "https://cdn.discordapp.com/app-icons/701192860355002478/552e5411f87ca36da845bf4496c686d6.png"

            result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"}) 
        except:
            await ctx.send("Channel is not functional. Please delete this channel and set it up again.")
    else:
        await ctx.send("Channel is not set up")

@client.command()
@commands.has_permissions(manage_webhooks = True)
async def create_passive(ctx, channel: discord.TextChannel, chance, TBA):
    with open("channels.json", "r") as f:
        data = json.load(f)
    

    chance = int(chance)
    if chance > 1:
        await ctx.send("chance should be a float. the higher the value is (closer to 1), the higher of a chance it is.")
        return
    elif chance < 0:
        await ctx.send("chance should be greater than zero. Now what is negative chance supposed to mean?")
        return

    try:
        TBA = int(TBA)
        if (TBA <= 10):
            await ctx.send("your duration should be greater than 5 seconds. Alternatively, if you only want one message owoified, set it to 0.")
            return
        if TBA > 999:
            await ctx.send("your duration should also be less than 1000 seconds (17 minutes). Wouldn't want us having too much fun, now do we?")
            return
        if TBA % 5 != 0:
            await ctx.send("your duration will be rounded to the nearest multiple of 5 since the bot only updates every 5 seconds.")
    except:
        await ctx.send("duration should be an integral value")
        return

    data[str(channel.id)]["passive"]["enabled"] = True
    data[str(channel.id)]["passive"]["chance"] = chance
    data[str(channel.id)]["passive"]["TBA"] = TBA

    await ctx.send(f"Channel is now setup with chance 1/{chance} and Duration {TBA} seconds.")

    with open("channels.json", "w") as f:
        json.dump(data, f)

@client.command()
@commands.has_permissions(manage_webhooks = True)
async def remove_passive(ctx, channel: discord.TextChannel):
    with open("channels.json", "r") as f:
        data = json.load(f)
    
    if not data[str(channel.id)]["passive"]["enabled"]:
        await ctx.send("This channel does not already have a passive setup.")
        return
    
    data[str(channel.id)]["passive"]["enabled"] = False
    data[str(channel.id)]["passive"]["chance"] = 0
    data[str(channel.id)]["passive"]["TBA"] = 0

    await ctx.send("Successfully removed passive. Were you having too much fun?")

@client.command(aliases = ["praise", "master", "F", "credits"])
async def ourmaster(ctx):

    await ctx.send("Pay respects to our co-overlord: {}".format("<@277250557696147457>"))
    await ctx.send("Special Thanks to Discord.py and its rewrite branch for making this bot possible!")
    await ctx.send("Join our master's server here: {}".format("discord.gg/NzQbeTk"))

@client.command()
async def id(ctx, person : discord.Member):

    await ctx.send(f"This person's Social Security mumber (or, if you prefer, discord ID) is `{person.id}`")

@client.command()
async def ify(ctx, *, message):

    await ctx.send(furryto(message))
    await message.delete()

@client.command()
async def pp(ctx):
    string = '8'
    test = 2
    if (random.randint(0, 100) == 1):
        await ctx.send("Warning:rotating_light::rotating_light::rotating_light::warning::warning::warning::no_entry_sign::no_entry_sign::no_entry_sign::no_entry_sign::no_entry_sign::no_entry_sign::warning::warning::warning: [scanning... 10%] [scanning... 48%] [scanning... 72%] [scanning complete.] system consensus:PP LENGTH HAS BEEN DETECTED THAT IS SO LARGE THE SYSTEM CANNOT PUT IT IN NUMBERS FOR A SIMPLIFIED VERSION OF YOUR PP HERE IS A SIMULATED IMAGE 8∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞ AND SO FORTH DUE TO TIP BEING UNABLE TO BE FOUND. WE'LL TRY TO COMPREHEND YOUR PP LATER WITH OUR NEW TECHNOLOGY BUT FOR NOW STAY OFF THE PP MEASURER")
        return
    while (test != 3):
        string += '='
        test = random.randint(0, 5)
    string += 'D'
    await ctx.send(string)

async def update_passive():
    await client.wait_until_ready()

    coro = True
    while True:
        with open("channels.json", 'r') as f:
            data = json.load(f)
        
        for chan in data:
            if data[chan]["passive"]["enabled"]:
                for person in list(data[chan]["passive"]["members"]):
                    if int(data[chan]["passive"]["members"][person]) <= (round(time.time()) - data[chan]["passive"]["TBA"]):
                        del data[chan]["passive"]["members"][person]

        with open("channels.json", 'w') as f:
            json.dump(data, f)

        await asyncio.sleep(5)

client.loop.create_task(update_passive())
client.run("TOKEN")
