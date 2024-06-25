Sure, here is an example of a `README.md` file for your project:

```markdown
# AI Chat Interface for MySQL Database

Welcome to the AI Chat Interface for MySQL Database! This project allows users to interact with a MySQL database using natural language queries. It uses OpenAI's GPT-3.5 to generate SQL queries and visualizes the results using Plotly and Streamlit.

## Project Structure

```
my_app/
|-- .env
|-- main.py
|-- config.py
|-- database.py
|-- openai_utils.py
|-- intents.py
|-- requirements.txt
```

## Files Description

- **`.env`**: Contains environment variables for database and OpenAI API keys.
- **`main.py`**: The main Streamlit app script.
- **`config.py`**: Loads environment variables.
- **`database.py`**: Handles database connections and queries.
- **`openai_utils.py`**: Manages interactions with OpenAI API.
- **`intents.py`**: Defines intents and valid columns.
- **`requirements.txt`**: Lists all the dependencies required for the project.

## Setup Instructions

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Create a `.env` File**:
   Create a `.env` file in the root directory with the following content:
   ```
   MYSQL_HOST=your_remote_mysql_host
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=your_database_name
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Run the Streamlit App**:
   Navigate to your project directory and run the Streamlit app using the following command:
   ```sh
   streamlit run main.py
   ```

## Usage

### Asking Questions
Enter your question about the database in natural language in the input box and press "Submit". The application will:
1. Generate an appropriate SQL query using OpenAI's GPT-3.5.
2. Execute the query on the MySQL database.
3. Display the results in a table.
4. Visualize the data if applicable.

### Example Queries
Here are some example queries you can try:
- "What is the total revenue by listing state?"
- "Which are the top 10 SKUs by total profit?"
- "Can you show me the monthly revenue trend?"
- "What are the top 5 ASINs by total ordered items?"
- "Can you create a graph that shows the difference in revenue by listing state?"

### Viewing Table Structure
Click on the "Show Table Structure" button to see the structure of the `aggregate_profit_data` table.

## Notes
- The app uses the default table name `aggregate_profit_data`.
