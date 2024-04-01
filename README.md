# Discord AI Chat Cogs
## Some Discord Cogs combined with GPT and VOICEVOX
Isn't it wonderful to have an AI assistant or a cute partner to chat with?
This also supports the famous cute Japanese text-to-speak AI API, **VOICEVOX**!
## Preparation
1. you need an OpenAI API key
2. Change the settings in ```config.py```.
3. Download the [VOICEVOX](https://voicevox.hiroshiba.jp/) API.
4. Keep ```run.exe``` running.
5. Load the Cogs ```userdb```, ```chat_cmds```, ```user_cmds``` respectively using ```load-cogs [VALID_COG_NAME]``` command.
## How To Use
- Basic Chatting
  1. Type your message after ```chat_prefix```. For the default setting, try ```> hi```.
- Make it speak
  1. Use ```join``` command. ```$ join```, for example.
  2. Chat with the AI and wait for the response.
- Settings
  - Every user has his settings stored in ```User``` class from ```utils.UserDB```.
  - Use ```show``` command to lookup values. Try ```$ show``` or ```$ show prompt```.
  - Use ```set``` command to set values. For the default setting, try ```$ set voice_id 50```.
- Cogs Managing
  - List available Cogs with ```list-cogs```.
  - Load Cogs with ```load-cogs [VALID_COG_NAME]```.
  - Show loaded Cogs with ```show-cogs```.
  - Unload Cogs with ```unload-cogs [LOADED_COG_NAME]```
  - Reload Cogs with ```reload-cogs [LOADED_COG_NAME]```
  - Load all available Cogs with ```load-all-cogs```. *!!!Not Recommended!!!*
  - Unload all loaded Cogs with ```unload-all-cogs``` in the first place.
  - Reload all loaded Cogs with ```reload-all-cogs```.
## Warnings
- Using ```load-all-cogs``` is not recommended since ```chat_cmds``` and ```user_cmds``` requires ```userdb```.
