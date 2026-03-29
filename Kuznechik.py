import sys

# Размер блока алгоритма Кузнечик: 128 бит = 16 байт
BLOCK_SIZE = 16

# Таблица прямого S-преобразования
PI = [
    252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250,
    218, 35, 197, 4, 77, 233, 119, 240, 219, 147, 46,
    153, 186, 23, 54, 241, 187, 20, 205, 95, 193, 249,
    24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139,
    1, 142, 79, 5, 132, 2, 174, 227, 106, 143, 160, 6,
    11, 237, 152, 127, 212, 211, 31, 235, 52, 44, 81,
    234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206,
    204, 181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19,
    71, 156, 183, 93, 135, 21, 161, 150, 41, 16, 123,
    154, 199, 243, 145, 120, 111, 157, 158, 178, 177,
    50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198,
    128, 195, 189, 13, 87, 223, 245, 36, 169, 62, 168,
    67, 201, 215, 121, 214, 246, 124, 34, 185, 3, 224,
    15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80,
    78, 51, 10, 74, 167, 151, 96, 115, 30, 0, 98, 68,
    26, 184, 56, 130, 100, 159, 38, 65, 173, 69, 70, 146,
    39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149,
    59, 7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107,
    228, 136, 217, 231, 137, 225, 27, 131, 73, 76, 63,
    248, 254, 141, 83, 170, 144, 202, 216, 133, 97, 32,
    113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190,
    229, 108, 82, 89, 166, 116, 210, 230, 244, 180, 192,
    209, 102, 175, 194, 57, 75, 99, 182
]

# Таблица обратного S-преобразования
PI_INV = [
    165, 45, 50, 143, 14, 48, 56, 192, 84, 230, 158,
    57, 85, 126, 82, 145, 100, 3, 87, 90, 28, 96, 7,
    24, 33, 114, 168, 209, 41, 198, 164, 63, 224, 39,
    141, 12, 130, 234, 174, 180, 154, 99, 73, 229, 66,
    228, 21, 183, 200, 6, 112, 157, 65, 117, 25, 201,
    170, 252, 77, 191, 42, 115, 132, 213, 195, 175, 43,
    134, 167, 177, 178, 91, 70, 211, 159, 253, 212, 15,
    156, 47, 155, 67, 239, 217, 121, 182, 83, 127, 193,
    240, 35, 231, 37, 94, 181, 30, 162, 223, 166, 254,
    172, 34, 249, 226, 74, 188, 53, 202, 238, 120, 5,
    107, 81, 225, 89, 163, 242, 113, 86, 17, 106, 137,
    148, 101, 140, 187, 119, 60, 123, 40, 171, 210, 49,
    222, 196, 95, 204, 207, 118, 44, 184, 216, 46, 54,
    219, 105, 179, 20, 149, 190, 98, 161, 59, 22, 102,
    233, 92, 108, 109, 173, 55, 97, 75, 185, 227, 186,
    241, 160, 133, 131, 218, 71, 197, 176, 51, 250, 150,
    111, 110, 194, 246, 80, 255, 93, 169, 142, 23, 27,
    151, 125, 236, 88, 247, 31, 251, 124, 9, 13, 122,
    103, 69, 135, 220, 232, 79, 29, 78, 4, 235, 248, 243,
    62, 61, 189, 138, 136, 221, 205, 11, 19, 152, 2, 147,
    128, 144, 208, 36, 52, 203, 237, 244, 206, 153, 16,
    68, 64, 146, 58, 1, 38, 18, 26, 72, 104, 245, 129,
    139, 199, 214, 32, 10, 8, 0, 76, 215, 116
]

# Вектор коэффициентов для линейного преобразования
L_VEC = [148, 32, 133, 16, 194, 192, 1, 251,
         1, 192, 194, 16, 133, 32, 148, 1]


def xor_bytes(a, b):
    """Выполняет побайтовое XOR двух последовательностей."""
    return bytes(x ^ y for x, y in zip(a, b))


def gf_mul(a, b):
    """Умножает два байта в поле GF(2^8)."""
    res = 0
    for _ in range(8):
        if b & 1:
            res ^= a
        high_bit = a & 0x80
        a = (a << 1) & 0xFF
        if high_bit:
            a ^= 0xC3
        b >>= 1
    return res


def s_transform(data):
    """Прямое S-преобразование."""
    return bytes(PI[b] for b in data)


def s_inv_transform(data):
    """Обратное S-преобразование."""
    return bytes(PI_INV[b] for b in data)


def r_transform(state):
    """Однократное R-преобразование."""
    x = 0
    for i in range(16):
        x ^= gf_mul(state[i], L_VEC[i])
    return bytes([x]) + state[:15]


def r_inv_transform(state):
    """Обратное однократное R-преобразование."""
    x = state[0]
    result = bytearray(state[1:]) + bytearray([0])
    for i in range(15):
        x ^= gf_mul(result[i], L_VEC[i])
    result[15] = x
    return bytes(result)


