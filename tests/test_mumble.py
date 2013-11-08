# coding=utf-8
import unittest
import mumble


class ServerTests(unittest.TestCase):

    def setUp(self):
        self.meta = mumble.Meta('test')
        self.server = self.meta.get_server(1)

    def tearDown(self):
        for chan in self.server.get_channels():
            if chan.id != 0:
                try:
                    chan.delete()
                except:
                    pass

    def testGetAllConf(self):
        self.assertNotEqual(self.server.get_all_conf(), None)

    def testChannelByName(self):
        unicode_channel = self.server.add_channel(u'Têｓｔ Cɦａԉｎｅɭ 1')
        self.assertEqual(self.server.get_channel_by_name('Root').id, 0)
        self.assertEqual(self.server.get_channel_by_name(u'Têｓｔ Cɦａԉｎｅɭ 1').id, unicode_channel.id)
        self.assertEqual(self.server.get_channel_by_name('invalidChannelName'), None)

    def testInvalidChannelByName(self):
        self.assertEqual(self.server.get_channel_by_name(None), None)

    def testInvalidGetChannel(self):
        self.assertEqual(self.server.get_channel(-1), None)
        self.assertEqual(self.server.get_channel(232302323), None)
        self.assertEqual(self.server.get_channel(None), None)

    def testGetChannels(self):
        self.assertEqual(len(self.server.get_channels()), 1)

    def testAddChannel(self):
        self.assertNotEqual(self.server.add_channel('Test Channel 1'), None)
        self.assertNotEqual(self.server.add_channel(u'Têｓｔ Cɦａԉｎｅɭ 2'), None)

    def testInvalidAddChannel(self):
        self.assertEqual(self.server.add_channel(None), None)

    def testRemoveChannel(self):
        chan_id = self.server.add_channel('Removal').id
        self.server.remove_channel(chan_id)
        self.assertEqual(self.server.get_channel(chan_id), None)


class ChannelTests(unittest.TestCase):

    def setUp(self):
        self.meta = mumble.Meta('test')
        self.server = self.meta.get_server(1)
        self.root_channel = self.server.get_channel(0)
        self.link_channel = self.server.add_channel('Link Test')

    def tearDown(self):
        for chan in self.server.get_channels():
            if chan.id != 0:
                try:
                    chan.delete()
                except:
                    pass

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

    def testChannelParent(self):
        chan = self.server.add_channel('Parent Test')
        self.assertEqual(chan.parent.id, 0)
        chan2 = self.server.add_channel('Parent 2', parent=chan.id)
        self.assertEqual(chan2.parent.id, chan.id)

    def testSerailze(self):
        self.assertNotEqual(self.root_channel.serialize(), None)

    def testACL(self):
        self.assertEquals(len(self.root_channel.get_acls()), 3)

    def testGroup(self):
        self.assertEquals(len(self.root_channel.get_groups()), 1)
