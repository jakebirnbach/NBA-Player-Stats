import json
from aiohttp import web
import requests

perams = {
    'stat_type' : {},
    
    'P1' : {
        'first_name': {},
        'last_name': {},
        'year_f': {},
        'year_l': {}
    },

    'P2' : {
        'first_name': {},
        'last_name': {},
        'year_f': {},
        'year_l': {}
    }
}

perams['stat_type'] = "PTS"
perams['P1']['first_name'] = 'Lebron'
perams['P1']['last_name'] = 'James'
perams['P1']['year_f'] = 2003
perams['P1']['year_l'] = 2021

perams['P2']['first_name'] = 'Michael'
perams['P2']['last_name'] = 'Jordan'
perams['P2']['year_f'] = 1984
perams['P2']['year_l'] = 2004


#print(json.dumps(perams))



async def post_json(request):
    return web.json_response(perams)


#async def file_upload(request):
 #   return web.Response(text = )
#Use this to return stats JSON   
async def get_stats(request):
    body = await request.json()
    #import other python file
    return web.json_response(body)

#async def get(request):
    #return web.Response(text='Hi Ben')
app = web.Application()
app.add_routes([web.get('/data', post_json),
                web.static('/images', './outputs'),
                #generates images and returns json stat array, return urls
                web.post('/get-stats', get_stats)])
               
                #web.get('/p1-img', file_upload)])
web.run_app(app)

# curl -d '{"test": "Hi Mom"}' -H 'Content-Type: application/json' localhost:8080/get-stats