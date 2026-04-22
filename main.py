# Building a FastAPI application with Python

from fastapi import FastAPI

# Create an instance of the FastAPI application
app = FastAPI()

@app.get("/") # Define a route for the root URL
def home():
    return {"message": "Welcome to the FastAPI application!",
            "status": "online",
            "endpoints": {"/", "/about"}
    }

@app.get("/about") # Define a route/endpoint for the /about URL
def about():
    return {
        "course" : "Python Full Stack Developer",
        "instructor" : "Jo$h",
        "description" : "Learn Python programming from scratch to building full-stack applications."
    }



# import os
# import requests

# dune_api_key = os.getenv("DEFI_JOSH_DUNE_QUERY_API_KEY")

# if not dune_api_key:
#     raise ValueError("API key not found in environment variables")

# query_ids = [5779439, 5783623, 5785491, 5779698, 5781579, 5783320, 5783967, 5784210, 5784215, 5785149, 5785066, 5792313]  

# headers = {"X-DUNE-API-KEY": dune_api_key}

# for query_id in query_ids:
#     url = f"https://api.dune.com/api/v1/query/{query_id}/execute"
#     response = requests.post(url, headers=headers)
#     print(f"Query {query_id}: {response.status_code} - {response.text}")



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)