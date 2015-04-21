# Interview Questions Application

## Usage:

This app allows an ARC staff employee to log in and create a list of questions for potential new hires. The application supports moving these questions into categories and assigning each question a few tags to identify them quickly, and organize them easily. (Markdown format is supported for questions)

Once organized into a category, users can append more questions, or select one of two printout views (staff / applicant copies) which render the list of questions into an organized, markdown-supported raw HTML format for easy printing.

## Installation:

Clone the repository into a directory

    git clone https://github.com/ssean1/interview-questions.git

Set up a virtual environment in the app's root directory

    virtualenv --no-site-packages -p python3 .env
    source .env/bin/activate

Install & run the server

    make install && make
