DISCORD_API_TOKEN    = ""
DERPIBOORU_API_TOKEN = ""
COMMAND_PREFIX       = "!"
COMMAND_NAME         = "rb"

USER_BLACKLIST = []

import discord
import asyncio
from DerPyBooru.derpibooru import Search, sort

client = discord.Client()
helpgame = discord.Game(name = COMMAND_PREFIX + COMMAND_NAME + " <derpi query>", url = "", type = 0)

@client.event
async def on_ready():
	print('Logged in as:')
	print(client.user.name)
	print(client.user.id)
	print('------')
	await client.change_status(game = helpgame, idle = False)

@client.event
async def on_message(message):
	if message.content.startswith(COMMAND_PREFIX + COMMAND_NAME):
		print('Request received!') # Debug and logging
		requester = message.author
		print('Requester:', requester.name, '|', requester.id)

		if requester.id not in USER_BLACKLIST:
			query = message.content[(len(COMMAND_PREFIX + COMMAND_NAME) + 1):] # Strip command from message text
			print('Query:    ', query)

			await client.send_typing(message.channel) # Typing notification while loading

			search  = Search().query(query).key(DERPIBOORU_API_TOKEN).sort_by(sort.RANDOM).limit(1) # DerPyBooru searching
			results = [image for image in search]

			if len(results) == 0:
				print('Result:    No images found.')
				await client.send_message(message.channel, requester.mention + ' (' + query + '): No images found.')
			else:
				result = results[0]
				print('Result:   ', result.url)

				await client.send_message(message.channel, requester.mention + ' (' + query + '): ' + result.url)
		else:
			print("User blacklisted.")

		print('========')

client.run(DISCORD_API_TOKEN)
