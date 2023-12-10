uvicorn backend.app:app --reload &
sleep 5
streamlit run frontend/LEGO_employee_chatbot.py
