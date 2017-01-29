DISCORD_API_TOKEN    = ""
DERPIBOORU_API_TOKEN = ""
COMMAND_PREFIX       = "!"
COMMAND_NAME         = "rb"

USER_BLACKLIST = []

import discord
import asyncio
import random
from derpibooru import Search, sort

client = discord.Client()
helpgame = discord.Game(name = COMMAND_PREFIX + COMMAND_NAME + " <derpi query>", url = "", type = 0)

@client.event
async def on_ready():
	print('Logged in as:')
	print(client.user.name)
	print(client.user.id)
	print('------')
	await client.change_presence(game = helpgame, afk = False)

@client.event
async def on_message(message):
	if message.content == "!rb" or message.content.startswith(COMMAND_PREFIX + COMMAND_NAME + " "):
		print('Request received!') # Debug and logging
		requester = message.author
		print('Requester:', requester.name, '|', requester.id)

		query = message.content[(len(COMMAND_PREFIX + COMMAND_NAME) + 1):].strip() # Strip command from message text
		print('Query:    ', query)
		client.send_typing(message.channel)

		search  = Search().query(query).key(DERPIBOORU_API_TOKEN).sort_by(sort.RANDOM).limit(1) # DerPyBooru searching
		results = list(search)

		responseStr = requester.mention + (' (query: `' + query + '`)' if query != '' else '')

		if len(results) == 0:
			print('Result:    No images found.')
			await client.send_message(message.channel, responseStr + ' No images found.')
		else:
			result = results[0]
			print('Result:   ', result.url)

			if len(result.tags) > 20:
				tags = ", ".join(result.tags[:20]) + "..."
			else:
				tags = ", ".join(result.tags)

			color = random.randint(0, 16777215)

			em = discord.Embed(title = "Derpibooru Image", url = result.url, color = color)
			em.set_image(url = result.image)
			em.add_field(name = "Tags", value = tags, inline = False)
			em.add_field(name = "Score", value = "{score} (+{upvotes}/-{downvotes})".format(score = result.score, upvotes = result.upvotes, downvotes = result.downvotes), inline = True)
			em.add_field(name = "Favorites", value = result.faves, inline = True)
			em.set_footer(text = "Randibooru - Made with <3 by Bytewave")

			await client.send_message(message.channel, responseStr, embed = em)

		print('========')

client.run(DISCORD_API_TOKEN)
