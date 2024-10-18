from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/")
def index() -> Response:
    return Response(content='{"message": "OK"}', media_type="application/json")
