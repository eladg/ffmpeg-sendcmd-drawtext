"""
This script processes a CSV file containing object detection data and generates an FFmpeg `sendcmd` script. 

The CSV file should have the following structure:
    Timestamp,Label,Width,Height,Left,Top
    0,Person,0.673,0.860,0.165,0.139
    500,Person,0.673,0.861,0.165,0.138
    ...
    
The generated `sendcmd` script is used for adding annotations such as text labels and bounding boxes on video frames.
Example usage with FFmpeg:
    ffmpeg -y -i input.mp4 -vf 'sendcmd=f=sendcmd.txt,drawbox,drawtext' output.mp4
"""

import csv
import sys

# File paths
CSV_FILEPATH = "./input.csv"
SENDCMD_OUTPUT = "./sendcmd.txt"

# Time scale to convert milliseconds to seconds (used by FFmpeg)
TIMESCALE = 1000

def read_csv(file_path):
    """
    Reads a CSV file and returns the data as a list of dictionaries.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        list[dict]: List of rows, where each row is represented as a dictionary.
    """
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def generate_sendcmd(data):
    """
    Generates the FFmpeg `sendcmd` script from the input data.
    
    Args:
        data (list[dict]): List of dictionaries with annotation data.
        
    Returns:
        str: FFmpeg `sendcmd` script as a string.
    """
    cmd_text = ""

    for row in data:
        # Extract and format values from the CSV row
        start_time = float(row["Timestamp"]) / TIMESCALE
        b_width = f'{row["Width"]}*in_w'
        b_height = f'{row["Height"]}*in_h'
        label = row["Label"]
        p_left = f'{row["Left"]}*in_w'
        p_top = f'{row["Top"]}*in_h'
        t_left = f'{row["Left"]}*W'
        t_top = f'{row["Top"]}*H-30'
        box_color = 'green'

        # Construct the FFmpeg draw commands
        cmd_text += f'{start_time} [enter] '
        cmd_text += (
            f'drawtext reinit \'fontsize=30:fontcolor={box_color}:text={label}:'
            f'x={t_left}:y={t_top}\', '
            f'drawbox x \'{p_left}\', drawbox y \'{p_top}\', '
            f'drawbox w \'{b_width}\', drawbox h \'{b_height}\', '
            f'drawbox color \'{box_color}\''
        )
        cmd_text += ';\n'

    return cmd_text

def write_to_file(content, file_path):
    """
    Writes the content to a specified file.
    
    Args:
        content (str): Content to be written.
        file_path (str): Path to the output file.
    """
    with open(file_path, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    # Ensure the script is executed with a file argument
    if len(sys.argv) < 2:
        print("Usage: python generate_csv.py <CSV_FILEPATH>")
        sys.exit(1)
    
    # Get the CSV file path from command-line arguments
    CSV_FILEPATH = sys.argv[1]

    # Read the CSV file
    csv_data = read_csv(CSV_FILEPATH)
    
    # Generate the FFmpeg sendcmd script
    sendcmd_script = generate_sendcmd(csv_data)
    
    # Write the script to the output file
    write_to_file(sendcmd_script, SENDCMD_OUTPUT)
    
    print(f"Sendcmd script written to {SENDCMD_OUTPUT}")