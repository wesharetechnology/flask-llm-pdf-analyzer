# Flask-LLM App

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)
## Introduction
This is a flask app that uses the LLM model to extract chemicals from a PDF File input.
## Project Setting
1. The project runs on conda environment for running large language models. To install the same conda environment, run `conda env create -f llm_env.yml` or `pip install -r llm_requirement.txt` (actually pip install or conda install?)
### Build a flask app
Tutorial Source: [How to build a web application using Flask and deploy it to the cloud](https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/)
1. `pip install flask`; then create by `virtualenv "venv"`
2. On windows, allowing running the script `Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser`
3. On windows, `venv\Scripts\activate`
4. `pip install flask`
5. Enter directory `cd flask_app`
### run the llm model (ChatGLM-6B)
1. Make sure the correct python version/interpreter is used when typing `python` in terminal
2. Currently, the model is run locally. The path is set at `main.py` in `LLM_MODEL_PATH`. Change the path to the correct path of the model. or change to `THUDM\chatglm-6b`
## Problem of the current application
1. [Scalability] Locks and the multithread handler have not been implemented
2. [Error Rate] The llm gives unstable output
    - Results are not complete: some chemicals are missing
    - The output is not consistent: the same input may give different output
    - The output is not accurate: some chemicals that appear in the article are not used in the laboratory
    - The model can output mixed Chinese and English; This app cannot output JSON
3. [Response Time] Currently, each sentence is processed one by one, which is not efficient
    - There is a tradeoff: short sentences and short prompts lead to more accurate result, the model is called more times, hence slower response time; long sentences and long prompts lead to less accurate result, the model is called less times, and the response time is shorter