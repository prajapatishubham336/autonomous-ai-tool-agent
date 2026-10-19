# autonomous-ai-tool-agent
An autonomous AI agent built with Python, LangChain, and Groq that uses LLM-powered tool calling to check product inventory and calculate shipping costs based on user queries.


# 🤖 Autonomous AI Tool Agent

An intelligent, tool-using AI agent built with **Python, LangChain, and Groq**. This project demonstrates how a large language model (LLM) can interpret user requests, select appropriate custom tools, execute operations, and generate responses using the results.

The agent currently supports two practical operations: **product inventory lookup** and **shipping cost estimation**. Instead of relying only on generated text, it can invoke Python functions to retrieve predefined stock information or calculate shipping costs.

---

## 🚀 Features

- **LLM-Powered Agent:** Uses a language model to understand user requests and determine whether a tool is needed.
- **Custom Tool Integration:** Defines Python tools using LangChain's `@tool` decorator.
- **Product Inventory Lookup:** Checks predefined stock information for supported products.
- **Shipping Cost Calculator:** Estimates shipping costs based on package weight and delivery distance.
- **Tool Calling:** Connects the language model with custom Python functions through LangChain.
- **Tool Result Processing:** Returns tool results to the model using `ToolMessage`.
- **Automated Execution Flow:** Runs a request, executes any tool calls returned by the model, and generates a final response.
- **Environment Variable Configuration:** Loads the Groq API key from a `.env` file or the environment.
- **Console-Based Interface:** Demonstrates the agent with sample queries in a Python script.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and custom tool implementation |
| LangChain | Tool definitions and agent interaction workflow |
| `langchain-groq` | Connects LangChain to Groq-hosted language models |
| `langchain-core` | Provides messages and the `@tool` decorator |
| Groq API | Language model inference and tool-call generation |
| `python-dotenv` | Loads environment variables from `.env` |
| Custom Python functions | Perform shipping calculations and inventory lookup |

---

## 🧠 How It Works

The agent follows a tool-calling workflow:

1. The user submits a question.
2. The application initializes the Groq language model.
3. LangChain binds the available custom tools to the model.
4. The model processes the user's query and may request one or more tools.
5. The application identifies each requested tool and passes its arguments to the corresponding Python function.
6. The tool executes and returns a result.
7. The result is added to the conversation as a `ToolMessage`.
8. If tool calls were returned, the model is invoked again to generate a final response using the tool results.

### Architecture

```text
User Query
    |
    v
Groq LLM via LangChain
    |
    v
Tool Selection
    |
    +---------------------------+
    |                           |
    v                           v
Shipping Cost Calculator   Product Stock Lookup
    |                           |
    v                           v
Shipping Estimate          Inventory Result
    |                           |
    +-------------+-------------+
                  |
                  v
             ToolMessage
                  |
                  v
          LLM Final Response
                  |
                  v
              User Output
```

**Important:** The current implementation performs one round of tool execution and then makes one follow-up model call. It does not implement an unlimited autonomous loop.

---

## 🔧 Available Tools

### 1. Shipping Cost Calculator

Function: `calculate_shipping_cost(weight_kg, distance_km)`

Calculates an estimated shipping cost using the following formula:

```text
Shipping Cost = Base Rate + (Weight × 1.5) + (Distance × 0.05)
```

The current base rate is `$5.00`.

**Example:**

For a package weighing 2.5 kg traveling 450 km:

```text
Base rate   = $5.00
Weight cost = 2.5 × 1.5 = $3.75
Distance    = 450 × 0.05 = $22.50

Estimated total = $31.25
```

The function returns the estimated cost formatted to two decimal places.

*Note: This is a demonstration formula, not a real carrier quotation or production shipping tariff.*

### 2. Product Stock Checker

Function: `get_product_stock(product_name)`

Checks a predefined inventory dictionary using case-insensitive substring matching.

| Product | Inventory Status |
|---|---|
| Sony WH-1000XM5 | In Stock — 15 units |
| Logitech MX Master 3S | Low Stock — 3 units |
| Mechanical Keyboard | Out of Stock |

If a product does not match a known entry, the function reports that it was not found in the inventory database.

*Note: Inventory data is hard-coded for demonstration purposes and is not connected to a live store or database.*

---

