import time
from .user import User
from .channel import Channel


class Server(object):
    def __init__(self, meta, server):
        self.id = server.id()

        self.__meta = meta
        self.__server = server

    def __len__(self):
        return

    @property
    def running(self):
        return bool(self.__server.isRunning())

    def start(self):
        if not self.running:
            return self.__server.start()

    def stop(self):
        if self.running:
            return self.__server.stop()

    def delete(self):
        self.stop()
        return self.__server.delete()

    # Conf

    def get_all_conf(self):
        conf = self.__meta.get_default_conf()
        conf.update(self.__server.getAllConf())
        return conf

    def get_conf(self, key):
        return self.__server.getConf(key)

    def set_conf(self, key, value):
        return self.__server.setConf(key, value)

    # ACLs

    def get_acls(self, channel_id):
        acls, groups, inherit = self.__server.getACL(channel_id)
        return acls

    # Groups

    def get_groups(self, channel_id):
        acls, groups, inherit = self.__server.getACL(channel_id)
        return groups

    # Channels

    def get_channels(self):
        return [Channel(self, channel) for channel in self.__server.getChannels().values()]

    def get_channel(self, channel_id):
        channel = self.__server.getChannelState(channel_id)

        if channel is None:
            return None

        return Channel(self, channel)

    def get_channel_by_name(self, channel_name):
        for channel in self.get_channels():
            if channel.name == channel_name:
                return channel

    def set_channel_state(self, channel):
        self.__server.setChannelState(channel)

    def add_channel(self, name, parent=0):
        channel_id = self.__server.addChannel(name, parent)
        return self.get_channel(channel_id)

    def remove_channel(self, channel_id):
        self.__server.removeChannel(channel_id)

    def send_channel_message(self, channel_id, text, tree=False):
        self.__server.sendMessageChannel(channel_id, tree, text)
        return True

    # Users

    def get_users(self):
        return [User(self, user) for user in self.__server.getUsers().values()]

    def get_user(self, session):
        user = self.__server.getState(session)

        if user is None:
            return None

        return User(self, user)

    def kick_user(self, session, reason=''):
        return self.__server.kickUser(session, reason)

    def send_user_message(self, session_id, text):
        return self.__server.sendMessage(session_id, text)

    def set_user_state(self, state):
        return self.__server.setState(state)

    def get_registrations(self, filter=''):
        return self.__server.getRegistedUsers(filter)

    def get_registration(self, user_id):
        return self.__server.getRegistration(user_id)

    # Bans

    def get_bans(self):
        return self.__server.getBans()

    def set_bans(self, bans):
        self.__server.setBans(bans)

    def add_ban(self, address, reason='', bits=128, duration=360):
        from Murmur import Ban
        bans = self.get_bans()
        bans.append(Ban(
            reason=reason,
            bits=bits,
            duration=duration,
            start=int(time.time()),
            address=address,
        ))
        self.set_bans(bans)

    # Hooks

    def add_hook(self, cls):
        self.__meta.add_hook_to(self.__server, cls, self.id)

    def remove_hook(self, cls, hook):
        self.__meta.remove_hook_from(self.__server, cls, hook)