import discord
from discord.ext import commands
import random
import os

os_slash="\\"

#Administration
admin_list = { 0 } #List of Admin User IDs - Put the owner and the bot IDs here
admin_role = 0 #Set the role ID for administrators here
permissions = 8 #Admin Integer

#Variables
cur_path = os.path.dirname(os.path.realpath(__file__))
bot_id = None
bot_token = "" #Add the token here
server_id = 0  #Add your server ID here

server = None
roles = { "admin" : None}

status = discord.Game("with the API")
invite_link = "" #Add your server invite link here

#Discord.py Bot

async def Log(info):
	logs_file = open(f"{cur_path}{os_slash}logs.txt", "a")
	logs_file.write(info)
	logs_file.write("\n\n")
	logs_file.close()

client = commands.Bot(command_prefix='!')

#Events
@client.event
async def on_ready(): #Initialize
	global bot_id
	global roles
	global server
	bot_id = client.user.id
	server = client.get_guild(server_id)
	roles["admin"] = server.get_role(admin_role)
	await client.change_presence(status=discord.Status.online, activity=status)

@client.event
async def on_error():
	Log("Error!")

@client.event
async def on_message(message):
	await Log(f"Channel: {message.channel}\nUser: {message.author.name}#{message.author.id}\nMessage:{message.content}")
	if(message.author.id != bot_id):
		await client.process_commands(message)

#Commands
@client.command(name="invite", description="Retrieve invite link", pass_context=True) #!invite
async def invite(ctx):
	await ctx.send(f"{ctx.message.author.mention} use the following link to invite someone: {invite_link}")
#----------------------------------------------------
client.remove_command("help")
@client.command(name="help", description="Retrieve list of commands", pass_context=True)
async def help(ctx):
	command_list="\n".join([cmd.name + " - " + cmd.description for cmd in client.commands])
	await ctx.send(f"{ctx.author.mention}\n```{command_list}```")
#----------------------------------------------------
@client.command(name="kick", description="Kick member from server", pass_context=True) #!kick @someone
async def kick(ctx, *, member : discord.Member):
	if(ctx.message.author.id in admin_list or roles["admin"] in ctx.author.roles):
		await member.kick()
		await ctx.send(f"The user {member.mention} has been kicked")
	else:
		await ctx.send(f"You are not allowed to use this command {ctx.author.mention}")
#----------------------------------------------------
@client.command(name="ban", description="Ban member from server", pass_context=True) #!ban @someone
async def ban(ctx, *, member : discord.Member):
	if((ctx.message.author.id in admin_list or roles["admin"] in ctx.author.roles) and member.author.id not in admin_list):
		await member.ban()
		await ctx.send(f"The user {member.mention} has been banned")
	else:
		await ctx.send(f"You are not allowed to use this command {ctx.author.mention}")
#----------------------------------------------------
@client.command(name="unban", description="Unban member from server", pass_context=True) #!unban someone#id
async def unban(ctx, *, member):
	if(ctx.message.author.id in admin_list or roles["admin"] in ctx.author.roles):
		ban_list = await server.bans()
		for banned_user in ban_list:
			user = banned_user.user
			if(f"{str(user.name)}#{str(user.discriminator)}" == member):
				await server.unban(user)
				await ctx.send(f"The user {user.mention} has been unbanned")
	else:
		await ctx.send(f"You are not allowed to use this command {ctx.author.mention}")

#Run
client.run(bot_token)