class ACL(object):
    """
    ACL entry for a Channel.
    """
    def __init__(self, channel, acl):
        self.__channel = channel
        self.__acl = acl

    @property
    def apply_here(self):
        """Indiciates if the ACL applies to the current channel"""
        return bool(self.__acl.applyHere)

    @property
    def apply_subs(self):
        """Indicates if the ACL applies to sub channels"""
        return bool(self.__acl.applySubs)

    @property
    def inherited(self):
        """Indiciates if the ACL is inherited from a parent channel"""
        return bool(self.__acl.inherited)

    @property
    def user(self):
        """Returns the User ID this ACL applies to"""
        if self.__acl.userid != -1:
            return self.__acl.userid

    @property
    def group(self):
        """Returns the group this ACL applies to"""
        return self.__acl.group

    @property
    def allow(self):
        """Returns a bitmask of permissions allowed by this ACL"""
        return self.__acl.allow

    @property
    def deny(self):
        """Returns a bitmask of permissions denied by this ACL"""
        return self.__acl.deny


class Group(object):
    def __init__(self, channel, group):
        self.__channel = channel
        self.__group = group

    @property
    def name(self):
        """Name of the group"""
        return self.__group.name

    @property
    def inherited(self):
        """Indiciates if the group is inherited from a parent channel."""
        return bool(self.__group.inherited)

    @property
    def inheritable(self):
        """Indiciates if the group is inherited by sub channels."""
        return bool(self.__group.inheritable)

    @property
    def members(self):
        """List of User IDs that are members of the group"""
        return self.__group.members


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
        if self.__channel.parent != -1:
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

    def get_acls(self):
        """Returns the list of ACLs for this channel."""
        acls = []
        for acl in self.__server.get_acls(self.__channel.id):
            acls.append(ACL(self, acl))
        return acls

    def get_groups(self):
        """Returns a list of groups for this channel."""
        groups = []
        for group in self.__server.get_groups(self.__channel.id):
            groups.append(Group(self, group))
        return groups

    def delete(self):
        """Remove the channel from Mumble."""
        self.__server.remove_channel(self.__channel.id)
        return True

    def update(self, **kwargs):
        """Update a channel property on the Mumble server."""
        for key, value in kwargs.items():
            setattr(self.__channel, key, value)
        self.__server.set_channel_state(self.__channel)

    def send_message(self, text, tree=False):
        """Send a message to the channel."""
        return self.__server.send_channel_message(self.__channel.id, text, tree)

    def link(self, channel):
        """Link this channel to another channel."""
        current_links = self.__channel.links
        current_links.append(channel.id)
        self.update(links=current_links)

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