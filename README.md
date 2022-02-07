# IPMI Bot [![Docker image build](https://github.com/realdeadbeef/IPMI-Bot/actions/workflows/buildmain.yml/badge.svg)](https://github.com/realdeadbeef/IPMI-Bot/actions/workflows/buildmain.yml)
This is a basic python based telegram bot which is designed to allow you to remotely manage a device using IPMI.

# Setup
**Obtaining your telegram bot token and chat ID:**
1. Obtain your token from @BotFather  
	a. Run the command `/newbot` and follow the prompts.  
	b. Copy the API token. (This should NEVER be shared with anyone, as it gives the holder **complete** control over the bot's actions; as such, it should also be saved somewhere safe.)  
2. Send `/start` to @RawDataBot and look for:
```
"chat": {
	"id": xxxxxxxxxx,
```
This is your chat ID.
## Method 1 - Docker 🐳:

**Running the bot:**

`docker run -d --network=bridge --name=ipmibot -e IPMI_IP=0.0.0.0 -e IPMI_USER=username -e IPMI_PASSWORD=password -e TOKEN=token -e CHAT_ID=chatid realdeadbeef/ipmi-bot:latest`

Make sure to change the environment variables and then run the command.

But Wait! What does this command do?

 1. `-d`: This tells docker to run the container in the background.
 2. `--network=bridge`: Ensures that the script can talk to devices on your home network, in this case the IPMI server.
 3. `--name=ipmibot`: Gives the container a name, in this case: `ipmibot`.
 4. `-e IPMI_IP=0.0.0.0`: Sets the IP of the IPMI server.
 5. `-e IPMI_USER=username`: Sets the username of the user for interfacing with IPMI.
 6. `-e IPMI_PASSWORD=password`: Sets the password for the user used to interface with IPMI.
 7. `-e TOKEN=token`: Sets the token of your telegram bot.
 8. `-e CHAT_ID=chatid`: Sets the chat ID that the bot should respond to messages from, so only you can manage the server.
 9. **(Optional)** You can remove the `-d` flag and replace it with `-it` to see the bot's output in an interactive console.

---

**Managing the docker container:**  
`docker ps` - This command shows all running containers and their names, as well as other information (add `-a` to see stopped containers as well).  
`docker start [container name]` - Used to start a docker container.  
`docker restart [container name]` - Used to restart a docker container  
`docker stop [container name]` - Used to stop a docker container.  
`docker kill [container name]` - Used to kill a running/crashed container.

## Method 2 - Running directly in python
**Prerequisites:**
1. The [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library. (`pip install python-telegram-bot --upgrade`)
2. [Python 3](https://python.org)
3. [ipmitool](https://www.ibm.com/docs/en/power8/8335-GTA?topic=overview-ipmitool) (`apt install ipmitool`)

**Running:**  
Change `configType` to `ini` and run `main.py`. Change the settings in the new `config.ini` file to your desired configuration and run `main.py` once more. That's it!
