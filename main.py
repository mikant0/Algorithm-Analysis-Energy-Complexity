import time
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from codecarbon import EmissionsTracker

# --- 1. ALGORİTMALAR (Divide and Conquer) ---
# [Kaynak: Proje Dosyası Sayfa 2 - MergeSort ve QuickSort]

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def quick_sort(arr):
    # Derin özyineleme (recursion) hatasını önlemek için limit artırımı
    sys.setrecursionlimit(20000) 
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)

# --- 2. DENEY MOTORU ---

def run_experiment(algorithm_func, data, algo_name):
    data_copy = data.copy() # Orijinal veri bozulmasın
    
    # Enerji Takipçisi Başlatılıyor (CodeCarbon)
    tracker = EmissionsTracker(project_name=algo_name, measure_power_secs=0.01, save_to_file=False, logging_logger=None)
    tracker.start()
    
    start_time = time.perf_counter()
    
    # Algoritma Çalıştırılıyor
    if algo_name == "QuickSort":
        algorithm_func(data_copy.tolist())
    else:
        algorithm_func(data_copy)
        
    end_time = time.perf_counter()
    emissions = tracker.stop()
    
    # Hesaplamalar:
    # CodeCarbon enerjiyi kWh verir. Biz Joule'e çevireceğiz.
    # 1 kWh = 3,600,000 Joule
    energy_kwh = tracker.final_emissions_data.energy_consumed
    energy_joules = energy_kwh * 3_600_000
    duration = end_time - start_time
    
    return duration, energy_joules

# --- 3. MAİN VE GRAFİK ÇİZİMİ ---

if __name__ == "__main__":
    print("Deney başlatılıyor... Lütfen bekleyiniz (Bu işlem 1-2 dakika sürebilir).")
    
    # Farklı girdi boyutları (Düşük, Orta, Yüksek) [Kaynak: Proje Dosyası Sayfa 1]
    input_sizes = [1000, 5000, 10000, 20000, 50000]
    results = []

    for n in input_sizes:
        print(f"Test ediliyor: Girdi Boyutu {n}...")
        # Rastgele veri üretimi
        data = np.random.randint(0, 100000, n)
        
        # MergeSort Testi
        dur_m, eng_m = run_experiment(merge_sort, data, "MergeSort")
        results.append({"Algoritma": "MergeSort", "Boyut": n, "Süre (sn)": dur_m, "Enerji (Joule)": eng_m})
        
        # QuickSort Testi
        dur_q, eng_q = run_experiment(quick_sort, data, "QuickSort")
        results.append({"Algoritma": "QuickSort", "Boyut": n, "Süre (sn)": dur_q, "Enerji (Joule)": eng_q})

    # Verileri Kaydet
    df = pd.DataFrame(results)
    df.to_csv("Proje_Sonuclari.csv", index=False)
    print("\n--- SONUÇLAR (Excel/CSV olarak kaydedildi) ---")
    print(df)

    # --- GRAFİKLERİN ÇİZİLMESİ ---
    sns.set_theme(style="whitegrid")

    # Grafik 1: Zaman Karmaşıklığı
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="Boyut", y="Süre (sn)", hue="Algoritma", marker="o", linewidth=2.5)
    plt.title("Zaman Karmaşıklığı Analizi (Time Complexity)", fontsize=14)
    plt.xlabel("Girdi Boyutu (n)", fontsize=12)
    plt.ylabel("Süre (Saniye)", fontsize=12)
    plt.grid(True)
    plt.savefig("Grafik_Zaman.png", dpi=300)
    print("\nGrafik_Zaman.png oluşturuldu.")

    # Grafik 2: Enerji Karmaşıklığı
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="Boyut", y="Enerji (Joule)", hue="Algoritma", marker="s", linewidth=2.5)
    plt.title("Enerji Karmaşıklığı Analizi (Energy Complexity)", fontsize=14)
    plt.xlabel("Girdi Boyutu (n)", fontsize=12)
    plt.ylabel("Enerji Tüketimi (Joule)", fontsize=12)
    plt.grid(True)
    plt.savefig("Grafik_Enerji.png", dpi=300)
    print("Grafik_Enerji.png oluşturuldu.")
    
    print("\nİŞLEM TAMAMLANDI! Klasörünüzü kontrol edin.")