import sys
sys.path.append(r"D:\Setelah Kuliah\Lamaran Pekerjaan\Kecilin\git\peopleCounterAbel")

from Counter import peopleCounter


# =============================================================================
# A. PILIH SALAH SATU POV KAMERA YANG DIINGINKAN:
#   
#   1. CLOSE
#   2. MEDIUM
#   3. FAR
#
# B. Pilih file yang ingin dimasukan (Opsional)
# C. Tentukan N Warning (Banyak orang sebagai warning)
# =============================================================================

file="input/Far.mp4"
penghitung=peopleCounter("Far",file,10)
penghitung.chooseModel()
penghitung.counting()