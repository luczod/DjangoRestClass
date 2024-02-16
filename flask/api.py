from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup


def download_website(url, statusCode):
    response = requests.get(url)
    if response.status_code == statusCode:
        soup = BeautifulSoup(response.content, 'html.parser')
        """ with open('index.html', 'w', encoding='utf-8') as file:
            file.write(str(soup)) """
        return str(soup)
    else:
        print(
            f"Failed to download website. Status code: {response.status_code}")


app = Flask(__name__)


@app.route('/echo', methods=['POST'])
def echo():
    # Check if the request has JSON content
    if request.is_json:
        data = request.json
        # download_website(data['URL'], 200)
        return download_website(data['URL'], 200)

    else:
        # Return an error message if the request doesn't contain JSON content
        return jsonify({'error': 'Request body must be in JSON format'}), 400


@app.route('/page_html', methods=['GET'])
def page_html():
    return render_template('page_404.html')


if __name__ == '__main__':
    app.run(debug=True)
