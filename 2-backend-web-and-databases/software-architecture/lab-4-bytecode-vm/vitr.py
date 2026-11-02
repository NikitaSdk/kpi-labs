import logging

logger = logging.getLogger('virt_logger')
logging.basicConfig(level=logging.DEBUG)


def bytefunc(bytecode):
    nreg = 256
    R = [0] * nreg  # 256 реєстрів
    count = 0
    output = []  # список для збереження виведених значень

    while count < len(bytecode):
        opcode = bytecode[count]
        if opcode == 0x00:  # IDLE
            logger.debug("IDLE")
            count += 1

        elif opcode == 0x01:  # LOAD: [0x01, byte1, byte2, register]
            if count + 3 >= len(bytecode):
                logger.error("Недостатньо байтів для LOAD")
                break
            value = (bytecode[count + 1] << 8) | bytecode[count + 2]
            reg = bytecode[count + 3]
            R[reg] = value
            logger.debug(f"LOAD: R{reg} = {value}")
            count += 4

        elif opcode == 0x05:  # SUBTRACT: [0x05, reg1, reg2, dest_reg]
            if count + 3 >= len(bytecode):
                logger.error("Недостатньо байтів для SUBTRACT")
                break
            reg1 = bytecode[count + 1]
            reg2 = bytecode[count + 2]
            dest = bytecode[count + 3]
            R[dest] = R[reg1] - R[reg2]
            logger.debug(f"SUBTRACT: R{dest} = R{reg1} - R{reg2} = {R[dest]}")
            count += 4

        elif opcode == 0x03:  # PRINT: [0x03, register]
            if count + 1 >= len(bytecode):
                logger.error("Недостатньо байтів для PRINT")
                break
            reg = bytecode[count + 1]
            logger.debug(f"PRINT: R{reg} = {R[reg]}")
            output.append(R[reg])
            count += 2

        else:
            logger.error(f"Невідомий opcode: {opcode}")
            break

    return output, R


# Додаємо блок, який викликається при запуску цього файлу напряму
if __name__ == '__main__':
    # Приклад байткоду:
    # 1. IDLE
    # 2. LOAD: завантаження 0xFF00 (65280) у R0
    # 3. LOAD: завантаження 0x0003 (3) у R1
    # 4. SUBTRACT: R0 - R1 (65280 - 3 = 65277) → запис у R2
    # 5. PRINT: вивід R2
    # 6. IDLE
    sample_bytecode = [
        0x00,  # IDLE
        0x01, 0xFF, 0x00, 0x00,  # LOAD: R0 = 65280
        0x01, 0x00, 0x03, 0x01,  # LOAD: R1 = 3
        0x05, 0x00, 0x01, 0x02,  # SUBTRACT: R2 = R0 - R1 = 65277
        0x03, 0x02,  # PRINT: вивід значення з R2
        0x00  # IDLE
    ]

    output, registers = bytefunc(sample_bytecode)
    print("результат:", output)
