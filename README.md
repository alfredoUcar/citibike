Full stack code challenge. The task is described in the `.pdf` file at the root of the repository.

# Usage

## Requirements

- Docker
- Docker Compose

## Running the project

### Start the APP

```bash
make up
```

API is available at `http://localhost:8000/` and swagger documentation at `http://localhost:8000/docs`

Front is served at `http://localhost:3000`

### Stop the APP

```bash
make down
```

### Check coverage

Generate html report

```bash
make coverage
```

change `backend/htmlcov/` permissions to access the report without root:

```bash
sudo chown -R $USER backend/htmlcov/
```

> Note: this is needed because docker creates the files with root permissions by default.

open report in browser

```bash
xdg-open backend/htmlcov/index.html
```


# Approach step by step

## 1) Understand the problem

The first thing is to read the statement, understand the problem and extract first TODOs. What are the needs? What are the constraints? What are the inputs and outputs? What are the expected results? Observations?

First thoughts and TODOs:
- Full challenge description seems an ETL-like process. Mandatory part is about extracting data from CSV files, transforming it and serving it through an API.
- There's optional part.
  - I'll focus on the mandatory part first. But I'll keep the optional part in mind.
- No authentication is required.
- Backend and frontend should be developed.
  - Since FastAPI is mandatory for backend I'will probably discard fullstack monorepo approach and use Headless like architecture.
- Tool must run both on reviewer's machine and production environment.
  - A containerized solution might be a good choice. I will use Docker.
- Code quality is important.
  - I will use a linter and a formatter that make me easier to follow standards such as PEP8 rules and pythonic code.
    - TODO: setup linter and formatter.
  - I will follow clean code and SOLID principles.
  - Assumption: DDD, CQRS and Event Sourcing or hexagonal architecture are probably overkill for this challenge. They fit better on complex systems and larger teams. But I can use some of their principles to make the code more maintainable if needed.
- Architecture:
  - Initially I'm considering keep backend and frontend in the same repository but in different folders to make it easier to manage. Using docker compose to run both services.
  - TODO: setup base project structure with backend and frontend folders.
  - TODO: Init FastAPI project as a docker container in backend folder.
- Tests are important.
  - I should consider unit tests for the backend and frontend and maybe some integration or e2e tests.
  - I will use a coverage tool to ensure that at least 80% of the code is covered by tests.
  - TODO: plan testing tools and strategies like TDD.
- Data validation is important.
  - I will consider using Pydantic for backend and maybe some form validation library for frontend.
- Error handling is important.
  - I will use a logger to keep track of errors and warnings.
  - I will consider a monitoring tool to keep track of the system's health such as Prometheus and Grafana.
  - TODO: plan observability tools.
- Datasets are provided as links to zip files with timestamp as filename.
  - TODO: check the content of the zip files. Are there any other files than CSV? How are the CSV files structured? Is data sorted and/or grouped? How are files named?
- No specifications about system requirements: CPU, memory, disk, network, etc. Both for server and client.
  - TODO: ask the interviewer.
  - Assumption: it will be deployed probably on a cloud service so it could be scaled up if needed but it should be optimized to keep costs low. Client should be able to run on a common laptop or desktop, i'll discard mobile devices.
- No specifications about the expected response time.
  - TODO: ask the interviewer.
  - Assumption: At least it should not raise timeout errors.
- Should data be served on-demand or could it be pre-processed and stored?
  - Assumption: since there are no restrictions, I can take advantage of this ambiguity and postpone this decision until later and use the option that is most convenient.
- Is the system expected to handle concurrency and fault tolerance under high load situations?
  - Assumption: As per "questions to resolve" high load is part of theorical scenarios but not expected in practice.


## 2) Datasets analysis

I assume that datasets filenames indicate the year and some of them also the month of the data they contain. I downloaded a couples of files to confirm this assumption.

Noticed there are data from June 2013 to January 2025 distributed in different files. There are three types of datasets by filename pattern available to download as zip files:
1. `YYYY-citibike-tripdata.zip` (with full year data from 2013* to 2023)
   1.  *checking dataset content 2013 is not a full year. It contains data from June to December.
