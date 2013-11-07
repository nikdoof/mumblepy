import time


class User(object):
    def __init__(self, server, user):
        self.__server = server
        self.__user = user

    @property
    def session(self):
        """Return the session ID of the user."""
        return self.__user.session

    @property
    def id(self):
        """Return the user ID of the user, if they are registered."""
        return self.__user.userid

    @property
    def muted(self):
        """Indicates if the user is currently muted."""
        return bool(self.__user.mute)

    @property
    def deafened(self):
        """Indiciates if the user is currently deafened"""
        return bool(self.__user.deaf)

    @property
    def suppress(self):
        """Indiciates if the user has been suppressed by the server due to lack of permissions"""
        return bool(self.__user.suppress)

    @property
    def priority_speaker(self):
        """Indiciates if the user is currently a Priority Speaker"""
        return bool(self.__user.prioritySpeaker)

    @property
    def self_muted(self):
        """Indiciates if the user has self muted."""
        return bool(self.__user.selfMute)

    @property
    def self_deafened(self):
        """Indiciates if the user is self-deafened."""
        return bool(self.__user.selfDeaf)

    @property
    def channel(self):
        """Returns the ``Channel`` object for the user's current channel"""
        return self.__server.get_channel(self.__user.channel)

    @property
    def name(self):
        """The user's display name"""
        return self.__user.name

    @property
    def online_seconds(self):
        """Returns the number of seconds the user has been connected to the server."""
        return self.__user.onlinesecs

    @property
    def bytes_per_second(self):
        """Returns the current bps speed of the user's connection to Mumble."""
        return self.__user.bytespersec

    @property
    def client_version(self):
        """Returns the version of the user's Mumble client."""
        return self.__user.osversion

    @property
    def client_release(self):
        """Returns the release of the user's Mumble client."""
        return self.__user.release

    @property
    def plugin_identity(self):
        """If a plugin is active for the user, this returns the plugin's identity"""
        return self.__user.identity

    @property
    def os(self):
        """The user's current operating system"""
        return self.__user.os

    @property
    def os_version(self):
        """The user's operating system release/version"""
        return self.__user.osversion

    @property
    def plugin_context(self):
        """If a plugin is currently active for the user, this returns their context"""
        return self.__user.context

    @property
    def comment(self):
        """Returns the user's set comment."""
        return self.__user.comment

    @property
    def ip_address(self):
        """Returns a tuple of the user's IP address in IPv6 format"""
        return self.__user.address

    @property
    def tcp_only(self):
        """Indiciates if the user is connected via a TCP only connection."""
        return bool(self.__user.tcponly)

    @property
    def idle_seconds(self):
        """Returns the number of seconds the user has been idle."""
        return self.__user.idlesecs

    def update(self, **kwargs):
        """Update a value of the user's state.kwargs

        Generally its advised to use one of the other functions (mute/deafen) to change the user's state, unless
        its isn't covered by the class' API.
        """
        for key, value in kwargs.items():
            setattr(self.__user, key, value)
        self.__server.set_user_state(self.__user)

    def send_message(self, text):
        """Send a message to the user via Mumble's chat feature"""
        return self.__server.send_user_message(self.__user.session, text)

    def mute(self):
        """Mute the user."""
        return self.update(mute=1)

    def deafen(self):
        """Deafen the user."""
        return self.update(deaf=1)

    def unmute(self):
        """Unmute the user."""
        return self.update(mute=0)

    def undeafen(self):
        """Undeafen the user."""
        return self.update(deaf=0)

    def priority_speaker(self):
        """Enable priority speaker for the user."""
        return self.update(prioritySpeaker=1)

    def remove_priority_speaker(self):
        """Remove priority speaker from the user."""
        return self.update(prioritySpeaker=0)

    def move(self, channel):
        """Move the user to the specified channel."""
        if isinstance(channel, int):
            return self.update(channel=channel)
        return self.update(channel=channel.id)

    def kick(self, reason=''):
        """Kick the user from the server"""
        return self.__server.kick_user(self.__user.session, reason)

    def ban(self, reason='', bits=128, duration=360):
        """Ban the user from the server"""
        return self.__server.add_ban(self.__user.address, reason, bits, duration)

    def serialize(self):
        """Returns the user's state in a standard ``dict``"""
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