uvicorn backend.app:app --log-config=log_conf.yaml &
UVICORN_PID=$!

# Wait for uvicorn to start (you can adjust the sleep duration as needed)
sleep 5

# Check if uvicorn is still running
if kill -0 $UVICORN_PID 2>/dev/null; then
    echo "UVicorn started successfully, launching Streamlit"
    streamlit run frontend/LEGO_employee_chatbot.py
else
    echo "UVicorn failed to start. Aborting."
fi