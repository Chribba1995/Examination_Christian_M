import unittest
from chat_server import rec_msg

class TestChatServer(unittest.TestCase):
    def test_rec_msg(self):

        message_one = ''
        message_two = 'Hello World'
        first_msg_test = message_one.encode('utf-8')
        sec_msg_test = message_two.encode('utf-8')

        self.assertFalse(first_msg_test)
        self.assertTrue(sec_msg_test)


if __name__=="__main__":
    TestChatServer()