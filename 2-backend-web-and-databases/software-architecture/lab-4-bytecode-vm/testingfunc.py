import unittest
from virt import bytefunc


# Імпортуємо функцію з файлу vm.py

class TestVM(unittest.TestCase):
    def test_subtraction_and_print(self):
        """
        Тестова програма:
        - Завантаження у R0 числа 0xFF00 (65280)
        - Завантаження у R1 числа 0x0003 (3)
        - SUBTRACT: R0 - R1 -> записати результат у R2 (65280 - 3 = 65277)
        - PRINT: вивід значення R2
        """
        bytecode = [
            0x00,                    # IDLE
            0x01, 0xFF, 0x00, 0x00,   # LOAD: R0 = 65280
            0x01, 0x00, 0x03, 0x01,   # LOAD: R1 = 3
            0x05, 0x00, 0x01, 0x02,   # SUBTRACT: R2 = R0 - R1 = 65277
            0x03, 0x02,             # PRINT: вивід значення з R2
            0x00                     # IDLE
        ]
        output, registers = bytefunc(bytecode)
        self.assertEqual(output, [65277])
        self.assertEqual(registers[2], 65277)

if __name__ == '__main__':
    unittest.main()
