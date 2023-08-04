#create separate text files for different length words
import os

def read_words_from_file(filename):
    with open(filename, 'r') as file:
        words_array = file.read().splitlines()
    return words_array

def create_2d_array_from_sorted_list(sorted_list):
    if not sorted_list:
        return []

    # Initialize the 2D array with the first element from the sorted list
    result_array = [[sorted_list[0], 1]]

    # Iterate through the remaining elements in the sorted list
    for i in range(1, len(sorted_list)):
        current_string = sorted_list[i]
        if current_string == result_array[-1][0]:
            # If the current string is the same as the last one in the result_array,
            # increment the count for that string
            result_array[-1][1] += 1
        else:
            # If the current string is different from the last one in the result_array,
            # add it as a new entry in the result_array with a count of 1
            result_array.append([current_string, 1])

    return result_array

def sort_2d_array_by_string_length(input_array):
    return sorted(input_array, key=lambda x: (len(x[0]), -x[1]))

def create_text_files(sorted_array, year):
    current_dir = os.getcwd()
    # If you need to go up one level in the directory structure (optional)
    words_dir = os.path.dirname(current_dir)
    folder_path = os.path.join(words_dir, f"WordFrequencyFiles/{year}")
    os.makedirs(folder_path, exist_ok=True)

    file_map = {}
    for item in sorted_array:
        word, frequency = item[0], item[1]
        length = len(word)

        if length not in file_map:
            file_map[length] = []

        file_map[length].append(f"{word} {frequency}")

    for length, lines in file_map.items():
        file_name = os.path.join(folder_path, f"len{length}.txt")
        with open(file_name, "w") as file:
            file.write("\n".join(lines))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startYear = 23
    endYear = 24
    year = startYear

    # Get the current working directory (current location of the Python script)
    current_dir = os.getcwd()
    # If you need to go up one level in the directory structure (optional)
    words_dir = os.path.dirname(current_dir) + "/WordProcessing"
    file_path = os.path.join(words_dir, f"cleaned_words{year}.txt")
    words = read_words_from_file(file_path)


    for y in range(startYear, endYear):
        year = str(y)
        file_path = os.path.join(words_dir, f"cleaned_words{year}.txt")
        words = read_words_from_file(file_path)
        wordsSorted = sorted(words)
        result_2d_array = create_2d_array_from_sorted_list(wordsSorted)
        sorted_result_2d_array = sort_2d_array_by_string_length(result_2d_array)
        create_text_files(sorted_result_2d_array, year)
