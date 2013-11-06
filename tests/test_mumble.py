import unittest
import mumble
import Ice


class ChannelTests(unittest.TestCase):

    def setUp(self):
        self.meta = mumble.Meta('test')
        self.server = self.meta.get_server(1)

    def tearDown(self):
        for chan in self.server.get_channels():
            if chan.id != 0:
                chan.delete()

    def testGetRoot(self):
        chan = self.server.get_channel(0)
        self.assertEqual(chan.id, 0)
        self.assertEqual(chan.name, 'Root')
        self.assertEqual(chan.parent, None)
        self.assertEqual(chan.description, '')
        self.assertEqual(chan.links, [])
        self.assertEqual(chan.position, 0)
        self.assertEqual(chan.temporary, False)

    def testChannelSetting(self):
        channel_id = self.server.add_channel('channelSetting', 0)
        chan = self.server.get_channel(channel_id)
        self.assertEqual(chan.name, 'channelSetting')
        chan.update(name='channelSetting1')
        self.assertEqual(chan.name, 'channelSetting1')

