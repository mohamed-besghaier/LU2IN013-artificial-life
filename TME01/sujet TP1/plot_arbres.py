import csv
import matplotlib.pyplot as plt

iterations = []
fractions = []

# Read CSV
with open("arbres.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)  # skip header
    for row in reader:
        iterations.append(int(row[0]))
        fractions.append(float(row[1]))

# Plot
plt.plot(iterations, fractions, color='green')
plt.xlabel("Itérations")
plt.ylabel("Fraction d'arbres sains")
plt.title("Évolution du nombre d'arbres sains")
plt.grid(True)
plt.show()
