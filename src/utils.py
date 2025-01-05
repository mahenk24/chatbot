import yaml
import pandas as pd


def read_parameters(file_path):
    """
    Reads the model parameters from the parameters.yaml file.
    
    Parameters:
    file_path (str): Path to the parameters.yaml file.
    
    Returns:
    dict: A dictionary containing the parameters.
    """
    with open(file_path, 'r') as file:
        params = yaml.safe_load(file)
    return params

def extract_coefficients(model_results):
    """
    Extracts the coefficients from the trained econometric model.

    Parameters:
    model_results (statsmodels.regression.linear_model.RegressionResultsWrapper): The fitted model results object.

    Returns:
    pandas.DataFrame: A dataframe containing the coefficient names and their values.
    """
    # Extract coefficients
    coefficients = model_results.params
    
    # Convert to DataFrame for easier interpretation
    coeff_df = coefficients.reset_index()
    coeff_df.columns = ['Coefficient', 'Value']
    
    return coeff_df

