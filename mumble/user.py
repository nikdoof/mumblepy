import time


class User(object):
    def __init__(self, server, user):
        self.__server = server
        self.__user = user

    @property
    def session(self):
        return self.__user.session

    @property
    def id(self):
        return self.__user.userid

    @property
    def muted(self):
        return bool(self.__user.mute)

    @property
    def deafened(self):
        return bool(self.__user.deaf)

    @property
    def suppress(self):
        return bool(self.__user.suppress)

    @property
    def priority_speaker(self):
        return bool(self.__user.prioritySpeaker)

    @property
    def self_muted(self):
        return bool(self.__user.selfMute)

    @property
    def self_deafened(self):
        return bool(self.__user.selfDeaf)

    @property
    def channel(self):
        return self.__server.get_channel(self.__user.channel)

    @property
    def name(self):
        return self.__user.name

    @property
    def online_seconds(self):
        return self.__user.onlinesecs

    @property
    def bytes_per_second(self):
        return self.__user.bytespersec

    @property
    def client_version(self):
        return self.__user.osversion

    @property
    def client_release(self):
        return self.__user.release

    @property
    def plugin_identity(self):
        return self.__user.identity

    @property
    def os(self):
        return self.__user.os

    @property
    def os_version(self):
        return self.__user.osversion

    @property
    def plugin_context(self):
        return self.__user.context

    @property
    def comment(self):
        return self.__user.comment

    @property
    def ip_address(self):
        return self.__user.address

    @property
    def tcp_only(self):
        return bool(self.__user.tcponly)

    @property
    def idle_seconds(self):
        return self.__user.idlesecs

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.__user, key, value)
        self.__server.set_user_state(self.__user)

    def send_message(self, text):
        return self.__server.send_user_message(self.__user.session, text)

    def mute(self):
        return self.update(mute=1)

    def deafen(self):
        return self.update(deaf=1)

    def unmute(self):
        return self.update(mute=0)

    def undeafen(self):
        return self.update(deaf=0)

    def priority_speaker(self):
        return self.update(prioritySpeaker=1)

    def remove_priority_speaker(self):
        return self.update(prioritySpeaker=0)

    def move(self, channel):
        if isinstance(channel, int):
            return self.update(channel=channel)
        return self.update(channel=channel.id)

    def kick(self, reason=''):
        return self.__server.kick_user(self.__user.session, reason)

    def ban(self, reason='', bits=128, duration=360):
        return self.__server.add_ban(self.__user.address, reason, bits, duration)

    def serialize(self):
        return {
            'session': self.__user.session,
            'id': self.__user.userid,
            'priority_speaker': self.__user.prioritySpeaker,
            'mute': self.__user.mute,
            'deaf': self.__user.deaf,
            'suppress': self.__user.suppress,
            'channel': self.__user.channel,
            'name': self.__user.name,
            'online_secs': self.__user.onlinesecs,
            'comment': self.__user.comment,
            'self_mute': self.__user.selfMute,
            'self_deaf': self.__user.selfDeaf,
            'idle_secs': self.__user.idlesecs,
            'ip': '.'.join(map(unicode, self.__user.address[-4:])),
            'os': self.__user.osversion
        }