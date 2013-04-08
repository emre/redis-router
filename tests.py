# -*- coding: utf8 -*-

import unittest
import os
import ketama

from redis_router.router import Router


class RouterTests(unittest.TestCase):

    def setUp(self):
        # localhost:6379 and localhost:6390 must be accessible redis instances for testing.
        self.valid_list_file = os.tmpnam()
        self.valid_list = file(self.valid_list_file, "w")
        self.valid_list.write("127.0.0.1:6379\t600\n")
        self.valid_list.write("127.0.0.1:6380\t400\n")
        self.valid_list.flush()

        self.invalid_list_file = os.tmpnam()
        self.invalid_list = file(self.invalid_list_file, "w")
        self.invalid_list.write("127.0.0.1:11211 600\n")
        self.invalid_list.write("127.0.0.1:11212 foo\n")
        self.invalid_list.flush()

        self.router = Router(self.valid_list_file)

    def tearDown(self):
        self.valid_list.close()
        os.unlink(self.valid_list_file)

        self.invalid_list.close()
        os.unlink(self.invalid_list_file)

    def test_valid_configuration(self):
        r = Router(self.valid_list_file)
        self.assertEqual(isinstance(r, Router), True)

    def test_invalid_configuration(self):
        self.assertRaises(ketama.KetamaError, Router, self.invalid_list_file)

    def test_continuum(self):
        cont = Router(self.valid_list_file).continuum
        self.assertEqual(type(cont), ketama.Continuum)

    def test_invalid_null(self):
        self.assertRaises(ketama.KetamaError, Router, "/dev/null")

    def test_hashing(self):
        router = Router(self.valid_list_file)
        router.set('forge', 13)
        router.set("spawning_pool", 18)

        key_hash, connection_uri = router.continuum.get_server('forge')
        self.assertEqual(key_hash, 4113771093)
        self.assertEqual(connection_uri, '127.0.0.1:6379')

        key_hash, connection_uri = router.continuum.get_server('spawning_pool')
        self.assertEqual(key_hash, 1434709819)
        self.assertEqual(connection_uri, '127.0.0.1:6380')

    def test_sinter(self):
        self.router.sadd('X', 'a', 'b', 'c')
        self.router.sadd('Y', 'a', 'd', 'e')

        self.assertEqual(self.router.sinter('X', 'Y'), set(['a', ]))

    def test_sinterstore(self):
        self.router.sadd('X1', 'a', 'b', 'c')
        self.router.sadd('Y1', 'a', 'd', 'e')
        self.router.sinterstore('Z1', 'X1', 'Y1')

        self.assertEqual(self.router.smembers('Z1'), set(['a', ]))

    def test_sunion(self):
        self.router.sadd('T1', 'a', 'b', 'c')
        self.router.sadd('M1', 'a', 'd', 'e')

        self.assertEqual(self.router.sunion('T1', 'M1'), set(['a', 'b', 'c', 'd', 'e']))

    def test_sunionstore(self):
        self.router.sadd('T2', 'a', 'b', 'c')
        self.router.sadd('M2', 'a', 'd', 'e')

        self.router.sunionstore('Z2', 'T2', 'M2')

        self.assertEqual(self.router.smembers('Z2'), set(['a', 'b', 'c', 'd', 'e']))

    def test_dbsize(self):
        self.router.flush_all()

        for index in xrange(1, 10):
            self.router.set('data{0}'.format(index), '1')

        self.assertEqual(self.router.dbsize(), 9)

    def test_flush_all(self):
        for index in xrange(1, 10):
            self.router.set('random_data{0}'.format(index), '1')

        self.router.flush_all()

        self.assertEqual(self.router.dbsize(), 0)








