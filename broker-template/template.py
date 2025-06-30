import pandas as pd

# Sample data - you can replace this with your own logic or input source
data = [
    ["CNE000001", "000538.ZK", "YUNNAN F", "S", "3/15/2022", "3/15/2022", "CNY", 78.49, 80000, 6279200, 4395.44, 6961.75, 6267843, "CBHKE", "CITIBANK HK A/C PBG HK"],
    ["CNE100002", "002714.ZK", "MUYUAN F", "S", "3/15/2022", "3/15/2022", "CNY", 52.61, 121687, 6401953, 4481.37, 7097.85, 6390374, "CBHKE", "CITIBANK HK A/C PBG HK"],
    ["AU0000001", "YAL.AX", "YANCOAL", "S", "3/15/2022", "3/17/2022", "AUD", 4.2767, 58724, 251144.9, 125.57, 1094.8, 250019.4, "CBHKE", "CITIBANK HK A/C PBG HK"],
]

columns = [
    "ISIN/IISIN", "Ticker", "Security Description", "Buy/Sell",
    "Trade Date", "Settlement Date", "Currency", "Price", "Quantity",
    "Principal", "Commission", "Total Market Charges", "Net Money",
    "Account", "Account Name"
]

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Save to Excel
output_path = "trade_data_report.xlsx"
df.to_excel(output_path, index=False)

print(f"Excel file saved at: {output_path}")
