import json
from flask import Flask, render_template, request
from transformers import AutoTokenizer, AutoModel
from werkzeug.middleware.proxy_fix import ProxyFix
import read_pdf
import run_llm

LLM_MODEL_PATH = "E:\Model\chatglm-6b"

app = Flask(__name__) 
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_PATH, trust_remote_code=True, revision="")
model = AutoModel.from_pretrained(LLM_MODEL_PATH, trust_remote_code=True, revision="").half().cuda()
model = model.eval()

@app.route('/')
def main():
    return render_template('index.html')
@app.route('/success', methods = ['POST'])
def success():  
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        sentences = read_pdf.extract_sentences(f.filename)
        result = run_llm.feed_to_model(sentences, model, tokenizer)
        # return render the result into string
        result_str = json.dumps(result, indent=4, ensure_ascii=False)
        # print(result_str)
        return render_template("acknowledgement.html", name = f.filename, result = result_str)

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(debug=True)