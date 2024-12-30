import sys
from pathlib import Path

plugindir = Path.absolute(Path(__file__).parent)
paths = (".", "lib", "plugin")
sys.path = [str(plugindir / p) for p in paths] + sys.path

import json
from flowlauncher import FlowLauncher
import webbrowser


def load_vim_commands(file_path):
    """Load Vim commands from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

vim_commands = load_vim_commands('db/commands.json')
# vim_commands = load_vim_commands('commands.Not_url_encoded.json')


class VimCheatSheet(FlowLauncher):

    def query(self, query):
        # """Search for Vim commands matching the user query."""
        results = []
        query_lower = query.lower()  # Convert query to lowercase for case-insensitive matching
        for command in vim_commands:
            if any(keyword.startswith(query_lower) or query_lower == keyword for keyword in command["keywords"]):
            # if any(keyword in query_lower for keyword in command["keywords"]):
                results.append({
                    "Title": f"{command["command"]}",
                    "SubTitle": f"{command["name"]} | {command["description"]}",
                    "IcoPath": "icon.png",
                    # "ContextData": ["foo", "bar"],
                    "JsonRPCAction": {
                        "method": "open_url",
                        "parameters": [f"https://vim.rtorr.com/#:~:text={command['rtorr_description']}"],
                        "dontHideAfterAction": False
                    }
                })
                # print(results)

        # Fallback if no match is found 
        if not results:
            results.append({
                "Title": "No match found",
                "SubTitle": "Try searching for a different Vim command",
                "IcoPath": "icon.png",
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://github.com/Flow-Launcher/Flow.Launcher"],
                    "dontHideAfterAction": False
                }
            })

        return results

    # def context_menu(self, data):
    #     return [
    #         {
    #             "Title": {data["name"]},
    #             "SubTitle": "Press enter to open Flow the plugin's repo in GitHub",
    #             "IcoPath": "Images/app.png",
    #             "JsonRPCAction": {
    #                 "method": "open_url",
    #                 "parameters": ["https://github.com/Flow-Launcher/Flow.Launcher.Plugin.HelloWorldPython"]
    #             }
    #         }
    #     ]


    def open_url(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    VimCheatSheet()

