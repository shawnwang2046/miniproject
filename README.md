# miniproject

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

To analysis 10k filings topics.


Detailed analysis is at:

https://docs.google.com/document/d/1dqil2g8VVNhrYTS_sEtiWTcImbsD_2yDTJBaRABj_MM/edit?usp=sharing

Slides at:
https://docs.google.com/presentation/d/1zcOt7jBQ78AigAlrFHLIC63Np1wUm9-7147IsiYsl8Y/edit#slide=id.g27d1918c0c4_0_157

Contents
- Dockerfile: Specifies the steps and commands to build the Docker image for the project.
  
- README.md: Provides comprehensive documentation for the project. If you are reading this, you're looking at the contents of this file!
  
- requirements.txt: Contains a list of Python packages and libraries required to run the project. Use `pip install -r requirements.txt` to install these dependencies.

- openapi.json: This file contains the OpenAPI specification for the API.
- redoc-static.html: An HTML file generated using Redoc for a visual representation of the API documentation based on the openapi.json file.
- tests: This directory contains all the test scripts and files required to validate the functionality and robustness of the project's API.

### App Directory

- main.py: This is the primary script responsible for executing the project's code, including initializing the API endpoints.

- crud.py: Contains utility functions for Create, Read, Update, and Delete operations on the database.

- database.py: Manages database connections and provides utility functions for database operations.

- model: Directory containing BERTopic model.

- topics.csv: A CSV file containing topic data.

Getting Started

1. Clone this repository:

2. Install the required packages:
   pip install -r requirements.txt

3. Run the main Python script:
   python main.py

4. (Optional) Build the Docker image:
   docker build -t miniproject .

5. (Optional) Run the Docker container:
   docker run -p 8000:8000 miniproject

Testing the API

Run the test script to validate the API:
   pytest

Contact

If you have any questions or need further assistance, please contact me at wxnfifth@gmail.com