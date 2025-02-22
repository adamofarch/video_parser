## Overview

This project is a Django-based web application that allows users to upload videos, extract subtitles from the videos using `ccextractor` binary, and perform keyword searches within the extracted subtitles. The application leverages Celery for asynchronous task processing.

## Technologies Used

- **Django**: Web framework for building the application.
- **Celery**: Asynchronous task queue for processing video files and subtitle extraction.
- **ccextractor**: Tool for extracting subtitles from video files.
- **Django Environ**: Library for managing environment variables.

## Features

- **Video Upload**: Users can upload video files through the web interface.
- **Subtitle Extraction**: Extracts subtitles from uploaded videos asynchronously using Celery and `ccextractor`.
- **Translation of subtitles**: Traslating subtitles into langugaes requied.
- **Keyword Search**: Allows users to search for keywords within the subtitles and returns corresponding timestamps.
- **Scalability**: Utilizes Celery for handling multiple video processing tasks concurrently.

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/adamofarch/video_parser.git
   cd video_parser

2. **Create and Activate a Virtual Environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt

4. **Install ccextractor binary**:
   - Note: It is highly recommended build ccextractor from source, You can Follow the **[Compilation Instructions](https://github.com/CCExtractor/ccextractor/blob/master/docs/COMPILATION.MD)**
   - Note for Arch Users: You can also install ccextractor from AUR using your favourite AUR helper

   Follow the Installation guide on **[CCExtractor/ccextractor](https://github.com/CCExtractor/ccextractor)** to install on your operating system.


5. **Run Migrations**:
   ```sh
   python manage.py migrate

6. **Start the Development Server**:
   ```sh
   python manage.py runserver

7. **Start Celery Worker**:
   ```sh
   celery -A video_parser worker -l INFO

## Usage

   1. **Upload a Video**:
      - Navigate to the home page and upload a video file.
      - The video will be processed asynchronously and subtitles will be extracted.

   2. **Search Subtitles**:
      - Enter a keyword in the search form to find the corresponding timestamps in the video where the keyword appears in the subtitles.

## Backend Capabilities

   - **Asynchronous Processing:** Leveraging Celery, the application can handle multiple video uploads and subtitle extraction tasks concurrently, ensuring a responsive user experience.
   - **Efficient Searching:** Storing subtitles in allows for fast keyword searches, providing users with quick and accurate results.

## Contributing 

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.
