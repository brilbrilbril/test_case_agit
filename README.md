# TEST CASE RAG AGIT 

**This is my answer about test case from AGIT. I built chatbot RAG system to do question answering about Isuzu vehicle. Please read this until the end.**

I use OpenAI API for the LLM, so make sure you have the API key (paid) to run and use this program.

## Weakness for future improvement
1. The output is not in streaming mode yet.
2. There is no picture of each vehicle.
3. The retrieval only retrieve 4 vehicles, even though there are 6 documents.

## How to Use
1. Clone this repository to your local.
2. Install the necessary package by executing this command in terminal:

    ``` pip install -r requirements.txt ```

3. (Optional, but recommended) create python virtual environment by executing this command on terminal:

    ``` python -m venv venv ```

    then activate it using:

    ``` venv/Scripts/activate ```

**For point 4-7 I have done it before, so you don't need to follow**

**This is a program to read documents and make the summary each document**

4. Open the preprocess_data.py.
5. Set the OPENAI_API_KEY.
6. You can change the file name or directory of the summary generated later.
7. Execute the command in terminal:

    ``` python preprocess_data.py ```

**Main program**

8. Open the main.py.
9. Set the OPENAI_API_KEY.
10. (Do this if you follow point 4-7) Set __json_path__ the same as your filename and directory you changed/did in point 4-7.
11. Execute this command to run the file:

    ``` streamlit run main.py ```

12. Wait until the localhost address appears, then you will be switched automatically in a web browser or you can copy this link and paste it manually in browser.

    ``` http://localhost:8501/ ```


**Example input and output**
![image](https://github.com/user-attachments/assets/8651f6c5-3484-4e6d-966c-e58df834d036)
![image](https://github.com/user-attachments/assets/e98b3708-8301-4365-a0cd-30e3f7c0d336)
![image](https://github.com/user-attachments/assets/ce1631d8-5ab4-4935-ad0a-f5c914202b17)
![image](https://github.com/user-attachments/assets/661f33a6-0d8e-4238-b6b9-f4af90986a49)
![image](https://github.com/user-attachments/assets/2b928b2e-c3ee-4c63-bb38-6f112fcf9c31)
![image](https://github.com/user-attachments/assets/7c2fdcb6-a009-408d-a936-30e7a685bf4f)
![image](https://github.com/user-attachments/assets/582add9e-0660-4f09-a43d-218de389e6e9)