## 📁 Project Structure

```text
autonomous-ai-tool-agent/
│
├── main.py             # Main agent and custom tool definitions
├── requirements.txt    # Python dependencies
├── .env                # Private Groq API key (not committed)
├── .gitignore          # Files excluded from Git
└── README.md           # Project documentation
```

The filename `main.py` is a suggested name for the supplied script. If your file has a different name, keep your actual filename and use it in the run command.

---

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or newer recommended.
- An internet connection.
- A Groq API key.
- Basic familiarity with Python and command-line tools.

### 1. Clone the Repository

```bash
git clone https://github.com/prajapatishubham336/autonomous-ai-tool-agent.git
cd autonomous-ai-tool-agent
```


### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Create a `requirements.txt` file:

```text
langchain-groq
langchain-core
python-dotenv
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API Key

Create an API key through the [Groq Console](https://console.groq.com/).

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your actual key.

**Security:** Never upload your `.env` file or expose your API key in source code, screenshots, or public repositories.

### 5. Run the Agent

If your script is named `main.py`, execute:

```bash
python main.py
```

The program will run the two example queries included in the script and print the agent's responses in the terminal.

---

## 💬 Example Queries

### Example 1: Check Product Availability

**User query:**

```text
Can you check if the Logitech MX Master 3S is currently in stock?
```

The model can select the `get_product_stock` tool, which returns:

```text
Stock status for 'Logitech MX Master 3S':
Low Stock (3 units available)
```

The language model then generates a response based on the tool result.

### Example 2: Calculate Shipping Cost

**User query:**

```text
How much will it cost to ship a 2.5 kg package
across a distance of 450 km?
```

The model can select `calculate_shipping_cost` and supply the weight and distance.

Expected calculation result:

```text
The estimated shipping cost is $31.25
```

The exact wording of the final AI response may vary.

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | Authenticates requests to the Groq API |

The model name `openai/gpt-oss-120b` is specified directly in the source code. Make sure it is available to your Groq account before running the application.

---

## 📌 Current Limitations

- The inventory is stored in a static Python dictionary.
- Shipping rates use a demonstration formula and do not reflect live carrier prices.
- The application runs in the terminal and does not include a web UI.
- Tool results are not persisted in a database.
- The current execution flow supports a single tool-calling round followed by a final model response.
- There is no built-in user authentication or authorization layer.
- Tool arguments and tool execution should be validated more thoroughly before production use.
- The agent depends on the configured Groq model supporting the required tool-calling behavior.

---

## 🚧 Future Enhancements

Possible future improvements include:

- Add a Streamlit or FastAPI interface.
- Connect inventory lookups to a real database or inventory API.
- Integrate live shipping carrier APIs.
- Implement a bounded agent loop for multiple rounds of tool calls.
- Add tool argument validation and execution safeguards.
- Introduce structured logging and automated tests.
- Add additional tools for order tracking, delivery estimates, and product information.
- Implement configurable model selection.
- Add Docker support and a CI/CD workflow.

These are potential improvements, not existing features.

---

## 🔒 Security Best Practices

- Keep API keys in environment variables or a secret manager.
- Add `.env` and virtual environment folders to `.gitignore`.
- Validate user input and model-generated tool arguments.
- Restrict tools to explicitly allowed functions.
- Apply appropriate timeouts, rate limits, and error handling.
- Avoid exposing secrets or sensitive information in logs.
- Treat model-generated tool calls as untrusted input.

### Recommended `.gitignore`

```gitignore
.env
.env.*
!.env.example

venv/
.venv/
env/

__pycache__/
*.py[cod]

.pytest_cache/
.DS_Store
Thumbs.db
```

---

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a pull request with a clear description.

Please ensure that API credentials and other secrets are never included in commits.

---

## 📄 License

No license is currently specified. Add a `LICENSE` file before distributing or permitting reuse of the project. Choose a license that matches your intended terms of use.

---

## 👨‍💻 Author

**Shubham Prajapati**

AI/ML Engineer | Machine Learning | Generative AI

GitHub: [@prajapatishubham336](https://github.com/prajapatishubham336)

---

## ⭐ Support

If you find this project useful for learning about LLM tool calling and AI agents, consider starring the repository on GitHub.

**Build smarter applications with AI agents and custom tools.**
