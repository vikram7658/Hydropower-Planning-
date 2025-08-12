import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates



# Update Matplotlib parameters
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 12,
    'axes.labelsize': 12,
    'axes.titlesize': 18,
    'legend.fontsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'figure.dpi': 300,
    'figure.figsize': (15, 15),  
    'figure.autolayout': False
})

def read_and_prepare_csv(file_path):
    # Read the CSV and parse the 'Date' column
    df = pd.read_csv(file_path, parse_dates=["Date"])
    df.set_index("Date", inplace=True)
    # Drop duplicate dates to avoid reindexing issues
    df = df[~df.index.duplicated(keep='first')]
    return df

# File paths for the CSVs (update these paths as needed)
file_paths = [
    r"MPBX Data Interpretation/MPBX7.csv",
    r"MPBX Data Interpretation/MPBX8.csv",
    r"MPBX Data Interpretation/MPBX9.csv"
]

# Read and prepare the dataframes (using all available files)
dfs = [read_and_prepare_csv(fp) for fp in file_paths]

# Define the columns for moving average and plotting
data_cells = ['Load1','Load2']  # Note: Ensure these names match your CSV
depth_cols = ['5m','10m', '15m']

# Apply a moving average to the specified columns if they exist
for df in dfs:
    for col in depth_cols:
        if col in df.columns:
            df[col] = df[col].rolling(window=5, min_periods=1).mean()
    for cell in data_cells:
        if cell in df.columns:
            df[cell] = df[cell].rolling(window=5, min_periods=1).mean()

# Define titles for each subplot
MPBX_titles = ['MPBX7', 'MPBX8', 'MPBX9']

# Define event dates with annotations
event_dates = {
    
    pd.to_datetime("03-08-2025", format="%m-%d-%Y").to_pydatetime(): "Earthquake",
    pd.to_datetime("03-05-2025", format="%m-%d-%Y").to_pydatetime(): "TRT widening",
}

# Create a 3-row subplot figure
fig, axs = plt.subplots(3, 1, sharex=False)
axs = axs.flatten()

# Define markers for each plot
marker_list = ['<', 'p', 'v']

# Loop through each subplot and plot the data
for ax, df, title, mark in zip(axs, dfs, MPBX_titles, marker_list):
    # Plot each depth column as a separate line
    for col in depth_cols:
        if col in df.columns:
            sns.lineplot(
                x=pd.to_datetime(df.index), 
                y=df[col],
                linestyle='--', 
                marker=mark,
                label=f'Loc {col},',
                ax=ax
            )
    
    # Add vertical lines with event annotations
    for ev_date, ev_detail in event_dates.items():
        ax.axvline(x=ev_date, color='blue', linestyle='--', linewidth=0.8)
        ylim = ax.get_ylim()
        ax.text(ev_date, ylim[0], f' {ev_detail}', rotation=90,
                verticalalignment='bottom', fontsize=15, color='black')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.set_ylabel('Vertical Displacement (mm)')
    ax.set_title(title)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.legend()
    plt.setp(ax.get_xticklabels(), rotation=45)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('MPBX_for_PH_wall_NE.png', dpi=300, bbox_inches='tight')
plt.show()


#%% For data cell 
# Create a 2x2 subplot figure
fig, axs = plt.subplots(3, 1, sharex=False)
axs = axs.flatten()
# depth_cols = [ '10m', '15m']  # Columns to plot
marker_list = ['<','v', '>','p']
for ax, df, title, mark in zip(axs, dfs, MPBX_titles, marker_list):
    # Plot each depth column as a separate line
    for col in data_cells:
        sns.lineplot(
            x=pd.to_datetime(df.index), 
            y=df[col],  # Directly reference the column
            linestyle='--', 
            marker = mark,
            label=f'{col}',  # Unique label per line
            ax=ax
        )
    # # Add vertical lines with event annotations
    for ev_date, ev_detail in event_dates.items():
        ax.axvline(x=ev_date, color='blue', linestyle='--', linewidth=0.8)
        ylim = ax.get_ylim()
        ax.text(ev_date, ylim[0], f' {ev_detail}', rotation=90,
                verticalalignment='bottom', fontsize=15, color='black')
    
    ax.set_ylabel('Load Cell Data (T)')
    ax.set_title(title)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.legend()
    plt.setp(ax.get_xticklabels(), rotation=45) 
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('05-20-2025 Load cell for PH_wall_NE.png', dpi=300, bbox_inches='tight')
plt.show()
