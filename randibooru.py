import discord
import asyncio
import random
import derpibooru
import configparser
import os.path
import sys
import traceback
import logging

log = logging.getLogger('randibooru')
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

config = configparser.ConfigParser()

if os.path.isfile('./config.ini'):
	config.read('./config.ini')
else:
	config['Command'] = {'Prefix': '!',
	                     'Name': 'rb'}
	config['API keys'] = {'Derpibooru': '',
	                      'Discord': ''}
	config['Logging'] = {'Level': 'INFO'}
	config['Other'] = {'ImagesPerRequest': 50}

	with open('./config.ini', 'w') as cfgfile:
		config.write(cfgfile)

	log.info('Config file generated!')
	log.info('Edit config.ini before starting Randibooru.')
	sys.exit(1)

level = logging.getLevelName(config.get('Logging', 'Level', fallback = 'INFO'))

try:
	log.setLevel(level = level)
except ValueError:
	log.setLevel(level = logging.INFO)

DISCORD_API_TOKEN    = config.get('API keys', 'Discord')
DERPIBOORU_API_TOKEN = config.get('API keys', 'Derpibooru')
COMMAND_PREFIX       = config.get('Command', 'Prefix', fallback = '!')
COMMAND_NAME         = config.get('Command', 'Name', fallback = 'rb')
COMMAND              = COMMAND_PREFIX + COMMAND_NAME

client = discord.Client()
helpgame = discord.Game(name = COMMAND_PREFIX + COMMAND_NAME + " <derpi query>", url = "", type = 0)

@client.event
async def on_ready():
	log.info('Logged in as ' + client.user.name + ' (' + client.user.id + ')')
	log.info('Use this link to invite me to your server: ' + discord.utils.oauth_url(client.user.id, permissions = discord.Permissions(permissions = 19456)))
	await client.change_presence(game = helpgame, afk = False)

@client.event
async def on_error(event, *args, **kwargs):
	log.error('Exception occurred in ' + event, exc_info = True)

@client.event
async def on_server_join(server):
	general = server.default_channel
	log.info('Joined server ' + server.name + ' (' + server.id + ')')
	if server.me.permissions_in(general).send_messages:
		log.debug('Able to post messages in general channel. Sending welcome message...')
		await client.send_message(general, "**Hey there!** I'm Randibooru! I pull random images from Derpibooru with an optional Derpibooru query.\n"
			+ "To get a random image, simply type `" + COMMAND + "` in chat, and I'll try to respond. You can optionally follow `" + COMMAND + "` with a Derpibooru query (info here: https://derpibooru.org/search/syntax), and I'll only pull images that match it.\n"
			+ "Have fun!\n\n"
			+ "*Made with <3 by Bytewave (https://github.com/BytewaveMLP/randibooru)*\n"
			+ "Join my Discord server! https://discord.gg/AukVbRR\n\n"
			+ "**NOTE:** I will refuse to post images tagged with `explicit` in non-NSFW channels!")

@client.event
async def on_server_remove(server):
	log.info('Removed from server ' + server.name + ' (' + server.id + ')')

@client.event
async def on_message(message):
	if (message.content == COMMAND) or message.content.startswith(COMMAND + " ") and not message.author.bot:
		requester = message.author
		query = message.content[(len(COMMAND) + 1):].strip() # Strip command from message text
		log_user_str = 'from ' + requester.name + ' (' + requester.id + ')' + (' with query ' + query if query != '' else '')
		log.info('Request received ' + log_user_str)
		await client.send_typing(message.channel)

		response_str = requester.mention + (' (query: `' + query + '`)' if query != '' else '')

		search = derpibooru.Search().query(query).key(DERPIBOORU_API_TOKEN).sort_by(derpibooru.sort.RANDOM).limit(int(config.get('Other', 'ImagesPerRequest', fallback = '50'))) # DerPyBooru searching

		results = list(search)

		if len(results) == 0:
			log.info('No results found for request ' + log_user_str)
			await client.send_message(message.channel, response_str + ' - *No images found.*')
		else:
			result = None

			if not message.channel.is_private:
				log.debug('Request ' + log_user_str + ' in channel ' + message.channel.name + ' (' + message.channel.id + ')')
				if message.channel.name != 'nsfw' and not message.channel.name.startswith('nsfw-'):
					log.debug('Request ' + log_user_str + ' was sent in a SAFE channel')
					for potential in results:
						if 'explicit' not in potential.tags:
							result = potential
							break
						log.debug('Skipping unsuitable image ' + potential.url + ' for request ' + log_user_str)
				else:
					log.debug('Request ' + log_user_str + ' was sent in an NSFW channel')
					result = random.choice(results)

				if result is None:
					log.info('Couldn\'t find any safe images to post for request ' + log_user_str)
					await client.send_message(message.channel, response_str + " - *I couldn't find any safe images! Try again, or call me in an NSFW channel for `explicit` images!*")
					return
			else:
				log.debug('Request ' + log_user_str + ' is a PM')
				result = random.choice(results)
			
			log.info('Found suitable result ' + result.url + ' for request ' + log_user_str)

			if len(result.tags) > 20:
				log.debug('Limiting displayed tags to 20 for request ' + log_user_str + ' to keep Discord from yelling at us')
				tags = ", ".join(result.tags[:20]) + "..."
			else:
				tags = ", ".join(result.tags)

			color = random.randint(0, 16777215)

			em = discord.Embed(title = "Derpibooru Image", url = result.url, color = color)
			em.set_image(url = result.representations['full'])
			em.add_field(name = "Tags", value = tags, inline = False)
			em.add_field(name = "Score", value = "{score} (+{upvotes}/-{downvotes})".format(score = result.score, upvotes = result.upvotes, downvotes = result.downvotes), inline = True)
			em.add_field(name = "Favorites", value = result.faves, inline = True)
			em.set_footer(text = "Randibooru - Made with <3 by Bytewave")

			log.debug('Sending embed for request ' + log_user_str)
			await client.send_message(message.channel, response_str, embed = em)

log.info('Randibooru bot starting...')

try:
	client.run(DISCORD_API_TOKEN)
except:
	log.critical('An error occurred while starting Randibooru', exc_info = True)