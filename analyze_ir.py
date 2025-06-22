import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Ustawienia
input_file = "data/spektrum.csv"
output_folder = "results"
plot_folder = "plots"
os.makedirs(output_folder, exist_ok=True)
os.makedirs(plot_folder, exist_ok=True)

# Wczytaj dane
df = pd.read_csv(input_file, delimiter=',', decimal=',')
df = df.apply(pd.to_numeric, errors='coerce')
wavelengths = df.iloc[:, 0]  # pierwsza kolumna

# Wykres dla każdej próbki
for i in range(1, df.shape[1]):
    sample_name = df.columns[i]
    absorbance = df.iloc[:, i]

    # Detekcja pików
    peaks, _ = find_peaks(absorbance, height=0.1)  # można dopasować threshold

    # Wykres
    plt.figure(figsize=(10, 5))
    plt.plot(wavelengths, absorbance, label=sample_name, color="black")
    plt.plot(wavelengths[peaks], absorbance[peaks], "ro", label="piki")
    plt.xlabel("Liczba falowa [cm⁻¹]")
    plt.ylabel("Absorpcja")
    plt.title(f"Widmo IR - {sample_name}")
    plt.gca().invert_xaxis()
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plot_path = f"{plot_folder}/widmo_{sample_name}.png"
    plt.savefig(plot_path)
    plt.close()

    # Eksport danych
    peak_data = pd.DataFrame({
        "Wavenumber [cm⁻¹]": wavelengths[peaks],
        "Absorbance": absorbance[peaks]
    })
    peak_data.to_csv(f"{output_folder}/piki_{sample_name}.csv", index=False)

print("Analiza zakończona. Wykresy i dane zapisane.")
