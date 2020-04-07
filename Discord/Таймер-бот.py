from settings import TOKEN
from discord.ext import commands, timers
import discord
from datetime import datetime, timedelta
import re
import asyncio


class TimeParse:
    def __init__(self, argument):
        compiled = re.compile(r"(?:(?P<hours>[0-9]{1,5})h)?(?:(?P<minutes>[0-9]{1,5})m)?(?:(?P<seconds>[0-9]{1,5})s)?$")
        self.original = argument
        try:
            self.seconds = int(argument)
        except ValueError as e:
            match = compiled.match(argument)
            if match is None or not match.group(0):
                raise commands.BadArgument('Укажите правильное время, например, `4h`, `3m` или `2s`') from e

            self.seconds = 0
            #hours = match.group('hours')
            if (hours := match.group('hours')) is not None:
                self.seconds += int(hours) * 3600
            #minutes = match.group('minutes')
            if (minutes := match.group('minutes')) is not None:
                self.seconds += int(minutes) * 60
            #seconds = match.group('seconds')
            if (seconds := match.group('seconds')) is not None:
                self.seconds += int(seconds)

        if self.seconds <= 0:
            raise commands.BadArgument('Извините, не умеем возвращаться в прошлое')

        if self.seconds > 604800:
            raise commands.BadArgument('7 дней - это долго, тебе не кажется?')

    @staticmethod
    def human_timedelta(dt):
        now = datetime.utcnow()
        delta = now - dt
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        years, days = divmod(days, 365)

        if days:
            if hours:
                return '%s и %s' % (Plural(дней=days), Plural(часов=hours))
            return Plural(дней=days)

        if hours:
            if minutes:
                return '%s и %s' % (Plural(часов=hours), Plural(минут=minutes))
            return Plural(часов=hours)

        if minutes:
            if seconds:
                return '%s и %s' % (Plural(минут=minutes), Plural(секунд=seconds))
            return Plural(минут=minutes)
        return Plural(секунд=seconds)


class Plural:
    def __init__(self, **attr):
        iterator = attr.items()
        self.name, self.value = next(iter(iterator))

    def __str__(self):
        v = self.value
        if v % 2 == 0:
            return '%s %sы' % (v, self.name)
        return '%s %s' % (v, self.name)


class TimerBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['set_timer'])
    @commands.cooldown(1, 10, commands.cooldowns.BucketType.user)
    async def timer(self, ctx, time: TimeParse, *, message=''):
        reminder = None
        completed = None
        message = message.replace('@everyone', '@\u200beveryone').replace('@here', '@\u200bhere')

        if not message:
            reminder = ':timer: Хорошо {0.mention}, устанавливаю таймер на {1}.'
            completed = ':alarm_clock: Время X пришло {0.mention}!'
        else:
            reminder = ':timer: Хорошо {0.mention}, устанавливаю таймер для `{2}` на {1}.'

        human_time = datetime.utcnow() - timedelta(seconds=time.seconds)
        human_time = TimeParse.human_timedelta(human_time)
        await ctx.send(reminder.format(ctx.author, human_time, message))
        await asyncio.sleep(time.seconds)
        await ctx.send(completed.format(ctx.author, message, human_time))

    @timer.error
    async def timer_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(str(error))
        elif isinstance(error, commands.errors.CommandOnCooldown):
            seconds = str(error)[34:]
            await ctx.send(f':alarm_clock: Кулдаун! Пожалуйста, попробуйте ещё раз через {seconds = }')



class BotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключился к чату:\n'
                f'{guild.name}(id: {guild.id})\n')


bot = commands.Bot(command_prefix='$')
bot.timer_manager = timers.TimerManager(bot)
bot.add_cog(TimerBot(bot))
bot.run(TOKEN)
client = BotClient()
client.run(TOKEN)