def l_transform(data):
    """Прямое L-преобразование."""
    result = data
    for _ in range(16):
        result = r_transform(result)
    return result


def l_inv_transform(data):
    """Обратное L-преобразование."""
    result = data
    for _ in range(16):
        result = r_inv_transform(result)
    return result


def generate_constants():
    """Генерирует 32 константы для развёртывания ключа."""
    constants = []
    for i in range(1, 33):
        c = bytearray(16)
        c[15] = i
        constants.append(l_transform(bytes(c)))
    return constants


def f_transform(k1, k2, constant):
    """Преобразование F для генерации раундовых ключей."""
    temp = xor_bytes(k1, constant)
    temp = s_transform(temp)
    temp = l_transform(temp)
    temp = xor_bytes(temp, k2)
    return temp, k1


def expand_key(master_key):
    """Разворачивает исходный ключ в 10 раундовых ключей."""
    if len(master_key) != 32:
        raise ValueError("Ключ должен содержать 32 байта.")

    left = master_key[:16]
    right = master_key[16:]
    keys = [left, right]
    constants = generate_constants()

    for group in range(4):
        for step in range(8):
            left, right = f_transform(left, right, constants[group * 8 + step])
        keys.append(left)
        keys.append(right)

    return keys


def encrypt_block(block, round_keys):
    """Шифрует один блок длиной 16 байт."""
    state = block
    for i in range(9):
        state = xor_bytes(state, round_keys[i])
        state = s_transform(state)
        state = l_transform(state)
    state = xor_bytes(state, round_keys[9])
    return state


def decrypt_block(block, round_keys):
    """Расшифровывает один блок длиной 16 байт."""
    state = xor_bytes(block, round_keys[9])
    for i in range(8, -1, -1):
        state = l_inv_transform(state)
        state = s_inv_transform(state)
        state = xor_bytes(state, round_keys[i])
    return state


def pad_data(data):
    """Добавляет padding, только если длина данных не кратна 16 байтам."""
    if len(data) % BLOCK_SIZE == 0:
        return data
    padding_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([padding_len] * padding_len)


def unpad_data(data):
    """Удаляет padding, если он присутствует и корректен."""
    if not data:
        return data

    padding_len = data[-1]

    if padding_len < 1 or padding_len > BLOCK_SIZE:
        return data

    if len(data) < padding_len:
        return data

    if data[-padding_len:] == bytes([padding_len] * padding_len):
        return data[:-padding_len]

    return data


def read_text_file(path):
    """Читает текстовый файл целиком."""
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def read_hex_file(path):
    """Читает hex-данные из текстового файла."""
    content = read_text_file(path)
    hex_data = "".join(content.split())

    if len(hex_data) == 0:
        return b""

    if len(hex_data) % 2 != 0:
        raise ValueError("Hex-данные должны содержать чётное количество символов.")

    try:
        return bytes.fromhex(hex_data)
    except ValueError:
        raise ValueError("Файл содержит некорректные hex-данные.")


