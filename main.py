import discord
import requests
import json
import random
import mysql.connector
import requests
from io import BytesIO

# Database
# Connects to server

db = mysql.connector.connect(
  host = "127.0.0.1",
  port = 8889,
  user="root",
  password="root",
  database="image_bot"
)

tags = {}

# Sets cursor
cursor = db.cursor()

# Discord bot
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

async def send_embed(msg, title, description, db):
    embed = discord.Embed(color=0x53d5fd)
    embed.add_field(name=title, value=description, inline=False)
    await msg.channel.send(embed=embed)
    return

# To download an image from a link
async def download_image(name, link):
    response = requests.get(link)

    if response.status_code == 200:
        content = response.content
        im = BytesIO()
        im.write(content)
        filename = name
        with open(filename, "wb") as f:
            f.write(im.getvalue())
    else:
        print("Error downloading image")

async def define_message(msg_obj):
    message = {
        "User": str(msg_obj.author),
        "Text": "",
        "File_Name": "",
        "File_Link": "",
        "Tag": []
    }
    msg = msg_obj.content
    if '#' in msg:
        message["File_Name"] = msg[msg.index('(')+1:msg.index(')')]
        message["File_Link"] = msg[msg.index(')')+1:]

        print(message)
    if '$' in msg and '#' not in msg:
        location = []
        for i in range(len(msg)):
            if msg[i] == '"':
                location.append(i)
        print(location)
        message["Text"] = msg[location[0]+1:location[1]]
        print(message)
    if msg_obj.attachments:
        message["File_Link"] = str(msg_obj.attachments[0].url)
    if '!' in msg:
        message["Tag"] = msg[msg.index('[')+1:msg.index(']')]
        print(message)
    if '$' in msg and '#' in msg:
        message["Text"] = msg[msg.index('$')+1:msg.index('#')]
        print(message)
        # Download image
        await download_image(message["File_Name"], message["File_Link"])
    # Only stores text
    return message

# Code for database store and retrieval
async def store(msg):
    message = await define_message(msg)

    sql = "INSERT INTO inputs(User, Text, File_Name, Image_Link, Time) VALUES (%s, %s, %s, %s, %s)"
    this_time = msg.created_at
    time = str(this_time.year)+ '-' + str(this_time.month) + '-' + str(this_time.day)
    print(time)
    val = (message["User"], message["Text"], message["File_Name"], message["File_Link"], str(time))
    # Inserts values into database
    cursor.execute(sql, val)
    db.commit()

    await send_embed(msg, "Sent", "Your file has been saved!", 0)

    print(cursor.rowcount, "record inserted.")
    return

async def return_image(msg):
    message = await define_message(msg)
    path = "/Users/call911pls/Desktop/De Anza Hackathon Project/"
    path = path + message["File_Name"]
    file = discord.File(path, filename=message["File_Name"])
    path = "attachment://"
    path = path + message["File_Name"]
    embed = discord.Embed()
    embed.set_image(url=path)
    print("File Sent")
    await msg.channel.send(file=file, embed=embed)

async def tag_image(msg):
    message = await define_message(msg)
    if message["Tag"] in tags:
        tags[message["Tag"]].append(message["Text"])
    else:
        temp = []
        temp.append(message["Text"])
        new_tag = {message["Tag"]: temp}
        tags.update(new_tag)
    print(tags)
    await send_embed(msg, "Tagged!", "Your file has been tagged", tags)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    discord.Intents.all()
    msg = message.content

    # Database message storage
    if msg.startswith("store$"):
        await store(message)

    # Database retrival
    if msg.startswith("get#"):
        await return_image(message)

    if msg.startswith("tag!"):
        await tag_image(message)
    
                      

client.run('MTE2NTA0NTYxODUyODQ4NTQ0Nw.G-HZWb.OJMUeWTn105JF4RsIXGgDvKYvZN-ixZ9cCXYF8')
