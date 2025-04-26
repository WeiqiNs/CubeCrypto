from src.encitem.encryption import Encryption
from src.helper.constant import Key


class TestEncryption:
    # Set the test plain message and the encryption protocol.
    message = "Hello World"
    protocol = Encryption(message=message, cube_side_length=3)

    def test_process_string(self):
        assert self.protocol.process_string(self.message) == "helloworld"

    def test_current_string(self):
        assert self.protocol.get_current_content()[:10] == \
            self.protocol.process_string(self.message)

    def test_encryption(self):
        self.protocol.encrypt(key=[Key(move="right", angle=360, index=1)])

        assert self.protocol.get_current_content()[1:11] == \
            self.protocol.process_string(self.message)

    def test_decrypt(self):
        assert self.protocol.get_decrypted_str() == \
            self.protocol.process_string(self.message)
