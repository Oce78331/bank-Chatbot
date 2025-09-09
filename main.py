from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
import warnings
from rag_service import RAGService

# Suppress noisy logs and telemetry
logging.getLogger("chromadb").setLevel(logging.CRITICAL)
logging.getLogger("onnxruntime").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"
warnings.simplefilter("ignore")

app = FastAPI()

# CORS (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service lazily to avoid API key requirement at startup
rag_service = None

def get_rag_service():
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
    return rag_service


@app.post("/chat/rag/stream")
async def chat_rag_stream(request: Request):
    data = await request.json()
    question = data.get("question", "")
    if not question:
        return JSONResponse({"error": "Question is required"}, status_code=400)

    async def event_generator():
        try:
            service = get_rag_service()
            async for token in service.stream_answer(question):
                yield f" {token}\n\n"   # Proper SSE format
            yield "[DONE]\n\n"         # End of stream
        except Exception as e:
            yield f"ERROR: {str(e)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post("/chat/rag")
async def chat_rag(request: Request):
    data = await request.json()
    question = data.get("question", "")
    if not question:
        return JSONResponse({"error": "Question is required"}, status_code=400)

    service = get_rag_service()
    answer = await service.get_answer(question)
    return {"answer": answer}


@app.get("/")
async def read_root():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "Banking Chatbot API is running"}


@app.get("/styles.css")
async def read_css():
    return FileResponse("styles.css")


@app.get("/script.js")
async def read_js():
    return FileResponse("script.js")