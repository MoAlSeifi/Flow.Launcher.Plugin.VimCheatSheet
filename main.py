import sys
from pathlib import Path

plugindir = Path.absolute(Path(__file__).parent)
paths = (".", "lib", "plugin")
sys.path = [str(plugindir / p) for p in paths] + sys.path

import json
from flowlauncher import FlowLauncher
import webbrowser

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_vim_commands(file_path):
    """Load Vim commands from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

vim_commands = load_vim_commands('db/commands.json')
# vim_commands = load_vim_commands('commands.Not_url_encoded.json')
icon_path = "src/icon.png"

# Global variables for TF-IDF processing
documents = [
    " ".join(command["keywords"]) + " " + command["description"] for command in vim_commands
]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

class VimCheatSheet(FlowLauncher):

    def query(self, query):
        # Transform the query into a TF-IDF vector
        query_vector = vectorizer.transform([query])

        # Compute cosine similarity between the query and all documents
        similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

        # Separate matches into keyword and description categories
        keyword_matches = []
        description_matches = []

        if similarities.max() > 0:  # Check if there are relevant matches
            top_indices = similarities.argsort()[::-1]  # Sort indices by similarity in descending order

            for index in top_indices:
                if similarities[index] == 0:  # Stop if similarity is zero
                    break

                command = vim_commands[index]

                # Check if the query matches keywords or description
                if any(query.lower() in keyword.lower() for keyword in command["keywords"]):
                    keyword_matches.append({
                        "Title": f"{command['command']}",
                        "SubTitle": f"{command['name']} | {command['description']}",
                        "IcoPath": icon_path,
                        "JsonRPCAction": {
                            "method": "open_url",
                            "parameters": [f"https://vim.rtorr.com/#:~:text={command['rtorr_description']}"],
                            "dontHideAfterAction": False
                        }
                    })
                else:
                    description_matches.append({
                        "Title": f"{command['command']}",
                        "SubTitle": f"{command['name']} | {command['description']}",
                        "IcoPath": icon_path,
                        "JsonRPCAction": {
                            "method": "open_url",
                            "parameters": [f"https://vim.rtorr.com/#:~:text={command['rtorr_description']}"],
                            "dontHideAfterAction": False
                        }
                    })

        # Combine keyword matches first, then description matches
        results = keyword_matches + description_matches

           # Fallback if no match is found 
        if not results:
            results.append({
                "Title": "No match found",
                "SubTitle": "Try searching for a different Vim command",
                "IcoPath": icon_path,
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://github.com/MoAlSeifi/Flow.Launcher.Plugin.VimCheatSheet"],
                    "dontHideAfterAction": False
                }
            })

        return results

        # Fallback if no match is found 
        if not results:
            results.append({
                "Title": "No match found",
                "SubTitle": "Try searching for a different Vim command",
                "IcoPath": icon_path,
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://github.com/MoAlSeifi/Flow.Launcher.Plugin.VimCheatSheet"],
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

