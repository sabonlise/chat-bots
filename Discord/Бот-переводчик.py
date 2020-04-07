from settings import TOKEN, yandex_api_translator_key
from discord.ext import commands
import discord
import asyncio
import requests

API_SERVER = "https://translate.yandex.net/api/v1.5/tr.json/translate"


class TranslateBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.params = {'key': yandex_api_translator_key, 'lang': 'en-ru'}

    @commands.command(name='help_bot')
    async def help_bot(self, ctx):
        await ctx.send('Доступные команды:\n'
                       '$set_lang <«с какого»-«на какой»> - смена языка перевода. Например, $set_lang `en-ru`.\n'
                       '$text <текст> - ввод фразы для перевода.\n'
                       '$help_bot - для вывода этого сообщения.')

    @commands.command(name='set_lang')
    async def set_lang(self, ctx, lang):
        check_lang = lang.split('-')
        if len(check_lang) == 2 and (check_lang[1] != '' and check_lang[0] != ''):
            self.params['lang'] = lang
            await ctx.send(f'Успешно сменил язык перевода на `{lang}`.')
        else:
            await ctx.send('Неверный формат ввода. Напишите `$help_bot` для более подробной информации.')

    @commands.command(name='text')
    async def translate(self, ctx, *, message=''):
        if not message:
            await ctx.send('Пожалуйста, введите сообщение для перевода.')
            return
        self.params['text'] = message
        response = requests.get(API_SERVER, params=self.params)
        json_response = response.json()
        result = json_response['text'][0]
        if result == message:
            await ctx.send(f'Вы ввели текст не на том языке. Текущая раскладка: `{self.params["lang"]}`')
        else:
            await ctx.send(f'Результат перевода:\n{result}')


class BotClient(discord.Client):

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключился к чату:\n'
                f'{guild.name}(id: {guild.id})\n')


bot = commands.Bot(command_prefix='$')
bot.add_cog(TranslateBot(bot))
bot.run(TOKEN)
client = BotClient()
client.run(TOKEN)
