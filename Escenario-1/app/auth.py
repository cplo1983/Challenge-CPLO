from fastapi import Header, HTTPException, status

API_KEY = "your_api_key_here"  # Cargar de variable de entorno en producción

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return x_api_key