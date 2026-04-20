# How to Run the Beginner Code Examples

Welcome to the College Management System beginner tutorials! If you are new to Python and Streamlit, follow these simple steps to run any of the `.py` files in this track.

## Prerequisites

1.  Make sure you have **Python** installed.
2.  Open your terminal or command prompt.
3.  Activate your virtual environment (if you are using one).
4.  Install required packages by running:
    ```bash
    pip install -r requirements.txt
    ```

## Running Streamlit Apps

All the files ending with `.py` (except in the `backend` or `model` folders) are designed to be run as Streamlit web applications.

To run an app, open your terminal, navigate to the folder containing the repository, and use the `streamlit run` command followed by the file path.

**Examples:**

*   To run the very first basics example:
    ```bash
    streamlit run beginner/Unit_1_Streamlit_Fundamentals/1_1_basics.py
    ```
*   To run the interactive UI example:
    ```bash
    streamlit run beginner/Unit_1_Streamlit_Fundamentals/1_2_interactive_ui.py
    ```

After running the command, Streamlit will start a local web server and usually open your default web browser automatically. If it doesn't, it will print a `Local URL` (like `http://localhost:8501`) in the terminal that you can click or copy-paste into your browser.

## Running Flask API (Unit 3 & 4)

Some advanced units like Model Deployment (Unit 3) will require running a backend API separately from a frontend. 
For these, you would first run the Python script normally using `python`:
```bash
python beginner/Unit_3_Model_Deployment/flask_api.py
```
And then in a *new* terminal window, run the frontend:
```bash
streamlit run beginner/Unit_3_Model_Deployment/streamlit_client.py
```

Happy coding!
