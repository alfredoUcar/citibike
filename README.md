Full stack code challenge. The task is described in the `.pdf` file at the root of the repository.

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
  - Seems like a containerized solution is a good choice. I will use Docker.
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

