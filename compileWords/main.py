import os

def parse_file(filepath):
    with open(filepath, 'r') as file:
        word_dict = {}
        for line in file:
            word, freq = line.strip().split()
            year = int(filepath.split("/")[-2])
            freq = int(freq)
            if word in word_dict:
                word_dict[word]['freq'] += freq
                word_dict[word]['year'] = max(word_dict[word]['year'], year)
            else:
                word_dict[word] = {'freq': freq, 'year': year}
        return word_dict

def compile_word_frequencies(root_folder, output_folder):
    word_freq_by_length = {}

    for year in range(24):
        folder_path = os.path.join(root_folder, str(year))
        if not os.path.exists(folder_path):
            continue

        for length in range(3, 22):
            file_path = os.path.join(folder_path, f"len{length}.txt")
            if os.path.exists(file_path):
                word_dict = parse_file(file_path)
                if length in word_freq_by_length:
                    for word, data in word_dict.items():
                        if word in word_freq_by_length[length]:
                            word_freq_by_length[length][word]['freq'] += data['freq']
                            word_freq_by_length[length][word]['year'] = max(word_freq_by_length[length][word]['year'], data['year'])
                        else:
                            word_freq_by_length[length][word] = data
                else:
                    word_freq_by_length[length] = word_dict

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for length, word_dict in word_freq_by_length.items():
        output_file = os.path.join(output_folder, f"len{length}.txt")
        with open(output_file, 'w') as outfile:
            for word, data in word_dict.items():
                outfile.write(f"{word} {data['freq']} {data['year']}\n")

if __name__ == "__main__":
    current_dir = os.getcwd()
    # If you need to go up one level in the directory structure (optional)
    words_dir = os.path.dirname(current_dir)
    root_folder = os.path.join(words_dir, f"WordFrequencyFiles/")
    output_folder = "CompiledWords"
    compile_word_frequencies(root_folder, output_folder)
