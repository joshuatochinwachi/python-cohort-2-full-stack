# Building a FastAPI application with Python

from fastapi import FastAPI

# Create an instance of the FastAPI application
app = FastAPI()

@app.get("/") # Define a route for the root URL
def home():
    return {"message": "Welcome to the FastAPI application!",
            "swagger ui": "/docs",
            "endpoints": ["/about", "/csv"]}

@app.get("/about") # Define a route/endpoint for the /about URL
def about():
    return {
        "course" : "Python Full Stack Developer",
        "instructor" : "Jo$h",
        "description" : "Learn Python programming from scratch to building full-stack applications."
    }

@app.get("/csv")
def csv():
    csv_content = "name,age,city\nAlice,30,New York\nBob,25,Los Angeles\nCharlie,35,Chicago"
    return {"csv_data": csv_content}
