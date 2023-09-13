from flask import Flask, request

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/post_json', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    print(content_type)
    if (content_type == 'application/json'):
        json = request.get_json()

        print(json["name"])

        return json
    else:
        return 'Content-Type not supported!'
 
# main driver function
if __name__ == '__main__':
    app.run(debug=True)