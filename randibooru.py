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
			query = message.content[(len(COMMAND_PREFIX + COMMAND_NAME) + 1):].strip() # Strip command from message text
			print('Query:    ', query)
			if query == '':
				response = await client.send_message(message.channel, requester.mention + ' **Please wait**, searching for images...')
			else:
				response = await client.send_message(message.channel, requester.mention + ' **Please wait**, searching for images with query `' + query + '`...')

			search  = Search().query(query).key(DERPIBOORU_API_TOKEN).sort_by(sort.RANDOM).limit(1) # DerPyBooru searching
			results = list(search)

			responseStr = requester.mention + (' (query: `' + query + '`)' if query != '' else '') + ' '

			if len(results) == 0:
				print('Result:    No images found.')
				await client.edit_message(response, responseStr + 'No images found.')
			else:
				result = results[0]
				print('Result:   ', result.url)

				await client.edit_message(response, responseStr + result.url + "\nFull image: " + result.image)
		else:
			print("User does not have access.")

		print('========')

client.run(DISCORD_API_TOKEN)
