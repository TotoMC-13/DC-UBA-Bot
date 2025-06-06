import os
from typing import Any

import discord
import motor.motor_asyncio
from pymongo.results import DeleteResult, UpdateResult


class MongoHandler:
    def __init__(self):
        self.client: motor.motor_asyncio.AsyncIOMotorClient | None = None
        self.db: motor.motor_asyncio.AsyncIOMotorDatabase | None = None
        self.vc_collection: motor.motor_asyncio.AsyncIOMotorCollection | None = None

    async def connect(self, db_name: str, collection_name: str):
        db_url = os.getenv("DB_URL")

        if not db_url:
            raise ValueError("La variable de entorno DB_URL no está configurada.")

        self.client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]
        self.vc_collection = self.db[collection_name]

    async def close(self):
        """
        Cierra la conexión con la base de datos.
        """
        if self.client:
            self.client.close()
            print("Conexión a MongoDB cerrada.")

    def _check_connection(self):
        """
        Para asegurarnos que estamos conectados.
        """
        if self.vc_collection is None:
            raise ConnectionError("No conectado a la base de datos. Llama a 'connect()' primero.")

    def _get_vc_query(self, voice_channel: discord.VoiceChannel) -> dict[str, Any]:
        return {
            "type": "authorized_vc",
            "guild_id": voice_channel.guild.id,
            "id": voice_channel.id
        }

    async def add_vc(self, voice_channel: discord.VoiceChannel) -> bool:
        """
        Añade un canal de voz a la lista de autorizados usando una operación 'upsert'.
        Devuelve True si el canal fue insertado, False si ya existía.
        """
        self._check_connection()
        query = self._get_vc_query(voice_channel)
        
        update_doc = {"$set": {"name": voice_channel.name}}

        result: UpdateResult = await self.vc_collection.update_one(query, update_doc, upsert=True)
        
        # result.upserted_id no será None solo si se creó un nuevo documento.
        return result.upserted_id is not None

    async def remove_vc(self, voice_channel: discord.VoiceChannel) -> bool:
        """
        Elimina un canal de voz de la lista.
        Devuelve True si el canal fue eliminado, False si no existía.
        """
        self._check_connection()
        query = self._get_vc_query(voice_channel)
        
        result: DeleteResult = await self.vc_collection.delete_one(query)
        
        # Solo se cumple si se borró un canal.
        return result.deleted_count > 0 

    async def is_configured(self, voice_channel: 'discord.VoiceChannel') -> bool:
        """
        Comprueba si un canal de voz está configurado o no.
        """
        self._check_connection()
        query = self._get_vc_query(voice_channel)

        document = await self.vc_collection.find_one(query, {"_id": 1})
        return document is not None
