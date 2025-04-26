from src.encbit.encryption import Encryption
from src.helper.constant import Key


# noinspection PyProtectedMember
class TestEncryptionOneCube:
    # Set the test plain message.
    message = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwX"
    # Set the testing protocol.
    protocol = Encryption(message=message, cube_side_length=4)

    # Set the padded binary string.
    binary_chunk = [cube.content for cube in protocol._cubes]

    def test_current_string(self):
        assert self.protocol.get_current_binary() == "".join(self.binary_chunk)

    def test_encryption(self):
        # Test redundant keys give the same result.
        self.protocol.encrypt(key=[Key(move="right", angle=360, index=1)])
        first_content = self.protocol.get_current_binary()

        self.protocol.decrypt()

        self.protocol.encrypt(key=[Key(move="left", angle=360, index=1)])
        second_content = self.protocol.get_current_binary()

        assert first_content == second_content

    def test_decrypt(self):
        assert self.protocol.get_decrypted_str() == self.message
