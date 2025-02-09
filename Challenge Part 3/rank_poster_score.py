import pandas as pd

def rank_posters(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # First calculate total score for each poster (sum of both judges)
    poster_stats = df.groupby('Poster Number').agg({
        'Total': 'sum',
        'Innovation': 'mean',
        'Clarity': 'mean',
        'Presentation': 'mean'
    }).reset_index()
    
    # Sort posters based on criteria in descending order
    sorted_posters = poster_stats.sort_values(
        by=['Total', 'Innovation', 'Clarity', 'Presentation'],
        ascending=[False, False, False, False]
    )
    
    # Create continuous (dense) ranking starting from 1
    dense_rank = 1
    prev_values = None
    ranks = []
    
    # Custom ranking logic: if the current poster's scores differ from the previous one,
    # increment the dense_rank by 1. Otherwise, keep the same rank.
    for _, row in sorted_posters.iterrows():
        current_values = (row['Total'], row['Innovation'], row['Clarity'], row['Presentation'])
        
        if prev_values is not None and current_values != prev_values:
            dense_rank += 1
        
        ranks.append(dense_rank)
        prev_values = current_values
    
    sorted_posters['Rank'] = ranks
    
    # Create a dictionary to map poster numbers to ranks
    rank_mapping = dict(zip(sorted_posters['Poster Number'], sorted_posters['Rank']))
    
    # Add rank column to original DataFrame
    df['Rank'] = df['Poster Number'].map(rank_mapping)
    
    # Save to new Excel file
    df.to_excel(output_file, index=False)
    
    # Print rankings for verification
    print("\nRanking Summary:")
    summary = sorted_posters.sort_values('Rank')[['Poster Number', 'Total', 'Innovation', 'Clarity', 'Presentation', 'Rank']]
    print(summary.to_string(index=False))
    
    return df

# Example usage:
input_file = "output_for_part3.xlsx"  # Replace with your input file path
output_file = "poster_rankings.xlsx"  # Replace with desired output file path

# Run the ranking
result = rank_posters(input_file, output_file)