def write_hex_file(path, data):
    """Записывает данные в файл в hex-формате."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(data.hex())


def print_file_content(label, path):
    """Выводит содержимое файла в консоль."""
    content = read_text_file(path)
    print(f"{label} ({path}):")
    print(content if content else "[пустой файл]")
    print()


def encrypt_ecb(data, round_keys):
    """Шифрует данные в режиме ECB."""
    result = bytearray()
    for i in range(0, len(data), BLOCK_SIZE):
        result.extend(encrypt_block(data[i:i + BLOCK_SIZE], round_keys))
    return bytes(result)


def decrypt_ecb(data, round_keys):
    """Расшифровывает данные в режиме ECB."""
    result = bytearray()
    for i in range(0, len(data), BLOCK_SIZE):
        result.extend(decrypt_block(data[i:i + BLOCK_SIZE], round_keys))
    return bytes(result)


def encrypt_cbc(data, round_keys, iv):
    """Шифрует данные в режиме CBC."""
    if len(iv) != BLOCK_SIZE:
        raise ValueError("IV для режима CBC должен быть длиной 16 байт.")

    result = bytearray()
    previous = iv

    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        mixed = xor_bytes(block, previous)
        encrypted = encrypt_block(mixed, round_keys)
        result.extend(encrypted)
        previous = encrypted

    return bytes(result)


def decrypt_cbc(data, round_keys, iv):
    """Расшифровывает данные в режиме CBC."""
    if len(iv) != BLOCK_SIZE:
        raise ValueError("IV для режима CBC должен быть длиной 16 байт.")

    result = bytearray()
    previous = iv

    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        decrypted = decrypt_block(block, round_keys)
        plain = xor_bytes(decrypted, previous)
        result.extend(plain)
        previous = block

    return bytes(result)


def encrypt_file(input_path, output_path, key_hex, cipher_mode, iv_hex=None):
    """Шифрует содержимое входного файла."""
    print_file_content("Содержимое входного файла", input_path)

    key = bytes.fromhex(key_hex)
    round_keys = expand_key(key)

    data = read_hex_file(input_path)
    print("Входные данные после чтения как hex:")
    print(data.hex() if data else "[пусто]")
    print()

    data = pad_data(data)

    if cipher_mode == "ecb":
        result = encrypt_ecb(data, round_keys)
    elif cipher_mode == "cbc":
        if iv_hex is None:
            raise ValueError("Для режима CBC необходимо указать IV.")
        iv = bytes.fromhex(iv_hex)
        result = encrypt_cbc(data, round_keys, iv)
    else:
        raise ValueError("Неподдерживаемый режим шифрования.")

    write_hex_file(output_path, result)
    print_file_content("Содержимое выходного файла", output_path)


def decrypt_file(input_path, output_path, key_hex, cipher_mode, iv_hex=None):
    """Расшифровывает содержимое входного файла."""
    print_file_content("Содержимое входного файла", input_path)

    key = bytes.fromhex(key_hex)
    round_keys = expand_key(key)

    data = read_hex_file(input_path)
    print("Входные данные после чтения как hex:")
    print(data.hex() if data else "[пусто]")
    print()

    if len(data) % BLOCK_SIZE != 0:
        raise ValueError("Длина зашифрованных данных должна быть кратна 16 байтам.")

    if cipher_mode == "ecb":
        result = decrypt_ecb(data, round_keys)
    elif cipher_mode == "cbc":
        if iv_hex is None:
            raise ValueError("Для режима CBC необходимо указать IV.")
        iv = bytes.fromhex(iv_hex)
        result = decrypt_cbc(data, round_keys, iv)
    else:
        raise ValueError("Неподдерживаемый режим шифрования.")

    result = unpad_data(result)

    write_hex_file(output_path, result)
    print_file_content("Содержимое выходного файла", output_path)


def print_usage():
    """Печатает справку по запуску программы."""
    print("Использование:")
    print("  python kuznechik.py encrypt ecb <input_file> <output_file> <key_hex>")
    print("  python kuznechik.py decrypt ecb <input_file> <output_file> <key_hex>")
    print()
    print("  python kuznechik.py encrypt cbc <input_file> <output_file> <key_hex> <iv_hex>")
    print("  python kuznechik.py decrypt cbc <input_file> <output_file> <key_hex> <iv_hex>")
    print()
    print("Где:")
    print("  encrypt / decrypt - операция")
    print("  ecb / cbc         - режим шифрования")
    print("  input_file        - входной файл")
    print("  output_file       - выходной файл")
    print("  key_hex           - ключ длиной 64 hex-символа")
    print("  iv_hex            - IV для CBC длиной 32 hex-символа")


def main():
    """Точка входа в программу."""
    if len(sys.argv) not in (6, 7):
        print("Ошибка: неверное количество аргументов.")
        print_usage()
        return

    operation = sys.argv[1].lower()
    cipher_mode = sys.argv[2].lower()
    input_file = sys.argv[3]
    output_file = sys.argv[4]
    key_hex = sys.argv[5].strip()
    iv_hex = sys.argv[6].strip() if len(sys.argv) == 7 else None

    if operation not in ("encrypt", "decrypt"):
        print("Ошибка: операция должна быть 'encrypt' или 'decrypt'.")
        print_usage()
        return

    if cipher_mode not in ("ecb", "cbc"):
        print("Ошибка: режим должен быть 'ecb' или 'cbc'.")
        print_usage()
        return

    if len(key_hex) != 64:
        print("Ошибка: ключ должен содержать 64 hex-символа.")
        return

    try:
        bytes.fromhex(key_hex)
    except ValueError:
        print("Ошибка: ключ должен быть в корректном hex-формате.")
        return

    if cipher_mode == "cbc":
        if iv_hex is None:
            print("Ошибка: для режима CBC необходимо указать IV.")
            return
        if len(iv_hex) != 32:
            print("Ошибка: IV для CBC должен содержать 32 hex-символа.")
            return
        try:
            bytes.fromhex(iv_hex)
        except ValueError:
            print("Ошибка: IV должен быть в корректном hex-формате.")
            return

    if cipher_mode == "ecb" and iv_hex is not None:
        print("Ошибка: для режима ECB IV указывать не нужно.")
        return

    try:
        if operation == "encrypt":
            encrypt_file(input_file, output_file, key_hex, cipher_mode, iv_hex)
            print("Файл успешно зашифрован.")
        else:
            decrypt_file(input_file, output_file, key_hex, cipher_mode, iv_hex)
            print("Файл успешно расшифрован.")
    except Exception as e:
        print(f"Ошибка при выполнении программы: {e}")


if __name__ == "__main__":
    main()