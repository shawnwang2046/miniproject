# miniproject

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

To analysis 10k filings topics.


Detailed analysis is at:

https://docs.google.com/document/d/1dqil2g8VVNhrYTS_sEtiWTcImbsD_2yDTJBaRABj_MM/edit?usp=sharing

Contents

- Dockerfile: This file is used to build a Docker image for the project.
- main.py: This is the main Python script that executes the project's code.
- README.md: This file provides documentation for the project.
- requirements.txt: This file lists the Python packages that are required to run the project.
- test_api.py: This script contains the tests for the API.

Getting Started

1. Clone this repository:

2. Install the required packages:
   pip install -r requirements.txt

3. Run the main Python script:
   python main.py

4. (Optional) Build the Docker image:
   docker build -t miniproject .

5. (Optional) Run the Docker container:
   docker run -p 4000:80 miniproject

Testing the API

Run the test script to validate the API:
   python test_api.py

Contact

If you have any questions or need further assistance, please contact me at wxnfifth@gmail.com