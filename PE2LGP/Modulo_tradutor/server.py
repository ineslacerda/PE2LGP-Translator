import socket
import socket
import sys
import os
from tradutor import tradutor_main, translate_sentence
from _thread import start_new_thread
import json
import os


from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

import ssl

# from flask import Flask
# from flask_restful import abort, Api, Resource

# app = Flask(__name__)
# api = Api(app)

# class tradutor(Resource):
#     def get(self):
#         print(self)
#         return json.dumps({'success':True}), 200

#     def post(self):
#         print(self.text())
#         post_data = self.text()

#         try:
#             translated_sentence = translate_sentence(freeling_model, palavras_glosas, freq_dic, post_data)
#             print(translated_sentence)
#         except IndexError as err:
#             print('Error translating sentence')

#         try:
#             response = json.dumps(translated_sentence, ensure_ascii=False) #create response
#         except:
#             print('Error sending sentence')
#         return web.Response(status=200, body=response)

# api.add_resource(tradutor, '/tradutor', endpoint="tradutor")

# if __name__ == "__main__":
#     freeling_model, palavras_glosas, freq_dic = tradutor_main()
#     PORT = 443

#     ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#     ssl_context.load_cert_chain('../localhost.pem', '../localhost.pem')

#     app.run(host='0.0.0.0',port=PORT, ssl_context=ssl_context, debug=True)

from aiohttp import web
import aiohttp_cors

# AIOHTTP

routes = web.RouteTableDef()

# headers={"Access-Control-Expose-Headers": "Authorization, ETag",
#         "Access-Control-Allow-Origin": "*",
#         "Access-Control-Allow-Credentials": "true",
#         "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
#         "Access-Control-Allow-Headers": "*",

#headers={ "Content-Type": 'text/html'}

@routes.get('/')
async def get_handler(request):
    print(request.headers)
    return web.Response(status=200)

@routes.post('/')
async def post_handler(request):
    print("posttttt")
    print(request)
    post_data = await request.text()

    try:
        translated_sentence = translate_sentence(freeling_model, palavras_glosas, freq_dic, post_data)
        print(translated_sentence)
    except IndexError as err:
        print('Error translating sentence')
        translated_sentence = "Erro"

    try:
        response = json.dumps(translated_sentence, ensure_ascii=False) #create response
        if translated_sentence == "Erro":
                response = translated_sentence
    except:
        print('Error sending sentence')
    return web.Response(status=200, body=response)

#@routes.put('/')
#async def put_handler(request):
 #   print("putttt")

if __name__ == "__main__":
    freeling_model, palavras_glosas, freq_dic = tradutor_main()
    PORT = 80

    app = web.Application()
    # cors = aiohttp_cors.setup(app)
    corsconfig = {"http://web.tecnico.ulisboa.pt": aiohttp_cors.ResourceOptions(allow_credentials=True,
                                                    expose_headers=("Authorization", "ETag"),
                                                    allow_headers="*")}
    cors = aiohttp_cors.setup(app, defaults=corsconfig)
    app.add_routes(routes)

    for route in list(app.router.routes()):
        try:
            cors.add(route)
        except Exception as e:
            print(e)  # /register will be added twice and will raise error

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('../localhost.pem', '../localhost.pem')
    web.run_app(app, port=PORT) #ssl_context=ssl_context

    print("serving at port", PORT)
