import math
from scipy.stats import norm
import streamlit as st

# Full-screen layout
st.set_page_config(page_title="Hipotez Testi ve Güven Aralığı Hesaplama", layout="wide")

# Başlık
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Hipotez Testi ve Güven Aralığı Hesaplama</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Bu uygulama, birden fazla grup için hipotez testi yapmanızı ve güven aralığı hesaplamanızı sağlar.</p>", unsafe_allow_html=True)

# Grup sayısını seç
st.write("### Grup Sayısı")
num_samples = st.number_input("Grup Sayısı (N)", min_value=2, value=2)

# Dinamik girişler
st.write("### Grup Verileri")
sample_sizes = []
means = []
variances = []

# Display groups in rows of 3
for row_start in range(0, num_samples, 2):
    cols = st.columns(2)  # Create 3 columns per row
    for i, col in enumerate(cols):
        group_index = row_start + i + 1
        if group_index > num_samples:
            break
        with col:
            with st.expander(f"Grup {group_index} Verileri", expanded=True):
                sample_sizes.append(st.number_input(f"Örneklem Sayısı (n{group_index})", min_value=1, value=5, key=f"n{group_index}"))
                means.append(st.number_input(f"Ortalama (Grup {group_index})", value=50.0, key=f"mean{group_index}"))
                variances.append(st.number_input(f"Varyans (Grup {group_index})", min_value=0.0, value=30.0, key=f"var{group_index}"))

# Alfa değeri
st.write("### Test Parametreleri")
alfa = st.number_input("Anlamlılık Düzeyi (α)", min_value=0.0, max_value=1.0, value=0.05)

# Hesapla butonu
if st.button("Hesapla"):
    # Hesaplamalar
    mean_diff = means[0] - sum(means[1:])
    total_variance = variances[0] / sample_sizes[0]
    for i in range(1, num_samples):
        total_variance += variances[i] / sample_sizes[i]

    z_payda = math.sqrt(total_variance)
    z_skoru = mean_diff / z_payda
    z_kritik = norm.ppf(1 - alfa)

    # Hipotez testi sonucu
    if z_skoru > z_kritik:
        test_sonucu = "H0 reddedildi. İlk grubun ortalaması diğerlerinden büyüktür."
    else:
        test_sonucu = "H0 reddedilemedi. İlk grubun ortalaması diğerlerinden büyük olduğu söylenemez."

    # Güven aralığı
    z_kritik_2 = norm.ppf(1 - alfa / 2)
    hata_payi = z_kritik_2 * z_payda
    guven_araligi = (mean_diff - hata_payi, mean_diff + hata_payi)

    # Sonuçları göster
    st.write("### Sonuçlar")
    col1, col2, col3 = st.columns([1, 1, 2])  # Adjusted column widths

    with col1:
        st.metric("Z Skoru", f"{z_skoru:.3f}")
    with col2:
        st.metric("Kritik Z Değeri", f"{z_kritik:.3f}")
    with col3:
        st.write("### Güven Aralığı")
        st.metric("95% Güven Aralığı", f"[{guven_araligi[0]:.2f}, {guven_araligi[1]:.2f}]")

    st.metric("Hipotez Testi Sonucu", test_sonucu)

