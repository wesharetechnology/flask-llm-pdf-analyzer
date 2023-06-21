import json
def feed_to_model(sentences, model, tokenizer):
    responses = {
                    "chemical_info" : [
                    ]
                }
    # put the pdf text in a string
    # FIXME: delete i later
    i = 0
    for sentence in sentences:
        # feed each sentence to the model
        # prompt = f"""Please extract the names of chemical used in the text deliminated by triple backticks\
        # ```{sentence}```. Summerize each chemical in one JSON object. Do not output anything if there is no chemical name.\
        # The information of the chemical can be obtained from Sigma-Aldrich\
        # here is the json structure:\
        #     \"chemical_name\": \"..\",
        #     \"chemical_property\": \"..\",
        #     \"hazard\": \"..\"
        # """
        prompt = """Extract "chemical_name" (keyword,content) from the text above, 
                    also content such as "chemical_property", "chemical_hazard" and output in json format.
                    Do not output anything if there is no chemical name. Output JSON object only."""
        i += 1
        input ='{}\n\n{}'.format(sentence, prompt)
        
        response, history =  model.chat(tokenizer, input, history = [])
        print(response)
        try:
            data = json.loads(response)
        except:
            print("cannot load json")
            continue
        # print(type(data), data)
        responses["chemical_info"].append(data)
        # print(type(responses), responses)
    return responses

# def feed_to_model(setences, model, tokenizer):
#     responses = {
#         "chemical_info": [
    
#         ]
#     }
#     sentences = ["""TMI (150.6 mg, 0.5 mmol) was dissolved in ultrapure water (20 mL).""",
#     """Following the addition of potassium cyanide (65.1 mg, 1.0 mmol) and ethyl acetate (20 mL),
#     the mixture was stirred at room temperature for 30 min.""",
#     """After separating the organic layers,
#     the resulting water layer was extracted three times using ethyl acetate.""",
#     """A combined organic layer was dried over sodium sulfate and concentrated in vacuo to afford TMI-CN in high purity
#     as a pale yellow oil without further purification (95.2 mg, 95% yield). """]
    
#     # prompt = """Extract "chemical_name" (keyword, content) for chemicals that appears in the text above. 
#     #             You should also find the "property", "hazard" of the chemicals from Sigma-Aldrich and output in JSON format.
#     #             Do not output anything if there is no chemical name."""
#     # prompt = '从上文中，提取"chemical_name"(keyword,content)，包括:"property", "hazard"等类型的实体, 输出json格式内容'
#     prompt = """Extract "chemical_name" (keyword,content) from the text above, 
#                     also content such as "chemical_property", "chemical_hazard" and output in json format.
#                     Do not output anything if there is no chemical name. Output JSON object only."""
#     for sentence in sentences:
#         input ='{}\n\n{}'.format(sentence, prompt)
#         response, history = model.chat(tokenizer, input, history=[])
#         print(response)
#         data = json.loads(response)
#         print(type(data), data)
#         responses['chemical_info'].append(data)
#         print("response", type(responses), responses)
#     return responses
        