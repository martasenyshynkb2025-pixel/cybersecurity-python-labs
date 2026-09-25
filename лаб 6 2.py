from collections import Counter
import re
import string

ENEIDA_TEXT ="""
Еней був парубок моторний
І хлопець хоть куди козак,
Удавсь на всеє зле проворний,
Завзятіший од всіх бурлак.
Но греки, як спалили Трою,
Зробили з неї скирту гною,
Він, взявши торбу, тягу дав;
Осмалив з лясощів пику,
Забравши деяку здобичу,
На морі утікать поспішав.
Як був тодi Еней пiсля Трої,
Чи то було за ним якесь,
Не знаю, чи за ним вiз якесь
Не знаю, чи за ним вiз якесь
Чуже добро, чи просто вiн
Побачив з далека щось iнше,
Не знаю, чи було щось там.
"""

# Приклад "табл. 6" - список допустимих українських слів (використовується для фільтрації)
# В реальному завданні цей список мав би бути набагато більшим
UKR_VOCABULARY =set([
    'еней', 'був', 'парубок', 'моторний', 'і', 'хлопець', 'хоть', 'куди', 'козак', 'удавсь',
    'на', 'всеє', 'зле', 'проворний', 'завзятіший', 'од', 'всіх', 'бурлак', 'но', 'греки',
    'як', 'спалили', 'трою', 'зробили', 'з', 'неї', 'скирту', 'гною', 'він', 'взявши',
    'торбу', 'тягу', 'дав', 'осмалив', 'лясощів', 'пику', 'забравши', 'деяку', 'здобичу',
    'по', 'морю', 'утікать', 'поспішав', 'було', 'чи', 'то', 'за', 'ним', 'якесь', 'не',
    'знаю', 'віз', 'чуже', 'добро', 'просто', 'побачив', 'далека', 'щось', 'інше', 'там', 'морі'
])
print("2. Частотний аналіз тексту\n" + "-" * 50)
# --- Етап 1: Очищення та токенізація слів ---
def preprocess_text(text, min_len=3):
    # Переведення в нижній регістр
    text = text.lower()
    # Видалення пунктуації
    # Заміна тире, дефісів та іншої пунктуації на пробіл, а потім видалення всього, що не є літерою
    text = re.sub(r'[—–-]', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation.replace("'",
                                                                           "")))  # Залишаємо апостроф, якщо це потрібно для української

    # Виділення слів
    words = text.split()

    # Фільтрація: довжина >= min_len (3) та перевірка на входження у словник (UKR_VOCABULARY)
    filtered_words = [
        word for word in words
        if len(word) >= min_len and word.isalpha() and word in UKR_VOCABULARY
    ]
    return filtered_words


processed_words = preprocess_text(ENEIDA_TEXT)
print(f"Кількість оброблених слів: {len(processed_words)}")
print(f"Перші 10 слів: {processed_words[:10]}\n")

# --- Етап 2: Підрахунок частоти слів ---
word_counts = Counter(processed_words)
# Сортування: від найбільшої частоти до найменшої
sorted_word_counts = word_counts.most_common()


# --- Етап 3: Підрахунок частоти пар літер ---
def count_pair_frequencies(words):
    pair_counts = Counter()
    for word in words:
        # Парами є (слово[i], слово[i+1])
        for i in range(len(word) - 1):
            pair = word[i:i + 2]
            pair_counts[pair] += 1
    return pair_counts


pair_counts = count_pair_frequencies(processed_words)
# Сортування: від найбільшої частоти до найменшої
sorted_pair_counts = pair_counts.most_common()

# --- Етап 4: Виведення результатів ---

# СЛОВА
print("### Частота слів (довжина >= 3, є в словнику)")

# a. 50 слів з найбільшою частотою
top_50_words = sorted_word_counts[:50]
print(f"a. 50 слів з найбільшою частотою ({len(top_50_words)} знайдено):")
# print(top_50_words) # Для стислості виводу
if top_50_words:
    print(f"   Найчастіше: {top_50_words[0]} | Найменш часте з 50: {top_50_words[-1]}")

# b. 100 слів з найбільшою частотою
top_100_words = sorted_word_counts[:100]
print(f"b. 100 слів з найбільшою частотою ({len(top_100_words)} знайдено):")
# print(top_100_words)
if top_100_words:
    print(f"   Найчастіше: {top_100_words[0]}")

# c. 50 слів з найменшою частотою (беремо останні 50 зі зворотного списку)
bottom_50_words = sorted_word_counts[-50:]
print(f"c. 50 слів з найменшою частотою ({len(bottom_50_words)} знайдено):")
# print(bottom_50_words)
if bottom_50_words:
    print(f"   Найменш часте: {bottom_50_words[-1]} | Найчастіше з 50: {bottom_50_words[0]}")

# d. 100 слів з найменшою частотою
bottom_100_words = sorted_word_counts[-100:]
print(f"d. 100 слів з найменшою частотою ({len(bottom_100_words)} знайдено):")
# print(bottom_100_words)
if bottom_100_words:
    print(f"   Найменш часте: {bottom_100_words[-1]}")

print("\n" + "---" * 15)

# ПАРИ ЛІТЕР
print("### Частота пар літер")

# e. 50 пар літер з найбільшою частотою
top_50_pairs = sorted_pair_counts[:50]
print(f"e. 50 пар літер з найбільшою частотою ({len(top_50_pairs)} знайдено):")
# print(top_50_pairs)
if top_50_pairs:
    print(f"   Найчастіша: {top_50_pairs[0]} | Найменш часта з 50: {top_50_pairs[-1]}")

# f. 100 пар літер з найбільшою частотою
top_100_pairs = sorted_pair_counts[:100]
print(f"f. 100 пар літер з найбільшою частотою ({len(top_100_pairs)} знайдено):")
# print(top_100_pairs)
if top_100_pairs:
    print(f"   Найчастіша: {top_100_pairs[0]}")

# g. 50 пар літер з найменшою частотою
bottom_50_pairs = sorted_pair_counts[-50:]
print(f"g. 50 пар літер з найменшою частотою ({len(bottom_50_pairs)} знайдено):")
# print(bottom_50_pairs)
if bottom_50_pairs:
    print(f"   Найменш часта: {bottom_50_pairs[-1]} | Найчастіша з 50: {bottom_50_pairs[0]}")

bottom_100_pairs = sorted_pair_counts[-100:]
print(f"h. 100 пар літер з найменшою частотою ({len(bottom_100_pairs)} знайдено):")
# print(bottom_100_pairs)
if bottom_100_pairs:
    print(f"   Найменш часта: {bottom_100_pairs[-1]}")