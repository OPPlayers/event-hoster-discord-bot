# This module was the first file in this repository, i wrote this when event hoster was just a personal bot for simon says events in my server
# I am now going to update some old variable names to the current event-hoster's conventions

import discord
import gspread
import asyncio
import os

from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands, tasks
from urllib.request import urlopen
from data.utils.functions import console_log
from ast import literal_eval


class DatabaseFetcher(commands.Cog):

    # Logging into google sheets here
    def __init__(self, client):
        scope = [
            "https://spreadsheets.google.com/feeds",
            'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name("ServiceAccountCreds.json", scopes=scope)
        gspread_client = gspread.authorize(creds)
        sheet = gspread_client.open("api-tutorial").sheet1 # my google sheet was called api-tutorial then, idk why i didn't change it then, NOR AM I GOING TO CHANGE IT NOW, SIKE.
        self.client = client
        self.sheet = sheet
        self.fetchdatabase.start()

    def cog_unload(self):
        self.fetchdatabase.stop()

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.id_list = dict()

    @tasks.loop(minutes=15)
    async def fetchdatabase(self):
        console_log('Database fetch has started', "yellow")

        # Fetching the database
        sheet = self.sheet
        raw_database = sheet.get_all_records()
        id_list = dict()
        raw_database_to_list = list()

        for row_dict in id_list:
            # I am first going to get the values in a list to make things easier
            current_row_values = list()
            for item_index in row_dict:
                current_row_values.append(row_dict[item_index])
            id_list[current_row_values[0]] = {
                'id_channel_simonsays': current_row_values[1],
                'id_role_simonalive': current_row_values[2],
                'id_role_simondead': current_row_values[3],
                'id_role_simoncontroller': current_row_values[4]
            }

            raw_database_to_list.append(current_row_values)

        await asyncio.sleep(3)  # To make sure Google doesn't rate limit me

        # Pushing the local data to the online database
        data_to_push = list()

        for row in raw_database_to_list:
            if row[0] in self.client.id_list:
                continue
            data_to_push.append([
                row[0],
                self.client.id_list[row[0]]['id_channel_simonsays'],
                self.client.id_list[row[0]]['id_role_simonalive'],
                self.client.id_list[row[0]]['id_role_simondead'],
                self.client.id_list[row[0]]['id_role_simoncontroller']
            ])

        sheet.append_rows(data_to_push)

        self.client.id_list.update(id_list)

        console_log('Database fetch finished', "green")

    @fetchdatabase.before_loop
    async def before_fetch_loop(self):
        console_log(
            "Checking if the client is ready to start data.events.database-fetcher : tasks.loop", "blue")
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(DatabaseFetcher(client))
