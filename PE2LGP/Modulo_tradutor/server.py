import socket
import socket
import sys
import os
from tradutor import tradutor_main, translate_sentence
from _thread import start_new_thread
import json
import os
import traceback


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
import pandas as pd
import traceback

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
        df = pd.read_csv("error_log.csv", index_col=False)

        print(df)

        translated_sentence = translate_sentence(freeling_model, palavras_glosas, freq_dic, post_data, negativa_irregular, gestos_compostos)
        print(translated_sentence)

        # translated_sentence = {'glosas': ['BOA', 'TARDE', 'NOME', 'DELE', 'QUAL'], 'fonemas': [['BOA'], ['CA', 'CE'], ['CO', 'BE'], ['A', 'CE'], ['CUA']], 'gestos_compostos': ['false', 'false', 'false', 'false', 'false'], 'pausas': ['false', 'false', 'false', 'false', 'frase'], 'adv_cond': ['false', 'false', 'false', 'false', 'false'], 'exprFaciais': {'4-5': ['interrogativa_parcial'], '0-5': ['olhos_franzidos']}}

        # translated_sentence = {'glosas': ['NOME', 'DELE', 'QUAL'], 'fonemas': [['CO', 'BE'], ['CA', 'CE'], ['CUA']], 'gestos_compostos': ["false", "false", "false"], 'pausas': ['false', 'false', 'frase'], 'adv_cond': ["false", "false", "false"], 'adv_intensidade': ['false', 'false', 'false'], 'exprFaciais': {'2-3': ['interrogativa_parcial'], '0-3': ['olhos_franzidos']}}

        # translated_sentence = {'glosas': ['MULHER', 'IRMÃO', 'TEU', 'CONDUZIR'], 'fonemas': [['BU', 'CA'], ['EC', 'BAU'], ['CUA'], ['CU', 'CU']], 'gestos_compostos': ['false', 'true', 'false', 'false'], 'pausas': ['false', 'false', 'false', 'frase'], 'adv_cond': ['false', 'false', 'false', 'false'], 'adv_intensidade': ['false', 'false', 'false', 'false'], 'exprFaciais': {'3-4': ['interrogativa_total'], '0-4': ['olhos_franzidos']}}

        # translated_sentence = {'glosas': ['RAPAZ', 'AQUELE', 'ESCREVER', 'GOSTAR', 'NÃO', 'MAS', 'LER', 'ELE', 'GOSTAR'], 'fonemas': [['CA', 'BA'], ['A', 'CA', 'CE'], ['CE', 'FA'], ['CO', 'CA'], ['CAU'], ['BA'], ['CA'], ['A', 'CE'], ['CO', 'CA']], 'gestos_compostos': [False, False, False, False, False, False, False, False, False], 'pausas': ['false', 'false', 'false', 'false', 'oracao', 'false', 'false', 'false', 'frase'], 'adv_cond': [False, False, False, False, False, False, False, False, False], 'adv_intensidade': ['false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false'], 'exprFaciais': {'0-5': ['olhos_franzidos']}}

        # translated_sentence = {'glosas': ['CASA', 'ARRUMAR', 'MULHER', 'PRIMO', 'MEU_NO_EXPR', 'AJUDAR_EU'], 'fonemas': [['CA', 'CA'], ['A', 'CU', 'BA'], ['BU', 'CA'], ['BCE', 'BA'], ['BE', 'CA'], ['A', 'CU', 'COU', 'BE']], 'gestos_compostos': [False, False, False, True, False, False], 'pausas': ['false', 'false', 'false', 'false', 'false', 'frase'], 'adv_cond': [False, False, False, False, False, False], 'adv_intensidade': ['false', 'false', 'false', 'false', 'false', 'false']}

        # translated_sentence = {'glosas': ['CINEMA', 'TU', 'GOSTAR', 'NÃO', 'PORQUÊ'], 'fonemas': [['CE', 'CA', 'BA'], ['CU'], ['CO', 'CA'], ['CAU'], ['BU', 'CA']], 'gestos_compostos': [False, False, False, False, False], 'pausas': ['false', 'false', 'false', 'false', 'frase'], 'adv_cond': [False, False, False, False, False], 'adv_intensidade': ['false', 'false', 'false', 'false', 'false'], 'exprFaciais': {'4-5': ['interrogativa_parcial'], '0-5': ['olhos_franzidos']}}

        # translated_sentence = {'glosas': ['SUPERMERCADO', 'RAPAZ', 'ANDAR', 'QUANDO', 'MULHER', 'RAPAZ', 'ELE', 'CHOCAR_COM_PESSOA'], 'fonemas': [['CU', 'BA', 'BE', 'CA', 'CU'], ['CA', 'BA'], ['AC', 'CA'], ['CUA', 'CU'], ['BU', 'CA'], ['CA', 'BA'], ['A', 'CE'], ['CU', 'COU']], 'gestos_compostos': [False, False, False, False, False, True, False, False], 'pausas': ['false', 'false', 'oracao', 'false', 'false', 'false', 'false', 'frase'], 'adv_cond': [False, False, False, False, False, False, False, False], 'adv_intensidade': ['false', 'false', 'false', 'false', 'false', 'false', 'false', 'false']}
        
        # translated_sentence = {'glosas': ['SUPERMERCADO', 'SURDO', 'RAPAZ', 'ANDAR', 'QUANDO', 'MULHER', 'RAPAZ', 'ELE', 'CHOCAR_PESSOA', 'ELES', 'CAIR'], 'fonemas': [['CU', 'BA', 'BE', 'CA', 'CU'], [], ['CA', 'BA'], ['AC', 'CA'], ['CUA', 'CU'], ['BU', 'CA'], ['CA', 'BA'], ['A', 'CE'], ['CU', 'COU'], ['A', 'CE'], ['CAE', 'CAU']], 'gestos_compostos': [False, False, False, False, False, False, True, False, False, False, False], 'pausas': ['false', 'false', 'false', 'oracao', 'false', 'false', 'false', 'false', 'false', 'false', 'frase'], 'adv_cond': [False, False, False, False, False, False, False, False, False, False, False], 'adv_intensidade': ['false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false']}

        # translated_sentence = {'glosas': ['ELE', 'ESCREVER', 'NÃO_SABER', 'MAS', 'LER', 'ELE', 'SABER'], 'fonemas': [['A', 'CE'], ['CE', 'FA'], ['CAU'], ['BA'], ['CA'], ['A', 'CE'], ['CA', 'BE']], 'gestos_compostos': ['false', 'false', 'false', 'false', 'false', 'false', 'false'], 'pausas': ['false', 'false', 'oracao', 'false', 'false', 'false', 'frase'], 'adv_cond': ['false', 'false', 'false', 'false', 'false', 'false', 'false'], 'adv_intensidade': ['false', 'false', 'false', 'false', 'false', 'false', 'false'], 'exprFaciais': {'2-3': ['negativa_headshake'], '0-3': ['olhos_franzidos']}}

    except Exception as e:
        lines = traceback.format_exc().splitlines()
        exception_type = " " + lines[-1]
        filename = " " + lines[len(lines)-3].split(",")[0].split("/")[-1].replace('"', '')
        line_number = lines[len(lines)-3].split(",")[1]
        
        tempDf = pd.DataFrame(columns=['InputSentence','ErrorName','ErrorFile','ErrorLine'], data = [[post_data, exception_type, filename, line_number]])

        df = pd.concat([df,tempDf])
        print(df)
        df.to_csv("error_log.csv", index=False)
        print('Error translating sentence')
        translated_sentence = "Erro"

    try:
        response = json.dumps(translated_sentence, ensure_ascii=False) #create response
        if translated_sentence == "Erro":
                response = translated_sentence
    except:
        print('Error sending sentence')
    return web.Response(status=200, body=response)

# @routes.put('/')
# async def put_handler(request):
#    print("putttt")

if __name__ == "__main__":
    freeling_model, palavras_glosas, freq_dic, negativa_irregular, gestos_compostos = tradutor_main()
    PORT = 80

    app = web.Application()
    # cors = aiohttp_cors.setup(app)
    corsconfig = {"https://portallgp.ics.lisboa.ucp.pt": aiohttp_cors.ResourceOptions(allow_credentials=True,
                                                    expose_headers=("Authorization", "ETag"),
                                                    allow_headers="*")}
    cors = aiohttp_cors.setup(app, defaults=corsconfig)
    app.add_routes(routes)

    for route in list(app.router.routes()):
        try:
            cors.add(route)
        except Exception as e:
            print(e)  # /register will be added twice and will raise error

    # ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # ssl_context.load_cert_chain('../localhost.pem', '../localhost.pem')
    web.run_app(app, port=PORT) #ssl_context=ssl_context

    print("serving at port", PORT)
