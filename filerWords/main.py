import os

def read_words_from_file(filename):
    with open(filename, 'r') as file:
        words_array = file.read().splitlines()
    return words_array

def remove_non_capital_words(word_list):
    return [word for word in word_list if word.isupper()]

def remove_nyt_z (word_list):
    return [word for word in word_list if word not in ("NYT", "Z", "PDF", "FAQ")]

if __name__ == "__main__":
    startYear = 23
    endYear = 24
    year = str(startYear)

    for y in range(startYear, endYear):     # Loop for years
        year = str(y)

        # Get the current working directory (current location of the Python script)
        current_dir = os.getcwd()
        # If you need to go up one level in the directory structure (optional)
        words_dir = os.path.dirname(current_dir) + "/WordProcessing"
        file_path = os.path.join(words_dir, f"scraped_words{year}.txt")

        words = read_words_from_file(file_path)

        capital_words_list = remove_non_capital_words(words)
        cleaned_list = remove_nyt_z(capital_words_list)

        print(len(cleaned_list))
        for word in cleaned_list:
            print(word)

        savePath = os.path.join(words_dir, f"cleaned_words{year}.txt")

        with open(savePath, "w") as file:
            for word in cleaned_list:
                file.write(word + "\n")

            print(f"Cleaned words have been saved to: {savePath}")

