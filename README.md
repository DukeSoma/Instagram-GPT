# Instagram-GPT
Ini adalah bot Instagram yang menggunakan OpenAI API untuk membuat bot ChatGPT.

## To run the script on Windows or a VPS running Ubuntu, you will need to follow these steps:
```sudo apt-get update``` &
```sudo apt-get install python3```

## Install the required modules: Use the ```requirements.txt``` file provided earlier to install all the required modules by running the following command:
```pip install -r requirements.txt```

## Create a ```.env``` file: Create a ```.env``` file in the same directory as your script and add your OpenAI API key, Instagram username, and Instagram password to it in the following format:
```
OPENAI_API_KEY=your-openai-api-key
INSTAGRAM_USERNAME=your-instagram-username
INSTAGRAM_PASSWORD=your-instagram-password
```
Make sure to replace ```your-openai-api-key```, ```your-instagram-username```, and ```your-instagram-password``` with your actual OpenAI API key, Instagram username, and Instagram password.

## Run the script: Use the ```python``` command to run the script. On Windows, open a command prompt, navigate to the directory where your script is located, and run the following command:
```python bot.py```
