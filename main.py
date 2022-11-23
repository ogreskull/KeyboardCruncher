# Hi!
# This script is for finding words that are "next to each other" on a qwerty_keyboard. For example, on a standard QWERTY
# qwerty_keyboard, dye and fur are "next to each other." The goal for this script is to provide enough flexibility to easily
# check this on an arbitrary (n > 1 && n < 26) n-rowed Latin alphabet qwerty_keyboard.

# Comments are based on the QWERTY keyboard


# incoming keyboard digestion happens here and spits out a friendly string
def keyboard_eval(input_keyboard):
    key_count = 0
    for row in input_keyboard:
        key_count += len(row)
    keyboard_name_list = input_keyboard[0][:6]
    keyboard_name = "".join([i.upper() for i in keyboard_name_list])
    if keyboard_name == "PYFGCR":
        keyboard_name = "Dvorak"
    return "This looks like a " + keyboard_name + " keyboard with " + str(
        key_count) + " keys. The keys use are placed in " + str(len(input_keyboard)) + " rows."


def keyboard_printer(input_keyboard):
    return_holder = ""
    for row in input_keyboard:
        row_number = input_keyboard.index(row)
        row_contents = "[" + "][".join([i.upper() for i in row]) + "]"
        return_holder += ("Row " + str(row_number + 1) + ": " + row_contents + "\n")
    return return_holder


# nothing clever here, just making sure all the words in the dictionary file are good:
# all caps for ease
# returns a list for easier operations
# only returns words shorter than the max length
def dictionary_ingest(input_dictionary_path):
    raw_dictionary = open(input_dictionary_path, 'r')
    loud_abridged_dictionary = [i.upper().strip() for i in raw_dictionary if len(i) <= word_length_max]
    return loud_abridged_dictionary


# makes the array all caps for comparison
# should add: something to check for doubles
def keyboard_ingest(input_keyboard):
    return_holder = []
    for row in input_keyboard:
        row_contents = [i.upper() for i in row]
        return_holder.append(row_contents)
    return return_holder


# No vertical wrapping at this time because that requires some different rules!
def find_moving_words(input_dictionary, input_keyboard, input_direction, input_steps, input_row_wrap):
    word_pair_list = []
    finished_word = ""
    if input_direction.lower() == "left":
        step_attempt = -input_steps
    elif input_direction.lower() == "right":
        step_attempt = input_steps
    else:
        return "you dun goofed, review " + input_direction

    good_pairs = []
    for starting_word in input_dictionary:
        end_word = ""
        for starting_letter in starting_word:
            if input_row_wrap:
                start_coord = find_keyboard_index(input_keyboard, starting_letter)
                end_coord = (start_coord[0], (start_coord[1] + step_attempt))
                end_word += (input_keyboard[end_coord[0]][(end_coord[1]) % len(input_keyboard[end_coord[0]])])
            else:
                start_coord = find_keyboard_index(input_keyboard, starting_letter)
                end_coord = (start_coord[0], (start_coord[1] + step_attempt))
                if end_coord[1] >= len(input_keyboard[end_coord[0]]) or end_coord[1] < 0:
                    end_word += "i'm a no good dirty edge case"
                else:
                    end_word += (input_keyboard[end_coord[0]][end_coord[1]])
        if end_word in input_dictionary:
            good_pairs.append((starting_word, end_word))
    return good_pairs


# returns the row and row position of the requested key
def find_keyboard_index(input_keyboard, input_letter):
    input_letter = input_letter.upper()
    if len(input_letter) != 1:
        return "bad input, too many letters"
    for row in input_keyboard:
        if input_letter in row:
            return input_keyboard.index(row), row.index(input_letter)


qwerty_keyboard = (
    ("q", "w", "e", "r", "t", "y", "u", "i", "o", "p"),
    ("a", "s", "d", "f", "g", "h", "j", "k", "l",),
    ("z", "x", "c", "v", "b", "n", "m")
)

dvorak_keyboard = (
    ("p", "y", "f", "g", "c", "r", "l"),
    ("a", "o", "e", "u", "i", "d", "h", "t", "n", "s"),
    ("q", "j", "k", "x", "b", "m", "w", "v", "z")
)

# row_wrap enables p -> q, otherwise p is an invalid starting character
row_wrap = True
# column_wrap presents some further difficulties, what do you do with p?

# movement is "right" or "left". o->p is "right"
movement = "right"
# steps is a natural number, o->p is 1
steps = 1
# long words take longer to search, duh, and very few finds
word_length_max = 6

working_keyboard = qwerty_keyboard
scrabble_dict = "dictionary.txt"
tiny_dict = "tinydictionary.txt"
working_dict = scrabble_dict

if __name__ == '__main__':
    print("Hello\n")
    print("Today, we're going to find some words.", end="\n\n")
    print("For reference, we are going to use the following keyboard: ")
    print(keyboard_printer(working_keyboard))
    print(keyboard_eval(working_keyboard), end='\n\n')
    print("The following dictionary will be used: " + working_dict)
    loud_dictionary = dictionary_ingest(working_dict)
    loud_keyboard = keyboard_ingest(working_keyboard)

    results = find_moving_words(loud_dictionary, loud_keyboard, movement, steps, row_wrap)
    print(*results, sep='\n')
    print("I found " + str(len(results)) + " results!")
