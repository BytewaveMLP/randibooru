# randibooru
Pulls random images from Derpibooru for your Discord channel enjoyment.

## Setup
1. Install these libraries with `pip`, in order:

  - `discord.py`
  - `requests`
  - `https://github.com/joshua-stone/DerPyBooru/zipball/master` (`derpybooru` currently serves an out-of-date version of the package)
  
  (You might want to look into `virtualenv`s to avoid polluting your global package space)
  
2. `git clone https://github.com/BytewaveMLP/randibooru`
3. Fill in your information for Derpibooru and Discord

  - Obtain a client ID and API key for Discord [here](https://discordapp.com/developers/applications/me)
  - Obtain a Derpibooru API key [here](https://derpibooru.org/users/edit)

4. `python3 randibooru.py`
5. Complete and use this link to invite your instance of Randibooru to a server:

   https://discordapp.com/oauth2/authorize?client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=19456
   
6. ???
7. Profit!

If you don't want to setup Randibooru yourself, feel free to [invite OG Randibooru](https://discordapp.com/oauth2/authorize?client_id=206203876095950850&scope=bot&permissions=19456) to a server of your choice. Please do not overload the bot, however, as requests are **logged**. I **will** find you if you mess anything up.
