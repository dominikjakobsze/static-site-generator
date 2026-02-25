import unittest

from block_markdown import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_1(self):
        result = block_to_block_type("# This is a New York Times heading")
        self.assertEqual(result, BlockType.HEADING)

    def test_2(self):
        result = block_to_block_type("#This is a New York Times heading")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_3(self):
        result = block_to_block_type("```\n<p>Hello World Friend</p>\n```")
        self.assertEqual(result, BlockType.CODE)

    def test_4(self):
        result = block_to_block_type("```\n<p>Hello World Friend</p>\n``")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_5(self):
        result = block_to_block_type(">Pierwsza linia\n> Druga linia\n>Trzecia linia")
        self.assertEqual(result, BlockType.QUOTE)

    def test_6(self):
        result = block_to_block_type(">Pierwsza linia\n Druga linia\n>Trzecia linia")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_7(self):
        result = block_to_block_type("- Pierwszy punkt\n- Drugi punkt\n- Trzeci punkt")
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_8(self):
        result = block_to_block_type("- Pierwszy punkt\n Drugi punkt\n- Trzeci punkt")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_9(self):
        result = block_to_block_type("1. Kupić miód\n2. Zjeść miód\n3. Odpocząć")
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_10(self):
        result = block_to_block_type("1. Kupić miód\nZjeść miód\n3. Odpocząć")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_11(self):
        result = block_to_block_type("1. Kupić miód\n3. Zjeść miód\n2. Odpocząć")
        self.assertEqual(result, BlockType.PARAGRAPH)


if __name__ == '__main__':
    unittest.main()
