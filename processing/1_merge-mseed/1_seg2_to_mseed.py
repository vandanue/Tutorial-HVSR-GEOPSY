from obspy.core import read, Stream
import os
import glob

folder_path = r'D:\Kulon Progo 2025\Seismik Pasif\data\Kulon Progo\Kelompok 1_Day4\D1'
files = glob.glob(os.path.join(folder_path, '*.seg2'))

print(files)

del files[0]
del files[-1]
data=[None]*len(files)

for i in range(len(files)):
    data[i]=read(files[i])

x_comp=data[0].traces[0]
y_comp=data[0].traces[1]
z_comp=data[0].traces[2]

for j in range(1,len(files)):
    x_comp+=data[j].traces[0]
    y_comp+=data[j].traces[1]
    z_comp+=data[j].traces[2]
    

x_comp.stats.channel = "EHE"  # Komponen timur-barat
y_comp.stats.channel = "EHN"  # Komponen utara-selatan
z_comp.stats.channel = "EHZ"  # Komponen vertikal

# Gabungkan ketiga komponen menjadi satu Stream
combined_stream = Stream(traces=[x_comp, y_comp, z_comp])

# Ambil nama folder terakhir dari path sebagai nama file
folder_name = os.path.basename(folder_path)

output_filename = f"{folder_name}_merge3comps.mseed"
output_path = os.path.join(folder_path, output_filename)

# Simpan stream gabungan dalam format MiniSEED
combined_stream.write(output_path, format='MSEED')
print(f"\n\n----------------------------------------------------------\n File MSEED gabungan telah disimpan di: {output_path}")