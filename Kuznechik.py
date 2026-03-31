# -*- coding: utf-8 -*-
import sys

BLOCK_SIZE = 16  # размер блока в байтах (128 бит)

# ==========================
# S-блоки и таблицы
# ==========================
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

L_VEC = [148, 32, 133, 16, 194, 192, 1, 251,
         1, 192, 194, 16, 133, 32, 148, 1]


# ==========================
# Базовые функции
# ==========================
def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def gf_mul(a, b):
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
    return bytes(PI[b] for b in data)


def s_inv_transform(data):
    return bytes(PI_INV[b] for b in data)


def r_transform(state):
    x = 0
    for i in range(16):
        x ^= gf_mul(state[i], L_VEC[i])
    return bytes([x]) + state[:15]


def r_inv_transform(state):
    x = state[0]
    result = bytearray(state[1:]) + bytearray([0])
    for i in range(15):
        x ^= gf_mul(result[i], L_VEC[i])
    result[15] = x
    return bytes(result)


def l_transform(data):
    result = data
    for _ in range(16):
        result = r_transform(result)
    return result


def l_inv_transform(data):
    result = data
    for _ in range(16):
        result = r_inv_transform(result)
    return result


def generate_constants():
    constants = []
    for i in range(1, 33):
        c = bytearray(16)
        c[15] = i
        constants.append(l_transform(bytes(c)))
    return constants


def f_transform(k1, k2, constant):
    temp = xor_bytes(k1, constant)
    temp = s_transform(temp)
    temp = l_transform(temp)
    temp = xor_bytes(temp, k2)
    return temp, k1


def expand_key(master_key):
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
    state = block
    for i in range(9):
        state = xor_bytes(state, round_keys[i])
        state = s_transform(state)
        state = l_transform(state)
    state = xor_bytes(state, round_keys[9])
    return state


def decrypt_block(block, round_keys):
    state = xor_bytes(block, round_keys[9])
    for i in range(8, -1, -1):
        state = l_inv_transform(state)
        state = s_inv_transform(state)
        state = xor_bytes(state, round_keys[i])
    return state


def pad_data(data):
    if len(data) % BLOCK_SIZE == 0:
        return data
    padding_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([padding_len] * padding_len)


def unpad_data(data):
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


# ==========================
# Работа с файлами
# ==========================
def read_binary_file(path):
    """Читает файл как сырые байты"""
    with open(path, "rb") as file:
        return file.read()


def write_binary_file(path, data):
    """Записывает сырые байты в файл"""
    with open(path, "wb") as file:
        file.write(data)


def bytes_to_text(data):
    return data.decode("utf-8", errors="replace")


def print_bytes_preview(label, data):
    print(f"{label}:")
    print("Текст:")
    print(bytes_to_text(data) if data else "[пустой файл]")
    print("Hex:")
    print(data.hex() if data else "[пустой файл]")
    print()


# ==========================
# Режимы шифрования
# ==========================
def encrypt_ecb(data, round_keys):
    result = bytearray()
    for i in range(0, len(data), BLOCK_SIZE):
        result.extend(encrypt_block(data[i:i + BLOCK_SIZE], round_keys))
    return bytes(result)


def decrypt_ecb(data, round_keys):
    result = bytearray()
    for i in range(0, len(data), BLOCK_SIZE):
        result.extend(decrypt_block(data[i:i + BLOCK_SIZE], round_keys))
    return bytes(result)


def encrypt_cbc(data, round_keys, iv):
    if len(iv) != BLOCK_SIZE:
        raise ValueError("IV должен быть длиной 16 байт.")
    result = bytearray()
    prev = iv
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        encrypted = encrypt_block(xor_bytes(block, prev), round_keys)
        result.extend(encrypted)
        prev = encrypted
    return bytes(result)


def decrypt_cbc(data, round_keys, iv):
    if len(iv) != BLOCK_SIZE:
        raise ValueError("IV должен быть длиной 16 байт.")
    result = bytearray()
    prev = iv
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        decrypted = xor_bytes(decrypt_block(block, round_keys), prev)
        result.extend(decrypted)
        prev = block
    return bytes(result)


# ==========================
# Основные функции
# ==========================
def encrypt_file(input_path, output_path, key_hex, cipher_mode, iv_hex=None):
    # Читаем входной файл как бинарные данные
    data = read_binary_file(input_path)
    print_bytes_preview("Исходные данные", data)

    key = bytes.fromhex(key_hex)
    round_keys = expand_key(key)
    data = pad_data(data)

    if cipher_mode == "ecb":
        result = encrypt_ecb(data, round_keys)
    elif cipher_mode == "cbc":
        if iv_hex is None:
            raise ValueError("IV обязателен для CBC.")
        iv = bytes.fromhex(iv_hex)
        result = encrypt_cbc(data, round_keys, iv)
    else:
        raise ValueError("Неподдерживаемый режим.")

    print_bytes_preview("Зашифрованные данные", result)
    # Записываем результат как бинарные данные
    write_binary_file(output_path, result)


def decrypt_file(input_path, output_path, key_hex, cipher_mode, iv_hex=None):
    # Читаем входной файл как бинарные данные
    data = read_binary_file(input_path)
    print_bytes_preview("Исходные данные (зашифрованные)", data)

    key = bytes.fromhex(key_hex)
    round_keys = expand_key(key)

    if len(data) % BLOCK_SIZE != 0:
        raise ValueError("Длина зашифрованных данных должна быть кратна 16 байтам.")

    if cipher_mode == "ecb":
        result = decrypt_ecb(data, round_keys)
    elif cipher_mode == "cbc":
        if iv_hex is None:
            raise ValueError("IV обязателен для CBC.")
        iv = bytes.fromhex(iv_hex)
        result = decrypt_cbc(data, round_keys, iv)
    else:
        raise ValueError("Неподдерживаемый режим.")

    result = unpad_data(result)
    print_bytes_preview("Расшифрованные данные", result)
    # Записываем результат как бинарные данные
    write_binary_file(output_path, result)


def print_usage():
    print("Использование:")
    print("  python kuznechik.py encrypt ecb <input_file> <output_file> <key_hex>")
    print("  python kuznechik.py decrypt ecb <input_file> <output_file> <key_hex>")
    print()
    print("  python kuznechik.py encrypt cbc <input_file> <output_file> <key_hex> <iv_hex>")
    print("  python kuznechik.py decrypt cbc <input_file> <output_file> <key_hex> <iv_hex>")
    print()
    print("Примечание: все файлы читаются и записываются как бинарные данные.")


def main():
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

    if operation not in ("encrypt", "decrypt") or cipher_mode not in ("ecb", "cbc"):
        print_usage()
        return

    if len(key_hex) != 64:
        print("Ключ должен быть 64 hex-символа.")
        return
    try:
        bytes.fromhex(key_hex)
    except:
        print("Некорректный hex ключ.")
        return

    if cipher_mode == "cbc":
        if iv_hex is None or len(iv_hex) != 32:
            print("IV обязателен и должен быть 32 hex-символа.")
            return
        try:
            bytes.fromhex(iv_hex)
        except:
            print("Некорректный IV.")
            return

    try:
        if operation == "encrypt":
            encrypt_file(input_file, output_file, key_hex, cipher_mode, iv_hex)
            print("Файл зашифрован.")
        else:
            decrypt_file(input_file, output_file, key_hex, cipher_mode, iv_hex)
            print("Файл расшифрован.")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()