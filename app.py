
# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from openai import AzureOpenAI



# app = Flask(__name__)
# CORS(app)  


# #   rag setting + azure AI
# endpoint = "https://dealsummaryai.openai.azure.com/"
# deployment ="gpt-4"
# api_key = "10aJ5Quo1eQly3alznvLqEHQnqnfuEX2IRQcPUZaPRuPTDtxL67cJQQJ99BHACYeBjFXJ3w3AAABACOGTP4F"   # 👈 API Key auth instead of Entra ID

# # Azure OpenAI client (API Key based)
# client = AzureOpenAI(
#     azure_endpoint="https://dealsummaryai.openai.azure.com/",
#     api_key="10aJ5Quo1eQly3alznvLqEHQnqnfuEX2IRQcPUZaPRuPTDtxL67cJQQJ99BHACYeBjFXJ3w3AAABACOGTP4F",
#     api_version="2024-05-01-preview",
# )

# # --- Flask Routes ---
# @app.route("/chat", methods=["POST"])
# def chat():
#     try:
#         data = request.json
#         user_message = data.get("message", "")

#         if not user_message:
#             return jsonify({"error": "Message is required"}), 400

#         # Azure OpenAI with Cognitive Search (RAG)
#         response = client.chat.completions.create(
#             model=deployment,
#             temperature=0.7,
#             max_tokens=1000,
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant "},
#                 {"role": "user", "content": user_message}
#             ],
#             extra_body={
#                 "data_sources": [
#                     {
#                         "type": "azure_search",
#                         "parameters": {
#                             "endpoint": "https://cilma-search-index.search.windows.net",
#                             "index_name":"dealsummary",
#                             "authentication": {
#                                 "type": "api_key",  
#                                 "key": "D4D5AB4BAA282B5BD07C71B1E2DDB65B"
#                             }
#                         }
#                     }
#                 ],
#     #             "enhancements": {
#     #     "grounding": {
#     #         "allow_fallback": True   # 👈 lets model use general knowledge if dataset has no answer
#     #     }
#     # }
#             }
#         )

#         reply = response.choices[0].message.content
#         return jsonify({"reply": reply})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(port=5000, debug=True)




# with authentication via Entra ID

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import AzureOpenAI
from azure.identity import InteractiveBrowserCredential, get_bearer_token_provider
 
app = Flask(__name__)
CORS(app)  
 
# --- RAG settings ---
endpoint = "https://dealsummaryai.openai.azure.com/"
deployment = "gpt-4"
 
# --- Authentication using InteractiveBrowserCredential ---
credential = InteractiveBrowserCredential(
    tenant_id="72f988bf-86f1-41af-91ab-2d7cd011db47"
)
 
token_provider = get_bearer_token_provider(
    credential,
    "https://cognitiveservices.azure.com/.default"
)
 
# Azure OpenAI client (token-based)
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-05-01-preview",
)
 
# --- Flask Routes ---
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
 
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
 
        # Azure OpenAI with Cognitive Search (RAG)
        response = client.chat.completions.create(
            model=deployment,
            temperature=0.7,
            max_tokens=1000,
            messages=[
                {"role": "system", "content": "You are a helpful assistant "},
                {"role": "user", "content": user_message}
            ],
            extra_body={
                "data_sources": [
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": "https://cilma-search-index.search.windows.net",
                            "index_name":"dealsummary",
                            "authentication": {
                                "type": "api_key",  
                                "key": "D4D5AB4BAA282B5BD07C71B1E2DDB65B"
                            }
                        }
                    }
                ],
            }
        )
 
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
 
if __name__ == "__main__":
    app.run(port=5000, debug=True)

    