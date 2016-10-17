from myhdl import *
from IDEA import *
import unittest

class TestIDEA(unittest.TestCase):

	def encrypt1(self):
		plaintext = modbv(0x100020003)[64:]
		key = modbv(0x10002000300040005000600070008)[128:]
		cipher = encrypt(plaintext, create_subkeys(key))
		self.assertEqual(cipher, 0x11fbed2b01986de5L)

	def encrypt2(self):
		plaintext = modbv(0x05320a6414c819fa)[64:]
		key = modbv(0x006400c8012c019001f4025802bc0320)[128:]
		cipher = encrypt(plaintext, create_subkeys(key))
		self.assertEqual(cipher, 0x65be87e7a2538aedL)

	def decrypt1(self):
		plaintext = modbv(0x100020003)[64:]
		key = modbv(0x10002000300040005000600070008)[128:]
		cipher = encrypt(plaintext, create_subkeys(key))
		uncipher = encrypt(cipher, create_subkeys(key, encrypt=False), verbose=True)
		self.assertEqual(plaintext, uncipher)

if __name__ == '__main__':
	unittest.main()
