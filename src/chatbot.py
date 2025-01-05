import os
import yaml
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Load data and parameters
def load_data(data_path):
    """
    Load the dataset for the chatbot to reference.
    
    Args:
        data_path (str): Path to the CSV data file.
        
    Returns:
        pandas.DataFrame: Loaded dataframe.
    """
    return pd.read_csv(data_path)

def load_parameters(param_path):
    """
    Load parameters from the YAML configuration file.
    
    Args:
        param_path (str): Path to the YAML parameter file.
        
    Returns:
        dict: Parameters dictionary.
    """
    with open(param_path, 'r') as file:
        return yaml.safe_load(file)

# Preprocess data for chatbot context
def preprocess_data(df):
    """
    Generate summary statistics and key insights from the data.
    
    Args:
        df (pandas.DataFrame): The loaded dataframe.
        
    Returns:
        str: A summary string for the chatbot's context.
    """
    summary = df.describe(include='all').to_string()
    return f"Here is the dataset summary:\n{summary}"

# Chatbot setup
def initialize_chatbot(model_name="gpt2"):
    """
    Initialize the language model for the chatbot.
    
    Args:
        model_name (str): Name of the Hugging Face model to use.
        
    Returns:
        pipeline: Hugging Face conversational pipeline.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    # Add a pad token if needed
    tokenizer.pad_token = tokenizer.eos_token
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

# Chatbot query handling
# Chatbot query handling
def chatbot_query(chatbot, context, user_query):
    """
    Handle a user query using the chatbot.

    Args:
        chatbot (pipeline): The initialized chatbot pipeline.
        context (str): Context for the chatbot.
        user_query (str): User's query string.

    Returns:
        str: Chatbot response.
    """
    input_text = f"Context: {context}\nUser Query: {user_query}\nAnswer:"
    response = chatbot(
        input_text,
        max_new_tokens=3000,  
        num_return_sequences=1,
        truncation=True,
        pad_token_id=chatbot.tokenizer.eos_token_id
    )
    return response[0]['generated_text'].split("Answer:")[-1].strip()


# Main function
if __name__ == "__main__":
    # File paths
    data_path = "data/processed/data.csv"  # Update with your actual data path
    param_path = "conf/parameters.yaml"

    # Load data and parameters
    if not os.path.exists(data_path) or not os.path.exists(param_path):
        print("Data or parameters file is missing. Please check paths.")
        exit()
    df = load_data(data_path)
    parameters = load_parameters(param_path)
    
    # Prepare chatbot context
    context = preprocess_data(df)
    price_change_range = parameters.get("price_change_range", "Not specified")
    context += f"\nPrice change range is ±{price_change_range * 100}%.\n"

    # Initialize chatbot
    print("Initializing chatbot...")
    chatbot = initialize_chatbot()

    # Start chatbot interaction
    print("Chatbot is ready! Type 'exit' to quit.")
    while True:
        user_input = input("\nAsk a question: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = chatbot_query(chatbot, context, user_input)
        print(f"\nChatbot: {response}")
