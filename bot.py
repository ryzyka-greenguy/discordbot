import discord
import json
from discord import app_commands
from discord.ext import commands
from github import Github

# Replace these with your actual tokens
DISCORD_TOKEN = 'MTI5MDMwNDA5OTI2NjU5Mjg1MQ.G-fUA_.FSZrTgfRAiBvhnkQ60L1-B9gk7T7Oyf3e1N-NY'  # Your Discord bot token
GITHUB_TOKEN = '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'  # Your GitHub personal access token
GITHUB_REPO = 'ryzyka-greenguy/Neco-Hub'  # Your GitHub repository

# Initialize bot with intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)

@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')

    # Sync the command tree
    await bot.tree.sync()
    print('Command tree synced!')

@bot.tree.command(name="addscript")
@app_commands.describe(script_name="The name of the script", script_content="The content of the script")
async def add_script(interaction: discord.Interaction, script_name: str, script_content: str):
    bot_role = interaction.guild.me.top_role
    user_roles = interaction.user.roles

    if any(role.position > bot_role.position for role in user_roles):
        try:
            # Load the existing scripts from the .json file on GitHub
            contents = repo.get_contents('script.json')  # Path to the script.json
            scripts = json.loads(contents.decoded_content.decode())

            # Create a new script entry
            new_script = {
                "name": script_name,
                "script": script_content  # Directly use the content
            }
            scripts.append(new_script)

            # Convert back to JSON string with json.dumps
            updated_content = json.dumps(scripts, indent=4)

            # Commit the change to the GitHub repository
            repo.update_file(contents.path, f"Add script: {script_name}", updated_content, contents.sha)

            await interaction.response.send_message(f"Script '{script_name}' added successfully to GitHub!")

        except Exception as e:
            print(f"Error: {e}")  # Print error to the console for debugging
            await interaction.response.send_message(f"Failed to add script: {e}")
    else:
        await interaction.response.send_message("You do not have permission to use this command.")

bot.run(DISCORD_TOKEN)
