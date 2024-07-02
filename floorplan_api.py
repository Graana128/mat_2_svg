from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError

from floor_plan import FloorplanGenerator

class FileRequest(BaseModel):
    filename: str

app = FastAPI()

@app.post("/floorplan")
async def validate_mat_file(file_request: FileRequest):
    try:
        filename = file_request.filename 
        if not filename.endswith(".mat"):
            raise HTTPException(status_code=422, detail="Filename must end with .mat")

        outputfile = filename.split(".")[0] + ".svg"
        image_file = filename.split(".")[0] + ".png"
        floor_plan = FloorplanGenerator(filename, output_file=outputfile)
        floor_plan.draw("")

        paths = [outputfile, image_file]
        return {"paths": paths}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8020)
