import pandas as pd

def shift_datetime(input_file, output_file):
    # Load the CSV file without assuming the first row is a header
    df = pd.read_csv(input_file, header=None)
    
    # Rename the columns appropriately
    df.columns = ["datetime", "value"]
    
    # Convert the datetime column to proper datetime format
    df["datetime"] = pd.to_datetime(df["datetime"], format="%d-%b-%y %H:%M")
    
    # Shift the datetime by one hour
    df["datetime"] = df["datetime"] + pd.Timedelta(hours=2) # Summertime
    
    # Save the updated dataframe to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Shifted datetime saved to {output_file}")

# Example usage
input_file = "data_20250401.csv"  # Replace with your actual file path
output_file = "data_20250401_shifted.csv"
shift_datetime(input_file, output_file)