# :cloud: WhatsApp WordCloud


#### Generate Frequency-Based WordCloud of Whatsapp Conversation from Exported Chat Log

## Installation

The project can be cloned from github using the following command

```bash
git clone https://github.com/JKelly423/whatsapp-wordcloud.git
```

Navigate to the project directory using ```cd``` as follows
```bash 
cd whatsapp-wordcloud
```

Run the following command to install all dependancies required

```bash
pip install -r requirements.txt
```

## Configuration
The WhatsApp chat must  be extracted before the project is executed.
Instructions for exporting your WhatsApp chat can be found here for [Android](https://faq.whatsapp.com/1180414079177245/?cms_platform=android) and [IOS](https://faq.whatsapp.com/902477924463699/?locale=en_US&cms_platform=iphone). The exported file ```_chat.txt``` will be used to generate the WordClouds.

In order to differentiate your messages from your partner's messages, you will need to configure the Contact Names for both you and your partner.

The configuration of the Contact Names as well as the WhatsApp chat log filepath will need to be configured within the ```config.json``` file before the project is executed. 
The ```config.json``` file will be configured as shown below:
```json
{
  "my_name":        "my_contact_name_as_appears_in_Whatsapp",
  "partner_name":   "partner_contact_name_as_appears_in_Whatsapp",
  "chat_filepath":  "./data/_chat.txt"
}
```
The default value for ```chat_filepath``` is ```./data/_chat.txt```. To use this default value, copy your exported ```_chat.txt``` file from your WhatsApp export into the ```/data``` directory of the project directory.

For example, if your name (as shown in the WhatsApp chat) is ```John``` and your partners name (as shown in the WhatsApp chat) is ```Jane Doe```,
your config will look like this:
```json
{
  "my_name":        "John",
  "partner_name":   "Jane Doe",
  "chat_filepath":  "./data/_chat.txt"
}
```

## Execution 
After configuration is complete and all dependacies, the project can be executed using the following command.
```bash
python3 whatsapp-wordcloud.py
```

After allowing the program to run, the completed WordCloud images will be saved in the ```/output``` directory, named ```my_name_wordcloud.png``` and ```partner_name_wordcloud.png``` based on your name configuration. Enjoy!


----
#### Thanks for using my cool project :)