2. `YYYYMM-citibike-tripdata.zip` (with monthly data from 2024-01 to 2025-01)
3. `JC-YYYYMM-citibike-tripdata.csv.zip` (with monthly data from 2015-09 to 2025-01)

Datasets of type 2 and 3 overlap in time. Comparing January 2024 datasets seems that JC contain less data than the other. I will prioritize dataset 2 over 3.

Given that API must handle Year(mandatory) and Month(Optional) as query parameters I will apply the following strategy to select which dataset to download:

- if only year is provided and less than 2024 I will download the file `YYYY-citibike-tripdata.zip` of dataset 1.
- if only year is provided and greater than 2023 I will download all files from dataset 2 matching the year.
- if month is also provided:
  - if year is 2024 or 2025-01 I will download the file `YYYYMM-citibike-tripdata.zip` of dataset 2.
  - if year is between 2015-09 and 2023 I will download the file `JC-YYYYMM-citibike-tripdata.csv.zip` of dataset 3.
  - if it's before 2015-09 I will download the file `YYYY-citibike-tripdata.zip` of dataset 1 that matches the year. **Considerations**: it will include more data than needed but it's the only option available. As a second iteration I could filter the data to return only the requested month.
  - if it's before 2013 or after 2025-01 I will return an error message.


## 3) Initial backend setup

Prepare backend folder structure and setup FastAPI project using Docker. Just a simple "Hello World" for now.

```
/project-root
│── /backend
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│── docker-compose.yml
│── Makefile
│── README.md
```

I will use docker-compose so I can easily add the frontend service later.

At this point I'm able tu run the backend service by running `make up` and access it at `http://localhost:8000/`

## 4) Setup linter and formatter

Setup commands `make lint`,`make lint-fix` and `make format` to run linter and formatter with ruff and black.

## 5) Setup testing tools

Install `pytest` and `pytest-cov` to run tests and coverage.
Setup commands `make test` whith coverage as text output and `make coverage` to generate coverage html report.

Coverage report is available at `backend/htmlcov/index.html` but it's only accesible as root user because docker creates the files with root permissions. I will consider to fix this later.

## 6) TDD for API

Started developing API functionality in a TDD way. Incrementally adding tests and code based on strategy defined in step 2.

The plan is to create a route `/download` that receives `year` and `month` as query parameters and returns a file with the requested data.

Initially I will return a simple message with the requested parameters as a placeholder before implementing the download logic.

The first logic I would implement is to check if date is out of range and return an error message. The reason is that it's easier to test because I don't need to download the files to check if the logic is working and it's a good practice to handle errors first.

## 7) Proof of Concept, download a file

During the development I take a moment to test a simple download without any logic to check if it's working.

Regardless of parameters I will download the file `2013-citibike-tripdata.zip` to test the download. The point is to check if it starts downloading the file when I access the route.

Added something like this to the route:

```python
    file_url = "https://s3.amazonaws.com/tripdata/2013-citibike-tripdata.zip"

    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(filepath, "wb") as file:
            shutil.copyfileobj(response.raw, file)

        return FileResponse(filepath, filename=filename, media_type="application/zip")
```

Tested it with largest files and even it worked I noticed that it's not a good idea to download the file to the server before sending it to the client. It takes too much time before the download starts and it's not a good practice to store files on the server that are not needed. It's better to stream the file directly from the source to the client.

## 8) Streaming file to client

Let's iterate the previous test to see if I can stream the file directly to the client.

```python
    file_url = "https://s3.amazonaws.com/tripdata/2013-citibike-tripdata.zip"

    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        return StreamingResponse(response.iter_content(chunk_size=1024), media_type="application/zip", headers={"Content-Disposition": f"attachment; filename={filename}"})
```

It works fine so I will keep this approach.

## 9) Download the right file

Now I will resume the step 6 and use TDD to implement the logic to download the right file based on the query parameters.

## 10) Model to handle params validation

Refactor to extract params validation to a pydantic model and keep endpoint code cleaner (single responsability).

## 11) Service to resolve dataset url

Although I had not yet written all the logic, I saw that the endpoint was getting long and had too many responsibilities. So I have also moved to a service the responsibility of calculating which url to use.

