import os

letters_LIB : dict = {
    'A' : 0,
    'B' : 1,
    'C' : 2,
    'D' : 3,
    'E' : 4,
    'F' : 5,
    'G' : 6,
    'H' : 7,
    'I' : 8,
    'J' : 9,
    'K' : 10,
    'L' : 11,
    'M' : 12,
    'N' : 13,
    'Ñ' : 14,
    'O' : 15,
    'P' : 16,
    'Q' : 17,
    'R' : 18,
    'S' : 19,
    'T' : 20,
    'U' : 21,
    'V' : 22,
    'W' : 23,
    'X' : 24,
    'Y' : 25,
    'Z' : 26,
}

test_LIB : list[tuple] = [
    ('John', 113),
    ('Diana', 220),
    ('Dan', 144),
]

reference : tuple = ('Me', 37)

def word_weight(word : str) -> int:
    result : int = 0

    for letter in word:
        if (letter.upper() in letters_LIB.keys()):
            result += letters_LIB[letter.upper()]

    return result

def like_parser(likes_list : list[str]) -> int:
    result : int = 0
    for elements in likes_list:
        result += word_weight(elements)

    return result



def aproximate(user : tuple, max_size : int = 20) -> None:

    result : int = max_size

    table : list[int] = []
    results : list[int] = []

    for subjects in test_LIB:
        table.append(subjects[1])
    print(table)
    while result != 0:
        os.system('clear')
        print(
            f"USER : {reference} \n"
            f"TABLE : {table}"
        )

        for contents in table:
            results.append( user[1] - contents if (user[1] - contents) > 0 else contents - user[1])
        
        results.sort()
        print(results, results[0])
        input()

print(aproximate(reference))