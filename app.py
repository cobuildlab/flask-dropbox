#!flask/bin/python
from flask import Flask
from flask import jsonify
import dropbox

app = Flask(__name__)

API_KEY = 'your_api_key'
dbx_client = dropbox.Dropbox(API_KEY)


def process_list(list_folder, data):
    for entry in list_folder.entries:
        data.append({
            'filename': entry.name,
            'path': entry.path_lower
        })
    if list_folder.has_more:
        return process_list(dbx_client.files_list_folder_continue(list_folder.cursor), data)
    return data


@app.route('/', methods=['GET'])
def get_dropbox_files():
    file_list = process_list(dbx_client.files_list_folder("", recursive=True), [])
    return jsonify({'data': file_list})


if __name__ == '__main__':
    app.run(debug=True)
