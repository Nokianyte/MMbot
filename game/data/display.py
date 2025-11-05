from bot.client import discord

DISPLAY_CONFIG = {
    'stats': {
        'title': '🩻',
        'channels': {
            'text': [
                {'index': 'Sanity', 'title': '🧠|🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩', 'permissions': {'send_messages': False}},
                {'index': 'Hunger', 'title': '👅|🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩', 'permissions': {'send_messages': False}},
                {'index': 'Health', 'title': '🫀|🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩', 'permissions': {'send_messages': False}},
                {'index': 'Stamina', 'title': '🫁|🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩', 'permissions': {'send_messages': False}},
                {'index': 'Warmth', 'title': '🌡|🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩', 'permissions': {'send_messages': False}}
            ]
        }
    },
    'map': {
        'title': '🗺️',
        'channels': {
            'text': [
                {'index': 0, 'title': '🌫️🌫️🌫️🌫️🌫️', 'permissions': {'send_messages': False}},
                {'index': 1, 'title': '🌫️🌫️🌫️🌫️🌫️', 'permissions': {'send_messages': False}},
                {'index': 2, 'title': '🌫️🌫️🌫️🌫️🌫️', 'permissions': {'send_messages': False}},
                {'index': 3, 'title': '🌫️🌫️🌫️🌫️🌫️', 'permissions': {'send_messages': False}},
                {'index': 4, 'title': '🌫️🌫️🌫️🌫️🌫️', 'permissions': {'send_messages': False}}
            ]
        }
    }
}

class DisplayFactory:
    def __init__(self, guild, member):
        self.guild = guild
        self.member = member
        self.created_channels = {}
    
    async def create_category_with_channels(self, category_title, channel_configs):
        category = await self.guild.create_category_channel(
            category_title,
            overwrites=self._get_base_overwrites()
        )
        
        channels = {}
        
        for config in channel_configs.get('text', []):
            channel = await self.guild.create_text_channel(
                config['title'],
                category=category,
                overwrites=self._get_channel_overwrites(config.get('permissions', {}))
            )
            channels[config['index']] = channel
        
        for config in channel_configs.get('voice', []):
            channel = await self.guild.create_voice_channel(
                config['title'],
                category=category,
                overwrites=self._get_voice_overwrites(config.get('permissions', {}))
            )
            channels[config['index']] = channel
        
        self.created_channels[category_title] = {
            'category': category,
            'channels': channels
        }
        
        return category, channels
    
    def _get_base_overwrites(self):
        return {
            self.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            self.member: discord.PermissionOverwrite(view_channel=True)
        }
    
    def _get_channel_overwrites(self, custom_permissions):
        base = self._get_base_overwrites()
        base[self.member].update(**custom_permissions)
        return base
    
    def _get_voice_overwrites(self, custom_permissions):
        base_overwrites = {
            self.guild.default_role: discord.PermissionOverwrite(
                view_channel=False,
                connect=False
            ),
            self.member: discord.PermissionOverwrite(
                view_channel=True,
                connect=False
            )
        }
        base_overwrites[self.member].update(**custom_permissions)
        return base_overwrites
    
    def get_all_ids(self):
        result = {}
        for category_title, data in self.created_channels.items():
            result[category_title] = {
                'category_id': data['category'].id,
                'channels': {index: channel.id for index, channel in data['channels'].items()}
            }
        return result
