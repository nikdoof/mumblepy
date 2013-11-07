import unittest
import mumble
import Ice


class ChannelTests(unittest.TestCase):

    def setUp(self):
        self.meta = mumble.Meta('test')
        self.server = self.meta.get_server(1)
        self.root_channel = self.server.get_channel(0)
        self.link_channel = self.server.add_channel('Link Test')

    def tearDown(self):
        for chan in self.server.get_channels():
            if chan.id != 0:
                chan.delete()

    def testChannelCreateDelete(self):
        chan = self.server.add_channel('deleteTest')
        self.assertTrue(chan.delete())

    def testRootMessage(self):
        self.assertEqual(self.root_channel.send_message('Test Message'), True)

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
        chan = self.server.add_channel('channelSetting', 0)
        self.assertEqual(chan.name, 'channelSetting')
        chan.update(name='channelSetting1')
        self.assertEqual(chan.name, 'channelSetting1')

    def testChannelLinking(self):
        chan = self.server.add_channel('Link 2')
        chan.link(self.link_channel)
        self.assertEqual(chan.links[0].id, self.link_channel.id)
