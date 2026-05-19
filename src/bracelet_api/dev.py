import uvicorn


def run_dev() -> None:
    uvicorn.run(
        "bracelet_api.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )
