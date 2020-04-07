from settings import TOKEN, yandex_api_weather_key, yandex_api_geo_key
from discord.ext import commands
import discord
import asyncio
import requests

WEATHER_API_SERVER = "https://api.weather.yandex.ru/v1/forecast"
GEOCODE_API_SERVER = 'https://geocode-maps.yandex.ru/1.x/'
HEADERS = {'X-Yandex-API-Key': yandex_api_weather_key}


class WeatherBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.weather_params = {'lang': 'ru_RU',
                               'hours': False,
                               'limit': 2}
        self.geo_params = {'apikey': yandex_api_geo_key,
                           'geocode': 'unnamed',
                           'format': 'json'}

    @commands.command(name='help_bot')
    async def help_bot(self, ctx):
        await ctx.send('Доступные команды:\n'
                       '$place <место> - укажите место прогноза. Например, `$place Kaliningrad`\n'
                       '$current - вывод сообщения о текущей погоде в городе, указанном через команду `$place`.\n'
                       '$forecast <количество дней> - прогноз погоды на указанное количество дней.\n'
                       '$help_bot - для вывода этого сообщения.')

    @commands.command(name='place')
    async def forecast_place(self, ctx, address):
        if isinstance(address, str) and address != '':
            self.geo_params['geocode'] = address
            geo_response = requests.get(GEOCODE_API_SERVER,
                                        params=self.geo_params).json()
            position = geo_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            lon, lat = position.split()
            self.weather_params['lon'], self.weather_params['lat'] = lon, lat
            await ctx.send(f'Успешно сменил место прогноза на {address}')
        else:
            await ctx.send('Пожалуйста, введите корректное название города.')

    @commands.command(name='current')
    async def current_place(self, ctx):
        self.weather_params['limit'] = 2
        weather_response_json = requests.get(WEATHER_API_SERVER, headers=HEADERS,
                                             params=self.weather_params).json()
        current_date = weather_response_json["forecasts"][0]["date"]
        temperature = weather_response_json["fact"]["temp"]
        pressure = weather_response_json["info"]["def_pressure_mm"]
        humidity = weather_response_json['fact']['humidity']
        condition = weather_response_json['fact']['condition']
        wind_dir = weather_response_json['fact']['wind_dir']
        wind_speed = weather_response_json['fact']['wind_speed']
        if self.geo_params['geocode'] == 'unnamed':
            await ctx.send('Вы не указали место прогноза. Для этого воспользуйтесь коммандой `$place <место>`')
            return
        await ctx.send(f'Weather forecast in {self.geo_params["geocode"]} for {current_date}\n'
                       f'Temperature (celsium): {temperature},\n'
                       f'Pressure: {pressure} mm,\n'
                       f'Humidity: {humidity}%,\n'
                       f'Condition: {condition},\n'
                       f'Wind {wind_dir} {wind_speed} m/s.')

    @commands.command(name='forecast')
    async def forecast(self, ctx, days=2):
        try:
            days = int(days)
            if days > 7:
                await ctx.send('Извините, но прогноз погоды мы можем предложить максимум на 7 дней вперёд.')
            elif days <= 0:
                await ctx.send('Извините, не умеем возвращаться в прошлое.')
            elif days == 1:
                await self.current_place(ctx)
            else:
                self.weather_params['limit'] = days
                weather_response_json = requests.get(WEATHER_API_SERVER, headers=HEADERS,
                                                     params=self.weather_params).json()
                days = weather_response_json['forecasts']
                output = []
                for day in days:
                    date = day['date']
                    temp = day["parts"]["day_short"]["temp"]
                    press = day["parts"]["day_short"]["pressure_mm"]
                    humidity = day["parts"]["day_short"]["humidity"]
                    condition = day["parts"]["day_short"]["condition"]
                    wind_dir = day["parts"]["day_short"]["wind_dir"]
                    wind_speed = day["parts"]["day_short"]["wind_speed"]
                    output.append(f'Weather forecast in {self.geo_params["geocode"]} for {date}:')
                    output.append(f'Temperature (celsium): {temp},')
                    output.append(f'Pressure: {press} mm,')
                    output.append(f'Humidity: {humidity}%,')
                    output.append(f'Condition: {condition},')
                    output.append(f'Wind {wind_dir} {wind_speed} m/s.')
                    output.append('\n')
                await ctx.send('\n'.join(output))
        except ValueError:
            await ctx.send('Пожалуйста, введите количество дней для прогноза.')


class BotClient(discord.Client):

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключился к чату:\n'
                f'{guild.name}(id: {guild.id})\n')


bot = commands.Bot(command_prefix='$')
bot.add_cog(WeatherBot(bot))
bot.run(TOKEN)
client = BotClient()
client.run(TOKEN)
