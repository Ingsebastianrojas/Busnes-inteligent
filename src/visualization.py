import matplotlib.pyplot as plt

def grafica_facultad(df):
    plt.figure()
    plt.bar(df["facultad"], df["promedio"])
    plt.title("Promedio por Facultad")
    plt.xlabel("Facultad")
    plt.ylabel("Promedio")
    plt.xticks(rotation=45)
    plt.show()

def grafica_riesgo(df):
    plt.figure()
    plt.pie(df["count"], labels=df["riesgo"], autopct="%1.1f%%")
    plt.title("Distribución de Riesgo")
    plt.show()