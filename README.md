# Application that allows authenticated users to upload files of any size (hardware resources permitting)

## Setup Instructions:

- Clone the repository and navigate to the root directory
- Run `docker-compose up --build` to build and start the services (api & web)
- Run `docker compose ps` to check the status of the services (web should be up, api should be up and healthy)
- More specific instructions can be found in the README.md files in the frontend and backend directories

## Usage Guide:
- FastAPI Docs page is available at `http://localhost:8000/docs`
- Web app is available at `http://localhost:8080`
- Example of usage scenario:
  - Open two browser sessions (or tabs) and login with different credentials (test, guest)
  - Upload files in one session and observe the notifications in the other session

## Notes
- Used a single docker image for both api and test containers
- HTTP Basic Auth is used for authentication
  - The following credentials are available:
    - Username: `guest`, Password: `guest`
    - Username: `test`, Password: `test`
  - The auth on FE side works in similar way to the FastAPI docs page (storing headers in local storage)
- Websocket connection is used to notify clients about uploaded file events
- Files are stored in the API container filesystem (docker volume)
  - Resumable is used to upload files in chunks
  - Volume can be inspected using `docker volume inspect virtuo-app_uploaded-files-data` command
  - Files are stored in `./uploaded_files` directory
    - To view files in container filesystem, run `docker compose exec -it api ls -lah /home/user/app/uploaded_files`
- File storage is shared between users, so all users can see all files and overwrite them if they have the same name
- Client app is written using plain JS and HTML
  - To serve the client app, a simple python server is used
