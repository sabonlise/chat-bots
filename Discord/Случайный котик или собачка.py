import discord
from settings import TOKEN
import requests


class BotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключился к чату:\n'
                f'{guild.name}(id: {guild.id})\n'
                f'Готов показывать случайного котика (или пёсика!)')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return
        if 'кот' in message.content.lower():
            cat_request = 'https://api.thecatapi.com/v1/images/search'
            json_response = requests.get(cat_request).json()
            random_cat = json_response[0]['url']
            await message.channel.send(random_cat)
        elif 'соба' in message.content.lower():
            dog_request = 'https://dog.ceo/api/breeds/image/random'
            json_response = requests.get(dog_request).json()
            random_dog = json_response['message']
            await message.channel.send(random_dog)


client = BotClient()
client.run(TOKEN)
