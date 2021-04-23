import discord # imports the Discord library
from discord.ext import commands
import random, asyncio

token = "ODM0MTU2MjIxODk2MzI3MjA4.YH8yhQ.-C8i1jb7UfvJAdGfGroLq1y4LNs"

tree = 778733501180149806
desert = 778733501180149801
channel_ids = {
  "desert": 778733501180149801,
  "tree": 778733501180149806,
  "gen": 778733500639477766
}
items_dict = {
  "corpse_part": [720, "Corpse Part",channel_ids["desert"], 778733500148482087],
  "cats": [168, "Cat",channel_ids["desert"], 778760552905834527],
  "dio_diary": [192, "Dio Diary",channel_ids["desert"],784484983308943402],
  "green_child": [216, "Green Child",channel_ids["desert"],784484772310417438],
  "arrow": [12,"Arrow",channel_ids["desert"],778733500169322583],
  "golden_arrow": [48,"Golden Arrow",channel_ids["desert"],778733500169322584],
  "diamond_arrow": [168,"Diamond Arrow",channel_ids["desert"],778744411798110248],
  "berries": [36,"Berry",channel_ids["tree"], 778733500169322577]
}
corpse_parts = [
  ["The Head",    778733500148482087],
  ["The Ears",    778733500148482086],
  ["The Eyes",    778733500148482085],
  ["The Spine",   778733500148482084],
  ["The Rib Cage",778733500148482083],
  ["The Heart",   778733500148482082],
  ["The Arms",    778733500148482081],
  ["The Pelvis",  778733500148482080],
  ["The Legs",    778733500148482079]
]

client = commands.Bot(command_prefix = "j!")
prefix = 'j!'

updates = ["Alpha test, everything has been pushed to an online hosting platform, we'll see how it goes."]

def CE(**info):
  info.setdefault('title','Araki Bot')
  info.setdefault('description','No description was provided for this embed')
  info.setdefault('color', discord.Color.purple())
  embed = discord.Embed(title=info['title'],description=info['description'],color=info['color'])
  embed.set_footer(text='Made by Elephant#5716 2021')

  return embed

class items():
  def __init__(self,thing, goal,description,channel,role,full_item):
    if thing == "corpse_part":
      y = random.choice(corpse_parts)
      self.description = y[0]
      self.role = y[1]
    else:
      self.description = description
      self.role = role
    self.hour = 0
    self.firm_goal = goal
    self.goal = self.firm_goal + (random.randint(-5,5)/10)
    self.thing = thing
    # self.description = description
    self.active = True
    class message:
      id = 0
    self.message = message
    # self.role = role
    # self.message = <id = 0>
    self.channel = channel

  async def itemTiming(self):
    while True:
      print(f"{self.thing} ({self.description}): {self.hour}/{self.goal}")
      await asyncio.sleep(180) # 180
      self.hour += .05
      self.hour = round(self.hour, 2)
      if self.hour >= self.goal:
        self.active = True
        self.message = await client.get_channel(self.channel).send(embed=CE(description=f"A {self.description} has dropped! React with :hand_splayed: to pick it up! (Pick it up before its next drop or it will vanish!)",title=self.description))
        await self.message.add_reaction("🖐️")

        # print(self.message.guild.get_member(618574628608278528))
        
        # await client.wait_for('reaction_add')

        self.hour = 0
        self.goal = self.firm_goal + (random.randint(-5,5)/10)
  async def spacer():
    tick = 0
    while True:
      print(f"- - {tick} - -")
      await asyncio.sleep(180) # 180
      tick += .05
      tick = round(tick, 2)
  async def claimMessage(self, load):
    x = await self.message.guild.fetch_member(load.user_id)
    print([y.id for y in x.roles])

    temprole = discord.Object(self.role)
    if self.active == True and self.role not in [y.id for y in x.roles]:
      await x.add_roles(temprole)
      await client.get_channel(load.channel_id).send(embed=CE(description = f"<@{load.user_id}> has claimed the {self.description}! Good job!",title=self.description))
      self.active = False
    elif self.active == True and self.role in [y.id for y in x.roles]:
      await client.get_channel(load.channel_id).send(embed=CE(description = f"<@{load.user_id}> has claimed the {self.description}!",title=self.description))
      self.active = False
    else: pass


@client.event
async def on_raw_reaction_add(payload):
  if payload.user_id != client.user.id and payload.emoji.name == "🖐️" and payload.message_id in [x.message.id for x in listofitems]:
    asyncio.create_task(listofitems[[x.message.id for x in listofitems].index(payload.message_id)].claimMessage(payload))
  else: pass


@client.event
async def on_ready(): 
  global listofitems
  print("Client info:")
  print()
  print("{0.user} Has been successfully updated!\n".format(client))
  await client.change_presence(activity=discord.Game(name="OI, JOSUKE!")) # Sets status 
  jojo_gen_channel = client.get_channel(778733500639477766)
  await jojo_gen_channel.send(embed = CE(description="Up and running. Updates include:\n\n{}".format("\n".join(updates))))

  listofitems = []
  for y in range(len(items_dict)):
    listofitems.append(items(list(items_dict.keys())[y],list(items_dict.values())[y][0],list(items_dict.values())[y][1],list(items_dict.values())[y][2],list(items_dict.values())[y][3], list(items_dict.values())[y]))
  for x in listofitems:
    asyncio.create_task(x.itemTiming())
  asyncio.create_task(items.spacer())
  
@client.event
async def on_message(message):
  if message.content.startswith(prefix) and message.author != client.user:
    message.channel.send("Heard you")


client.run(token)
