# OwOifier
Best Bot

To host this bot for your server:

1) Check to see if you have python3 installed (python3). If not, go to https://www.python.org/downloads/ and download it. It should work with most Python 3 versions
2) Install discord.py + dependencies
Windows: 
>python3 -m pip install -U discord.py;
python3 -m pip install -U requests

Linux: 
>pip install discord.py;
pip install requests
3) Replace the os.chdir("") with your folder containing both the json file and the py file. Make sure it's inside of the quotation marks
4) If you haven't done so, open a Discord Developer account at https://discord.com/developers. Then, make an application, go to the Bot tab, and check Bot to true.  Now, your bot should have a token. Click reveal token and copy the token and paste it at the very bottom of the code -- where it says client.run("TOKEN"). Make sure your token is replacing the TOKEN word, but not the quotation marks or the parentheses.
5) Invite it to your server(s)!
Go to OAuth2, tick bot, give it sufficient perms (standard read, write, edit, manage messages and webhooks). Copy the given link and click on to invite it to your server.
5) Run it! If ya don't, it won't work!
> python3 [location of owoifier file]
