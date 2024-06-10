from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="C15A866FCD2B75D053EF27FD1B6BA6C")
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth = OAuth()
oauth.register(
    name='steam',
    client_id='C15A866FCD2B75D053EF27FD1B6BA6C6',
    authorize_url='https://steamcommunity.com/oauth/login',
    response_type='code',
)


@app.middleware('http')
async def some_middleware(request: Request, call_next):
    headers = dict(request.scope['headers'])
    headers[b'Access-Control-Allow-Origin'] = b'*'
    request.scope['headers'] = [(k, v) for k, v in headers.items()]

    return await call_next(request)


@app.get('/login/steam')
async def login_steam(request: Request):
    print(request.headers)
    redirect_uri = request.url_for('authorize_steam')
    return await oauth.steam.authorize_redirect(request, redirect_uri)


@app.get('/authorize/steam')
async def authorize_steam(request: Request):
    print(2)
    try:
        token = await oauth.steam.authorize_access_token(request)
        user = await oauth.steam.parse_id_token(request, token)
        # Здесь можно сохранить информацию о пользователе в базе данных
        return {'message': f'Logged in as {user["name"]}'}
    except OAuthError as e:
        return {'error': str(e)}
