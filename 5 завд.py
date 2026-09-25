path_to_file = r'C:\My Files\NULP\Programming tech\LAB3\bmp_8.bmp'

print("ПАРСИНГ ЗАГОЛОВКУ BMP-ФАЙЛУ (Варіант 8)")
print(f"Файл: {path_to_file}\n")

try:
    with open(path_to_file, 'rb') as f:
        data = f.read(54)

    print("ЗАГОЛОВОК ФАЙЛУ (BitMapFileHeader)\n")

    Type = data[0:2]
    type_str = Type.decode('ascii', errors='ignore')
    print(f"Type           = {Type.hex(':')} = '{type_str}'")

    Size = data[2:6]
    size_value = int.from_bytes(Size, byteorder='little')
    print(f"Size           = {Size.hex(':')} = {size_value} байт")

    Reserved1 = data[6:8]
    res1_value = int.from_bytes(Reserved1, byteorder='little')
    print(f"Reserved1      = {Reserved1.hex(':')} = {res1_value}")

    Reserved2 = data[8:10]
    res2_value = int.from_bytes(Reserved2, byteorder='little')
    print(f"Reserved2      = {Reserved2.hex(':')} = {res2_value}")

    OffsetBits = data[10:14]
    offset_value = int.from_bytes(OffsetBits, byteorder='little')
    print(f"OffsetBits     = {OffsetBits.hex(':')} = {offset_value} байт")

    print("\n" + "-" * 70)
    print("ІНФОРМАЦІЙНИЙ ЗАГОЛОВОК (BitMapInfoHeader)")

    InfoSize = data[14:18]
    info_size_value = int.from_bytes(InfoSize, byteorder='little')
    print(f"Size           = {InfoSize.hex(':')} = {info_size_value} байт")

    Width = data[18:22]
    width_value = int.from_bytes(Width, byteorder='little')
    print(f"Width          = {Width.hex(':')} = {width_value} пікселів")

    Height = data[22:26]
    height_value = int.from_bytes(Height, byteorder='little')
    print(f"Height         = {Height.hex(':')} = {height_value} пікселів")

    Planes = data[26:28]
    planes_value = int.from_bytes(Planes, byteorder='little')
    print(f"Planes         = {Planes.hex(':')} = {planes_value}")

    BitCount = data[28:30]
    bitcount_value = int.from_bytes(BitCount, byteorder='little')
    print(f"BitCount       = {BitCount.hex(':')} = {bitcount_value} біт/піксель")

    Compression = data[30:34]
    compression_value = int.from_bytes(Compression, byteorder='little')
    compression_types = {0: "Немає", 1: "8-bit RLE", 2: "4-bit RLE"}
    compression_str = compression_types.get(compression_value, "Невідомо")
    print(f"Compression    = {Compression.hex(':')} = {compression_value} ({compression_str})")

    SizeImage = data[34:38]
    size_image_value = int.from_bytes(SizeImage, byteorder='little')
    print(f"SizeImage      = {SizeImage.hex(':')} = {size_image_value} байт")

    XpelsPerMeter = data[38:42]
    xpels_value = int.from_bytes(XpelsPerMeter, byteorder='little')
    print(f"XpelsPerMeter  = {XpelsPerMeter.hex(':')} = {xpels_value} пікс/м")

    YpelsPerMeter = data[42:46]
    ypels_value = int.from_bytes(YpelsPerMeter, byteorder='little')
    print(f"YpelsPerMeter  = {YpelsPerMeter.hex(':')} = {ypels_value} пікс/м")

    ColorsUsed = data[46:50]
    colors_used_value = int.from_bytes(ColorsUsed, byteorder='little')
    print(f"ColorsUsed     = {ColorsUsed.hex(':')} = {colors_used_value}")

    ColorsImportant = data[50:54]
    colors_imp_value = int.from_bytes(ColorsImportant, byteorder='little')
    print(f"ColorsImportant= {ColorsImportant.hex(':')} = {colors_imp_value}")

    print("\n" + "-" * 70)
    print("ПІДСУМОК")

    print(f"Тип файлу: {type_str}")
    print(f"Розмір зображення: {width_value} x {height_value} пікселів")
    print(f"Глибина кольору: {bitcount_value} біт")
    print(f"Розмір файлу: {size_value} байт")


except FileNotFoundError:
    print(f"ПОМИЛКА: Файл '{path_to_file}' не знайдено!")
    print("Будь ласка, вкажіть правильний шлях до файлу bmp_8.bmp")
except Exception as e:
    print(f"ПОМИЛКА при читанні файлу: {e}")