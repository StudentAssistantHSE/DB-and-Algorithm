def get_top_indexes(row):
    row_values = row[row.index != row.name]  # exclude the row number
    row_values = row_values[row_values > 0]
    top_values = row_values.nlargest(5)  # get the top 4 highest values
    return top_values.index.tolist()
