from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from image_processing.process_images import process_images

router = APIRouter()

class ProcessamentoImagem(BaseModel):
    images_paths: list

@router.post("/processar-imagem")
async def processar_imagem(dados: ProcessamentoImagem):
    try:
        process_images(dados.images_paths)
        return {"message": "Imagem processada e partes salvas no banco de dados"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
