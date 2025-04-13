import pandas as pd
import numpy as np
import argparse
import sys

def calculate_stats(file_path):
    """
    Process a CSV file and calculate max and mean for each numeric column.
    
    Args:
        file_path: Path to the CSV file to process
        
    Returns:
        DataFrame with statistics for each numeric column
    """
    try:
        # Read the CSV file
        print(f"Reading file: {file_path}")
        df = pd.read_csv(file_path)
        
        # Get column information
        print(f"Total columns: {len(df.columns)}")
        print(f"Columns: {', '.join(df.columns)}")
        
        # Find numeric columns
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        print(f"Found {len(numeric_columns)} numeric columns: {', '.join(numeric_columns)}")
        
        if not numeric_columns:
            print("No numeric columns found in the file.")
            return None
        
        # Calculate statistics for each numeric column
        stats = pd.DataFrame(index=numeric_columns, columns=['Max', 'Mean', 'Min', 'Median', 'Count'])
        
        for col in numeric_columns:
            # Filter out non-numeric values that might still be in numeric columns
            numeric_values = pd.to_numeric(df[col], errors='coerce')
            valid_values = numeric_values.dropna()
            
            if len(valid_values) > 0:
                stats.at[col, 'Max'] = valid_values.max()
                stats.at[col, 'Mean'] = valid_values.mean()
                stats.at[col, 'Min'] = valid_values.min()
                stats.at[col, 'Median'] = valid_values.median()
                stats.at[col, 'Count'] = len(valid_values)
            else:
                stats.at[col, 'Max'] = np.nan
                stats.at[col, 'Mean'] = np.nan
                stats.at[col, 'Min'] = np.nan
                stats.at[col, 'Median'] = np.nan
                stats.at[col, 'Count'] = 0
        
        return stats
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Calculate statistics for numeric columns in a CSV file')
    parser.add_argument('file', help='Path to the CSV file to process')
    parser.add_argument('--output', '-o', help='Output file path (default: print to console)')
    
    # Parse arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    # Calculate statistics
    stats = calculate_stats(args.file)
    
    if stats is not None:
        # Display results
        print("\nStatistics for numeric columns:")
        print(stats.to_string(float_format="{:.6f}".format))
        
        # Save to file if output is specified
        if args.output:
            stats.to_csv(args.output)
            print(f"\nStatistics saved to {args.output}")

if __name__ == "__main__":
    main()