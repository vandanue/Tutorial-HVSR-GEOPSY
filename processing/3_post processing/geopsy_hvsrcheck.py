# File name     : geopsy_hvsrcheck.py
# Info          : Program to check reliable and clear peak of H/V curve from Geopsy file (.hv)
# Update        : 26th March 2020
# Written by    : Aulia Khalqillah,S.Si.,M.Si
# Email         : auliakhalqillah.mail@gmail.com
# Source        : GUIDELINES FOR THE IMPLEMENTATION OF THE H/V SPECTRAL RATIO TECHNIQUE ON AMBIENT VIBRATIONS
#                 MEASUREMENTS, PROCESSING AND INTERPRETATION, SESAME European research project
#                 WP12 – Deliverable D23.12 [ftp://ftp.geo.uib.no/pub/seismo/SOFTWARE/SESAME/USER-GUIDELINES/SESAME-HV-User-Guidelines.pdf]
#
# USAGE         : Using hvsrcheck.py as modules file
#                 example: hvsrcheck(input)
#                 input is dictionary type.
#                 "You just need to add the .hv and .log files in filename and logname variable that you have"
# TESTED        : Python >= 3.7
# ------------------------------------------------------------------------------------------------------------------------------------------
# EDITED        : - 24 Nov 2024, Michael Partogi. Solving hvcheck module for returning clear peak criteria
#                 - 12 Jan 2025, Annora Vandanu Erlangga. Add script to read .log dan .hv files in batch processing for SESAME criteria
# ------------------------------------------------------------------------------------------------------------------------------------------

import os
import numpy as np
import pandas as pd
import re
from hvcheck import hvsrcheck

def main():
    # Pindah ke folder yang ada file-nya
    os.chdir(r"D:\Kulon Progo 2025\Seismik Pasif\processing\2_HVSR\HV")

    files = [f for f in os.listdir() if f.endswith('.hv')]
    print("Files ditemukan:", files)
    prefixes = {f[:-3] for f in files}
    
    for prefix in prefixes:
        process_hvsr(prefix)

def find_window_info(logfile_path):
    """Mencari number of window dan window length dari file .log"""
    with open(logfile_path, 'r') as logfile:
        lines = logfile.readlines()
        
        window_number, window_length = None, None
        window_line_index = None
        
        for i, line in enumerate(lines):
            if "Number=" in line:
                window_number = int(line.split('=')[-1].strip())  # Ambil angka setelah "="
                window_line_index = i  # Simpan indeks baris ini untuk referensi
                
            elif window_line_index is not None and i == window_line_index + 2:
                # Cari angka terakhir di baris setelah "Start time End Time Window length"
                values = line.strip().split()
                if values:
                    try:
                        window_length = float(values[-1])  # Ambil angka terakhir
                    except ValueError:
                        pass
                break  # Sudah dapat window_length, keluar dari loop
        
    return window_number, window_length

def process_hvsr(file_prefix):
    """Memproses file HVSR berdasarkan prefix nama file (uT1, uT2, dst)."""
    filename = f"{file_prefix}.hv"
    logname = f"{file_prefix}.log"
    
    if not os.path.exists(filename) or not os.path.exists(logname):
        print(f"File {filename} atau {logname} tidak ditemukan.")
        return
    
    with open(filename, "r") as data:
        frequency, amplification, minamplification, maxamplification = [], [], [], []
        
        for index, line in enumerate(data):
            if index == 4:
                fr0 = line.strip().split("\t")
                domfreq = float(fr0[1])
                mindomfreq = float(fr0[2])
                maxdomfreq = float(fr0[3])
            elif index == 5:
                hv = float(line.strip().split("\t")[1])
            elif index >= 9:
                field = line.strip().split("\t")
                frequency.append(float(field[0]))
                amplification.append(float(field[1]))
                minamplification.append(float(field[2]))
                maxamplification.append(float(field[3]))
    
    frequency = np.array(frequency)
    amplification = np.array(amplification)
    minamplification = np.array(minamplification)
    maxamplification = np.array(maxamplification)
    KG = ((hv**2) / domfreq)
    idmaxamp = np.argmax(amplification)
    stdA = maxamplification[idmaxamp] / amplification[idmaxamp]
    stdf0 = domfreq - mindomfreq
    stdhv = amplification - minamplification
    minstdA0 = minamplification[np.argmax(minamplification)]
    maxstdA0 = maxamplification[np.argmax(maxamplification)]

    collect = [frequency,amplification,minamplification,maxamplification]
    store_data = pd.DataFrame(collect,index=['Frequency','Average','Min','Max']).T
    print("-----------------------------------------------------------------------")
    print("OUTPUT INFORMATION OF H/V")
    print("-----------------------------------------------------------------------")
    # print(store_data)
    print("A0\t\t\t\t\t:",hv)
    print("F0\t\t\t\t\t:",domfreq,"Hz")
    print("KG\t\t\t\t\t:",KG)
    print("MIN F0\t\t\t\t:",mindomfreq,"Hz")
    print("MAXF0\t\t\t\t:",maxdomfreq,"Hz")
    data.close()    
    
    window, winlength = find_window_info(logname)
    
    print(f"Processing {filename} and {logname}")
    print("WINDOW NUMBER\t\t:", window)
    print("WINDOW LENGTH\t\t:", winlength, "seconds")
    
    input_data = {
        'filename': filename,
        'maxfreq': max(frequency),
        'winlength': winlength,
        'window': window,
        'frhv': frequency,
        'hvsr': amplification,
        'A0': hv,
        'F0': domfreq,
        'KG': KG,
        'stdA': stdA,
        'stdf0': stdf0,
        'stdhv': stdhv,
        'f0min': mindomfreq,
        'f0max': maxdomfreq,
        'minstdhv': minamplification,
        'maxstdhv': maxamplification,
        'minstdA0': minstdA0,
        'maxstdA0': maxstdA0,
        'lengthhv': len(amplification),
    }
    
    hvsrcheck(input_data)
    print("\n\n\n")

# def main():
#     """Menjalankan pemrosesan untuk semua file .hv dan .log dalam direktori."""
#     files = [f for f in os.listdir() if f.endswith('.hv')]
#     prefixes = {f[:-3] for f in files}  # Mengambil prefix dari file (misal uT1, uT2)
    
#     for prefix in prefixes:
#         process_hvsr(prefix)

# def main():
#     """Menjalankan pemrosesan untuk semua file .hv dan .log dalam direktori dan menyimpan hasil ke CSV."""
#     files = [f for f in os.listdir() if f.endswith('.hv')]
#     prefixes = {f[:-3] for f in files}  # Mengambil prefix dari file (misal uT1, uT2)
    
#     results_list = []  # List untuk menyimpan hasil
    
#     for prefix in prefixes:
#         process_hvsr(prefix, results_list)
    
#     # Simpan hasil ke CSV
#     results_df = pd.DataFrame(results_list)
#     results_df.to_csv("HVSR_Results.csv", index=False)
    
#     print("\n Hasil telah disimpan dalam 'HVSR_Results.csv'")

if __name__ == "__main__":
    main()
