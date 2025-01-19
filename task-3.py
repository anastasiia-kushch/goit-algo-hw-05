from pathlib import Path
import timeit


def build_shift_table(pattern):
    table = {}
    length = len(pattern)

    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1

    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0 

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1 

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1 

        if j < 0:
            return i 


        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1




def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1




def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)

    base = 256 
    modulus = 101  

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1




def main():
    text1 = None
    text2 = None

    with open(Path('text/article_1.txt'), 'rb') as file:
        text1 = file.read().decode('utf-8', errors='ignore')

    with open(Path('text/article_2.txt'), 'r', encoding='utf-8') as file:
        text2 = file.read()


    pattern = "International Journal on Software Tools"
    
    results_text1 = {
        "Boyer-Moore": timeit.timeit(lambda: boyer_moore_search(text1, pattern), number=1), 
        "Knuth-Morris-Pratt": timeit.timeit(lambda: kmp_search(text1, pattern), number=1), 
        "Rabin-Karp": timeit.timeit(lambda: rabin_karp_search(text1, pattern), number=1)
    }
    
    results_text2 = {
        "Boyer-Moore": timeit.timeit(lambda: boyer_moore_search(text2, pattern), number=1), 
        "Knuth-Morris-Pratt": timeit.timeit(lambda: kmp_search(text2, pattern), number=1), 
        "Rabin-Karp": timeit.timeit(lambda: rabin_karp_search(text2, pattern), number=1)
    }
    
    generate_markdown(results_text1, results_text2)


def generate_markdown(results_text1, results_text2):
    markdown = "# Результати алгоритмів пошуку підрядка\n\n"

    markdown += "## Текст 1\n\n"
    markdown += "| Алгоритм          | Час виконання (секунди) |\n"
    markdown += "|-------------------|-------------------------|\n"
    for algo, time in results_text1.items():
        markdown += f"| {algo:<17} | {time:.6f}               |\n"

    markdown += "\n## Текст 2\n\n"
    markdown += "| Алгоритм          | Час виконання (секунди) |\n"
    markdown += "|-------------------|-------------------------|\n"
    for algo, time in results_text2.items():
        markdown += f"| {algo:<17} | {time:.6f}               |\n"

    markdown += "\n## Висновки\n\n"
    markdown += (
        f"Для тексту 1 найшвидшим алгоритмом є {min(results_text1, key=results_text1.get)}.\n"
        f"Для тексту 2 найшвидшим алгоритмом є {min(results_text2, key=results_text2.get)}.\n"
    )

    with open("results.md", "w", encoding="utf-8") as file:
        file.write(markdown)



main()