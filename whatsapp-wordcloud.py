import sys, os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import re
from collections import Counter
import json

# Let users know that it's working in the background
print("Generating WordClouds...\n")

# Open and load config file into a config object
try:
    cf = open('./config.json', 'r')
    config = json.load(cf)
    cf.close()
except FileNotFoundError:
    msg = "Sorry, the file ./config.json does not exist."
    print(msg)

# Open and read the chats from the '_chat.txt' file exported by Whatsapp
try:
    file = open(config['chat_filepath'], encoding="utf8")
    chat = file.read()
    file.close()
except FileNotFoundError:
    msg = "Sorry, the file " + config['chat_filepath'] + ' does not exist.'
    print(msg)

# Extract all dates to a list
dates = re.findall('\[(.*)\]', chat)

# Remove the dates from the chat to extract only messages
for date in dates:
    chat = chat.replace(date,'')

# Split the array based on regex
messages = re.split('\[(.*)\]', chat)

# Remove empty strings from messages array
while('' in messages):
    messages.remove('')

# Remove newline characters from messages
for item in range(0,len(messages)):
    messages[item] = messages[item].replace('\n','')

# Strings to hold Each User's Name
# Keep colan and space since it helps distinguish from normal name occurrences
my_name = config['my_name'] + ': '
partner_name = config['partner_name'] + ': '

# List to hold the author name of each message. Will be parallel indexed with 'messages' and 'dates'
author = []

# List to hold clean messages
clean_messages = []

# Iterate through our dictionary and copy messages to appropriate individual dictionary
for i in range(0,len(dates)):
    message = messages[i]

    if my_name in message:
        # Remove name and store message in appropriate individual dict
        clean_message = message.replace(my_name, '').strip()
        # Append cleaned name to author
        author.append(my_name.replace(': ',''))
        clean_messages.append(clean_message)

    if partner_name in message:
        # Remove name and store message in appropriate individual dict
        clean_message = message.replace(partner_name, '').strip()
        author.append(partner_name.replace(': ',''))
        clean_messages.append(clean_message)

# create a dictionary with the three lists
CSVdict = {'Date': dates, 'Author': author, 'Message': clean_messages}

# create a Pandas DataFrame from the dictionary
df = pd.DataFrame(CSVdict)

# Preview dataframe
# display(df) # Uncomment this line to preview the dataframe before it is saved.

# Save the csv file
csv_filename = './data/all_messages.csv'
df.to_csv(csv_filename)

print(f'Successfully saved {csv_filename}!\n')

# Drop rows that contain '<attachment:' so only real messages are included.
df = df[df["Message"].str.contains("<attached:") == False]

# Drop rows that contain "deleted this message" so deleted messages aren't included. (messages you deleted)
df = df[df["Message"].str.contains("deleted this message") == False]

# Drop rows that contain "This message was deleted" so deleted messages aren't included. (messages partner deleted)
df = df[df["Message"].str.contains("This message was deleted") == False]

# Drop rows that contain "Missed video call" so missed calls are not included.
df = df[df["Message"].str.contains("Missed video call") == False]

# Drop rows that contain "Missed voice call" so missed calls are not included.
df = df[df["Message"].str.contains("Missed voice call") == False]

# Create dataframe for partner messages only
partner_df = df[df['Author'].str.match(config['partner_name'])]

# Create dataframe for my messages only
my_df = df[df['Author'].str.match(config['my_name'])]

# Create list of each person's messages to be stored separately. Will be used for graph generation.
my_messages = my_df['Message'].tolist()
partner_messages = partner_df['Message'].tolist()

# Create string of all messages (Can be used to generate non-frequency based wordcloud using WordCloud.generate() if needed)
my_messages_string = '. '.join(my_messages)
partner_messages_string = '. '.join(partner_messages)

# Save the message strings for each person for easy access later
filename = './data/' + config['partner_name'].replace(' ', '_') + '_message_string.txt'
file = open(filename, 'w+', encoding='utf8')
file.write(partner_messages_string)
file.close()
print(f'Successfully saved {filename}!')

filename = './data/' + config['my_name'].replace(' ', '_') + '_message_string.txt'
file = open(filename, 'w+', encoding='utf8')
file.write(my_messages_string)
file.close()
print(f'Successfully saved {filename}!\n')

# Convert each person's message list to a dictionary with counted occurrences for each message.
my_word_count_dict = Counter(my_messages)
my_wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(my_word_count_dict)

# Convert each person's message list to a dictionary with counted occurrences for each message.
partner_word_count_dict = Counter(partner_messages)
partner_wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(partner_word_count_dict)

# Plot the my_wordcloud wordcloud and save/display it.
plt.figure(figsize=(15,8))
plt.imshow(my_wordcloud)
plt.axis("off")
#plt.show() # Can be uncommented to preview graph before saving to file.
filename = './output/' + config['my_name'].replace(' ','_') + '_wordcloud.png'
plt.savefig(filename, bbox_inches='tight')
print(f'Successfully saved {filename}!')
plt.close()

# Plot the partner_wordcloud wordcloud and save/display it.
plt.figure(figsize=(15,8))
plt.imshow(partner_wordcloud)
plt.axis("off")
#plt.show() # Can be uncommented to preview graph before saving to file.
filename = './output/' + config['partner_name'].replace(' ','_') + '_wordcloud.png'
plt.savefig(filename, bbox_inches='tight')
print(f'Successfully saved {filename}!')
plt.close()

# Say thanks for using my project!
print("\nWordClouds Successfully Saved!\nGoodbye!")