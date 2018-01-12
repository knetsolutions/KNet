import unittest
import KNet.lib.utils as utils


class TestUtils(unittest.TestCase):

    def test_generate_id(self):
        self.assertEqual(utils.generate_id(), 0)

    def test_generate_id_again(self):
        self.assertEqual(utils.generate_id(), 1)

    def test_reset_generate(self):
        utils.reset_id()
        self.assertEqual(utils.generate_id(), 0)

if __name__ == '__main__':
    unittest.main()
