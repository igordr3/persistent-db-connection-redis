from aiohttp import web
import socketio
import utils
#Access to XMLHttpRequest at 'http://localhost:8080/socket.io/?EIO=3&transport=polling&t=OPklIs9' from origin 'http://0.0.0.0:8080' has been blocked by CORS policy: The request client is not a secure context and the resource is in more-private address space `local`.


## a new SocketIO server that serves as an event-based messaging system between the server (Python) and the UI (web-browser)
sio = socketio.AsyncServer(cors_allowed_origins=['http://0.0.0.0:8080', 'http://localhost:8080'])


## Aiohttp creates a new (http) web app server with the give routes
app = web.Application()

# Connects the SocketIO server to our Web App http server
sio.attach(app)

# Initialize connection to the Redis Database
utils.init_redis()

## An aiohttp HTTP endpoint is defined as this
async def chat(request):
    with open('frontend-app.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

## Event coming from the frontend that the backend is listening for
@sio.on('newUser')
async def print_message(sid, message):
    print("_______________")
    print("Another user has just joined...")
    print("Socket ID: " , sid)
    print("Name: " + message)

    # Interact with the open connection of Redis DB
    # add the current user to the set of online users
    utils.redis_client.sadd("who_is_online", message)
    print("Currently online:")
    print(utils.redis_client.smembers("who_is_online"))


## This is the route definition
# We bind our aiohttp endpoint to our SocketIO app
app.router.add_get('/frontend-app', chat)

## We kick off our server
if __name__ == '__main__':
    web.run_app(app)