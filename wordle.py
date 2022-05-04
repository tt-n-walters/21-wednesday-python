import requests


url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
response = requests.get(url)
if response.status_code == 200:
    print("Successfully downloaded.")
else:
    print("Download error.", response.status_code)
    exit()


words = response.text.splitlines()
print("Total words:", len(words))

all_five_letters = []

for i in range(370103):
    if len(words[i]) == 5:
        five_letter_word = words[i]
        all_five_letters.append(five_letter_word)


print("Five letter words:", len(all_five_letters))

green = "_oi_t"
yellow = ""
grey = "audms"


for i in range(15918):
    word = all_five_letters[i]
    passed_green = True
    for j in range(5):
        if not green[j] == "_" and not word[j] == green[j]:                                # GREEN LETTERS
            passed_green = False
    
    passed_yellow = True
    for j in range(len(yellow)):
        if yellow[j] not in word:
            passed_yellow = False
    
    passed_grey = True
    for j in range(len(grey)):
        if grey[j] in word:
            passed_grey = False

    if passed_green and passed_yellow and passed_grey:
        print(word)

    
