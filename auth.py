from langgraph_sdk import Auth

auth = Auth()

@auth.authenticate 
async def authenticate(headers: dict) -> Auth.types.MinimalUserDict:
  print(f"Headers: {headers}")
  origin = headers[b'origin'].decode("utf-8")
  print(origin)
  if origin != "movie-finder-ae697f7821735cd0abc9dac7c43c5980.us.langgraph.app":
    raise Auth.exceptions.HTTPException(status_code=401, detail="Invalid Auth Provided")

  return { 
    "identity": "movie-finder",
  }