from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import asyncio
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


STREAM_DELAY = 5 # second
RETRY_TIMEOUT = 15000  # milisecond




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/stream')
async def message_stream(request: Request):
    def new_messages():
        yield "Hello World"
    async def event_generator():
        while True:
            if await request.is_disconnected():
                print("Client Disconnected")
                break
            
            if new_messages():
                yield {
                    'data': {
                        "status":"Good"
                    }
                }
            
            await asyncio.sleep(STREAM_DELAY)
    
    return EventSourceResponse(event_generator())


@app.get("/")
def root():
    # return "Not found"
    try:
        with open("main.html","r") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>File Not found</h1>")
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error {e} occured</h1>")

