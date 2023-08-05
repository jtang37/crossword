import os

def get_number_in_middle(text):
    # Split the text by whitespace and return the middle number as an integer
    return int(text.split()[1])

if __name__ == "__main__":
    current_dir = os.getcwd()
    root_folder = os.path.join(current_dir, f"CompiledWords/")
    output_folder = os.path.join(current_dir, f"SortedWords/")
    filePath = "len"

    currentList = {}
    for i in range(3, 22):
        filePath = os.path.join(root_folder, f"len{str(i)}.txt")
        with open(filePath) as file:
            currentList = file.read().splitlines()
        sortedList = sorted(currentList, key=get_number_in_middle, reverse=True)
        file_name = os.path.join(output_folder, f"len{i}.txt")

        with open(file_name, 'w') as file:
            for item in sortedList:
                file.write("%s\n" % item)

