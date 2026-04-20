# Building a FastAPI application with Python

from fastapi import FastAPI

# Create an instance of the FastAPI application
app = FastAPI()

@app.get("/") # Define a route for the root URL
def home():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/about") # Define a route/endpoint for the /about URL
def about():
    return {
        "course" : "Python Full Stack Developer",
        "instructor" : "Jo$h",
        "description" : "Learn Python programming from scratch to building full-stack applications."
    }









# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)