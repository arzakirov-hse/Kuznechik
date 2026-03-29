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
    """Побитовое XOR двух байтовых последовательностей одинаковой длины."""
    return bytes(x ^ y for x, y in zip(a, b))


def gf_mul(a, b):
    """Умножение двух байтов в поле GF(2^8) с модулем x^8 + x^7 + x^6 + x + 1."""
    res = 0
    for _ in range(8):
        if b & 1:
            res ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0xC3
        b >>= 1
    return res


def s_transform(data):
    """Прямое S-преобразование: замена каждого байта по таблице PI."""
    return bytes(PI[b] for b in data)


def s_inv_transform(data):
    """Обратное S-преобразование: замена каждого байта по таблице PI_INV."""
    return bytes(PI_INV[b] for b in data)


def r_transform(state):
    """Однократное R-преобразование для 16-байтного состояния."""
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
    """Прямое L-преобразование: 16 последовательных R-преобразований."""
    result = data
    for _ in range(16):
        result = r_transform(result)
    return result


def l_inv_transform(data):
    """Обратное L-преобразование: 16 обратных R-преобразований."""
    result = data
    for _ in range(16):
        result = r_inv_transform(result)
    return result


def generate_constants():
    """Генерация 32 итерационных констант для развёртывания ключа."""
    constants = []
    for i in range(1, 33):
        c = bytearray(16)
        c[15] = i
        constants.append(l_transform(bytes(c)))
    return constants


def f_transform(k1, k2, c):
    """Преобразование F в алгоритме генерации раундовых ключей."""
    temp = xor_bytes(k1, c)
    temp = s_transform(temp)
    temp = l_transform(temp)
    temp = xor_bytes(temp, k2)
    return temp, k1


def expand_key(master_key):
    """Генерация 10 раундовых ключей из исходного 256-битного ключа."""
    if len(master_key) != 32:
        raise ValueError("Ключ должен содержать 32 байта (64 hex-символа).")

    k1 = master_key[:16]
    k2 = master_key[16:]
    round_keys = [k1, k2]

    constants = generate_constants()

    for i in range(4):
        for j in range(8):
            k1, k2 = f_transform(k1, k2, constants[i * 8 + j])
        round_keys.append(k1)
        round_keys.append(k2)

    return round_keys


def encrypt_block(block, round_keys):
    """Шифрование одного 16-байтного блока по алгоритму Кузнечик."""
    if len(block) != BLOCK_SIZE:
        raise ValueError("Размер блока для шифрования должен быть 16 байт.")

    state = block
    for i in range(9):
        state = xor_bytes(state, round_keys[i])
        state = s_transform(state)
        state = l_transform(state)
    state = xor_bytes(state, round_keys[9])
    return state


def decrypt_block(block, round_keys):
    """Расшифрование одного 16-байтного блока по алгоритму Кузнечик."""
    if len(block) != BLOCK_SIZE:
        raise ValueError("Размер блока для расшифрования должен быть 16 байт.")

    state = xor_bytes(block, round_keys[9])
    for i in range(8, -1, -1):
        state = l_inv_transform(state)
        state = s_inv_transform(state)
        state = xor_bytes(state, round_keys[i])
    return state


def pad_data(data):
    """Добавление PKCS#7 padding, только если длина данных не кратна 16 байтам."""
    if len(data) % BLOCK_SIZE == 0:
        return data
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)


def unpad_data(data):
    """Удаление PKCS#7 padding, если он присутствует и корректен."""
    if not data:
        return data

    pad_len = data[-1]

    if pad_len < 1 or pad_len > BLOCK_SIZE:
        return data

    if len(data) < pad_len:
        return data

    if data[-pad_len:] == bytes([pad_len] * pad_len):
        return data[:-pad_len]

    return data


def read_text_file(path):
    """Чтение исходного текстового содержимого файла без преобразований."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_hex_file(path):
    """Чтение текстового файла с hex-данными и преобразование их в байты."""
    content = read_text_file(path)
    hex_data = "".join(content.split())

    if len(hex_data) == 0:
        return b""

    if len(hex_data) % 2 != 0:
        raise ValueError("Hex-данные в файле должны содержать чётное число символов.")

    try:
        return bytes.fromhex(hex_data)
    except ValueError:
        raise ValueError("Файл содержит некорректные шестнадцатеричные данные.")


def write_hex_file(path, data):
    """Запись байтовых данных в текстовый файл в виде hex-строки."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(data.hex())


def print_file_content(label, path):
    """Вывод содержимого текстового файла в консоль."""
    content = read_text_file(path)
    print(f"{label} ({path}):")
    print(content if content else "[пустой файл]")
    print()


def encrypt_file(input_path, output_path, key_hex):
    """Чтение hex-данных из файла, их шифрование и запись результата в hex-формате."""
    print_file_content("Содержимое входного файла", input_path)

    key = bytes.fromhex(key_hex)
    round_keys = expand_key(key)

    data = read_hex_file(input_path)
    print("Входные данные после чтения как hex:")
    print(data.hex() if data else "[пусто]")
    print()

    data = pad_data(data)

    result = bytearray()
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        result.extend(encrypt_block(block, round_keys))

    write_hex_file(output_path, bytes(result))

    print_file_content("Содержимое выходного файла", output_path)


def decrypt_file(input_path, output_path, key_hex):
    """Чтение hex-шифртекста из файла, его расшифрование и запись результата в hex-формате."""
    print_file_content("Содержимое входного файла", input_path)

    key = bytes.fromhex(key_hex)
    round_keys = expand_key(key)

    data = read_hex_file(input_path)
    print("Входные данные после чтения как hex:")
    print(data.hex() if data else "[пусто]")
    print()

    if len(data) % BLOCK_SIZE != 0:
        raise ValueError("Длина зашифрованных данных должна быть кратна 16 байтам.")

    result = bytearray()
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        result.extend(decrypt_block(block, round_keys))

    result = unpad_data(bytes(result))
    write_hex_file(output_path, result)

    print_file_content("Содержимое выходного файла", output_path)


def print_usage():
    """Вывод справки по использованию программы."""
    print("Использование:")
    print("  python kuznechik.py encrypt <input_file> <output_file> <key_hex>")
    print("  python kuznechik.py decrypt <input_file> <output_file> <key_hex>")
    print()
    print("Файлы input/output должны содержать данные в шестнадцатеричном формате (hex).")
    print("Их можно открывать и редактировать в обычном Блокноте.")


def main():
    """Точка входа: разбор аргументов командной строки и запуск нужного режима."""
    if len(sys.argv) != 5:
        print("Ошибка: неверное количество аргументов.")
        print_usage()
        return

    mode = sys.argv[1].lower()
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    key_hex = sys.argv[4].strip()

    if len(key_hex) != 64:
        print("Ошибка: ключ должен содержать 64 hex-символа.")
        return

    try:
        bytes.fromhex(key_hex)
    except ValueError:
        print("Ошибка: ключ должен быть в корректном hex-формате.")
        return

    try:
        if mode == "encrypt":
            encrypt_file(input_file, output_file, key_hex)
            print("Файл успешно зашифрован.")
        elif mode == "decrypt":
            decrypt_file(input_file, output_file, key_hex)
            print("Файл успешно расшифрован.")
        else:
            print("Ошибка: режим должен быть 'encrypt' или 'decrypt'.")
            print_usage()
    except Exception as e:
        print(f"Ошибка при выполнении программы: {e}")


if __name__ == "__main__":
    main()