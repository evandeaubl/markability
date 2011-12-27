import os
from markability import markdownify
from flask import Flask, request, render_template, make_response
app = Flask(__name__)

@app.route("/")
def url_form():
    return render_template('form.html')

@app.route("/u", methods=['POST'])
def convert_to_markdown():
    url = request.form['u']
    paralink = request.form.getlist('paralink')
    paragraph_link = (len(paralink) != 0)
    response = make_response(markdownify([url], paragraph_links = paragraph_link))
    response.headers['Content-Type'] = 'text/plain; charset="utf-8"'
    return response

@app.errorhandler(500)
def internal_server_error(e):
    print e

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

