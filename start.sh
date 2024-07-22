if [ -z "$PORT" ]; then
  PORT=8501
fi

streamlit run main.py --server.port $PORT