This way the endpoint only has to execute the download

## 12) Last case

At this point I have already solved almost all the cases.

Let's summarize what we have so far:

An endpoint `GET /dataset/` which does the following:

- Delegates to the model that the range of requests is between 2013 and 2025 (with or without month)

- Runs a service that tells me the url of the dataset that I have to download according to the strategy that I defined in step 2, except for one exception*.

- Proceeds with the streaming download.

*The only case that I have not resolved yet is when the full year 2024 is requested. It is special because it is the only case where I have to download more than one file at a time, that is why I left it for last.


## 13) Partially solved

Adapted url resolver to return a list of urls and instead of a single url. This way I can handle also requests for full year 2024.
In that case it return 12 urls, one for each month.

Adapted route controller to add another handler in case of multiple urls that downloads all of them into a single zip file.
The problem is it fails before finish while debug logs show that it fails after download the first 4-5 individual files, even with streaming approach.

Error log:

```bash
backend_1  |     | requests.exceptions.ConnectionError: HTTPSConnectionPool(host='s3.amazonaws.com', port=443): Max retries exceeded with url: /tripdata/202404-citibike-tripdata.csv.zip (Caused by NameResolutionError("<urllib3.connection.HTTPSConnection object at 0x7ff503dc0640>: Failed to resolve 's3.amazonaws.com' ([Errno -5] No address associated with hostname)"))
```

Probably I'm getting banned due to a rate limit.

As an experiment if a test to limit download up to the first 4 files only it works fine. Takes more time than in other cases but downloads finish successfully and data is correct.

I'm considering to apply delays between requests or use a session to reuse connections. Anyway I'will park it here in order to advance with frontend part. This will remain as a TODO for later.

## 14) Setup frontend

Let's init a next.js project in `frontend/` dir. I know it's fullstack framework and might be more than needed but it's easy to use, include lots of useful presets such as linters or tailwind. Also I have experience with it and prefer to go with something familiar.

Add Dockerfile and update `docker-compose.yml` to add frontend service.

Checked config by running `make up` then `docker compose ps` to ensure both services are up and running. Finally open `localhost:3000` to see the next.js default homepage.

## 15) Customize with dataset form

Created a simple form that calls a frontend service which requests data to backend API.
Had to config CORS in backend so it allows requests from frontend (localhost:3000). That only works in development. It should adjusted for production.

## 16) Progress bar

Download works fine but there's no visual feedback during the download. After that it finally shows the dialog to save it on your device but it takes a minute before that.

Let's use Axios `onDownloadProgress` option to get updates so UI can be updated.
To make it work I had to specify Content-Length on response headers in backend.

## 17) Improve UI

Make inputs selectors.

![alt text](image.png)


# Pending work and final thoughts


In addition to the optional bonus, which I haven't done, I think there are some improvements that would have been interesting.

This is what I would have prioritized if I had spent more time on it:

- Better configure the "linter" and testing tools on the front. Tests on the front and a little more coverage on the backend.

- Better process the data for the year 2024, when the entire year is downloaded it fails halfway through the process.

- Filter the search by month when the request is prior to 2015-09, since in these cases I download the entire year.

- Set up the build of a production-optimized docker image (no test code or development dependencies). I probably would have used "service profiles"

- Once everything was well covered by test I would have refactored the code to make it cleaner.

# Questions to resolve (theorical part)

## Scalability  
- **Caching with Redis**: could be used for most demanded datasets.  
- **Load balancing with Nginx**: Spreads traffic across multiple FastAPI instances.  
- **Message queues (RabbitMQ or Kafka)**: Handles asynchronous requests efficiently.
- **Microservice**: Expensive processes such as filtering or merging datasets could be consumed from the asynchronous queue and processed by a microservice that has more resources or that uses some more specialized technology for that task.

## Monitoring  
- **Prometheus + Grafana**: Tracks API latency and errors.  
- **Structured logs**: Using tools like the ELK Stack for better visibility.  

# Security (Authentication)  

I would use **JWT (JSON Web Tokens)**. It's simple and stateless, no need to store sessions.
