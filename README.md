# cellscores
Repository for graphs of the Ingress cellscores, execute the script to present the cell scores in a Telegram chat

# Example output
![Checkpoint Graph](https://github.com/Lynnsanee/cellscores/blob/main/examples/cellscore_checkpoints.png)
![Cumulative Graph](https://github.com/Lynnsanee/cellscores/blob/main/examples/cellscore_cumulative.png)

# Installation
Install all necessary dependencies using pip

`python3 -m pip install -r requirements.txt`

# Configuration
Configurate cellscore graphs by editting the values in [cell_parameters](cell_parameters.py)

## Telegram
Configure the Telegram information by requesting a bot token from [Bot Father](t.me/botfather)

Insert the chat id that you want to post the images, mind that the bot is added to this chat and that it has permission to send images.

## Ingress
