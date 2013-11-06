class Channel(object):
    """
    A class to represent a Mumble channel
    """
    def __init__(self, server, channel):
        self.__server = server
        self.__channel = channel

    @property
    def id(self):
        return self.__channel.id

    @property
    def parent(self):
        if self.__channel.parent != 0:
            return self.__server.get_channel(self.__channel.parent)

    @property
    def links(self):
        return [self.__server.get_channel(channel_id) for channel_id in self.__channel.links]

    @property
    def name(self):
        return self.__channel.name

    @property
    def description(self):
        return self.__channel.description

    @property
    def temporary(self):
        return bool(self.__channel.temporary)

    @property
    def position(self):
        return self.__channel.position

    def delete(self):
        self.__server.remove_channel(self.__channel.id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.__channel, key, value)
        self.__server.set_channel_state(self.__channel)

    def send_message(self, text, tree=False):
        self.__server.send_message(self.__channel.id, tree, text)

    def serialize(self):
        return {
            'id': self.__channel.id,
            'parent': self.__channel.parent,
            'links': self.__channel.links,
            'name': self.__channel.name,
            'description': self.__channel.description,
            'temporary': self.__channel.temporary,
            'position': self.__channel.position,
        }