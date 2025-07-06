from langgraph_sdk import Auth

auth = Auth()

@auth.authenticate 
async def authenticate(headers: dict) -> Auth.types.MinimalUserDict:
  origin = headers[b'origin'].decode("utf-8")
  if origin != "https://findmymovie.ai":
    raise Auth.exceptions.HTTPException(status_code=401, detail="Invalid Auth Provided")

  return { 
    "identity": "movie-finder",
  }