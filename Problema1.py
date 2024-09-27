import math

def maximo_de_reliquias(M):
    R = len(M)
    C = len(M[0])

    # Inicializar las tablas DP con -inf usando listas
    dp_indiana = [[-math.inf for _ in range(C)] for _ in range(R)]
    dp_marion = [[-math.inf for _ in range(C)] for _ in range(R)]
    dp_sallah = [[-math.inf for _ in range(C)] for _ in range(R)]

    # Inicializar las posiciones iniciales
    dp_indiana[0][0] = M[0][0]  # Indiana empieza en (0,0)
    dp_marion[0][C-1] = M[0][C-1]  # Marion empieza en (0,C-1)
    dp_sallah[R-1][C//2] = M[R-1][C//2]  # Sallah empieza en (R-1,C//2)

    # DP para Indiana y Marion: se mueven hacia abajo
    for i in range(1, R//2 + 1):
        for j in range(C):
            if M[i][j] != -1:  # Solo continuar si la celda no está maldita
                # Indiana
                if j > 0 and dp_indiana[i-1][j-1] != -math.inf:
                    dp_indiana[i][j] = max(dp_indiana[i][j], dp_indiana[i-1][j-1] + M[i][j])
                if dp_indiana[i-1][j] != -math.inf:
                    dp_indiana[i][j] = max(dp_indiana[i][j], dp_indiana[i-1][j] + M[i][j])
                if j < C-1 and dp_indiana[i-1][j+1] != -math.inf:
                    dp_indiana[i][j] = max(dp_indiana[i][j], dp_indiana[i-1][j+1] + M[i][j])

                # Marion
                if j > 0 and dp_marion[i-1][j-1] != -math.inf:
                    dp_marion[i][j] = max(dp_marion[i][j], dp_marion[i-1][j-1] + M[i][j])
                if dp_marion[i-1][j] != -math.inf:
                    dp_marion[i][j] = max(dp_marion[i][j], dp_marion[i-1][j] + M[i][j])
                if j < C-1 and dp_marion[i-1][j+1] != -math.inf:
                    dp_marion[i][j] = max(dp_marion[i][j], dp_marion[i-1][j+1] + M[i][j])
            else: 
                dp_indiana[i][j] = -math.inf
                dp_marion[i][j] = -math.inf
    # DP para Sallah: se mueve hacia arriba
    for i in range(R-2, R//2 - 1, -1):
        for j in range(C):
            if M[i][j] != -1:  # Solo continuar si la celda no está maldita
                if j > 0 and dp_sallah[i+1][j-1] != -math.inf:
                    dp_sallah[i][j] = max(dp_sallah[i][j], dp_sallah[i+1][j-1] + M[i][j])
                if dp_sallah[i+1][j] != -math.inf:
                    dp_sallah[i][j] = max(dp_sallah[i][j], dp_sallah[i+1][j] + M[i][j])
                if j < C-1 and dp_sallah[i+1][j+1] != -math.inf:
                    dp_sallah[i][j] = max(dp_sallah[i][j], dp_sallah[i+1][j+1] + M[i][j])
            else:
                dp_sallah[i][j] = -math.inf
    #Traer el maximo de reliquieas que todos tienen hasta la fila de la mitad
    max_relics_indiana = [-math.inf] * C
    max_relics_marion = [-math.inf] * C
    max_relics_sallah = [-math.inf] * C

    for j in range(C):
        max_relics_indiana[j] = dp_indiana[R//2][j] if dp_indiana[R//2][j] != -math.inf else 0
        max_relics_marion[j] = dp_marion[R//2][j] if dp_marion[R//2][j] != -math.inf else 0
        max_relics_sallah[j] = dp_sallah[R//2][j] if dp_sallah[R//2][j] != -math.inf else 0

    
    #Calcular la mejor combinación en la misma fila de medio cuando halla maldiciones
    max_reliquias = -math.inf

    #iterar sobre las columnas y escoger la mejor combinación considerando que alguien muere
    for j in range(C):
        for k in range(C):
            for l in range(C):
                if M[i][j] == -1 or M[i][k] == -1 or M[i][l] == -1:
                    continue
                # Verificar si los tres caen en la misma celda
                if j == k == l:
                    # Si todos caen en la misma celda
                    max_reliquias = max(
                        max_reliquias, 
                        max_relics_indiana[j] + max_relics_marion[k] + max_relics_sallah[l] - M[R//2][j]
                    )
                else:
                    # Para el caso general donde no se encuentran todos en la misma celda
                    if j != k and k != l and j != l:  # Indiana, Marion y Sallah en diferentes celdas
                        max_reliquias = max(
                            max_reliquias, 
                            max_relics_indiana[j] + max_relics_marion[k] + max_relics_sallah[l]
                        )

    return max_reliquias

def leer_casos_desde_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        num_casos = int(archivo.readline().strip())
        casos = []
        
        for _ in range(num_casos):
            R, C = map(int, archivo.readline().strip().split())
            matriz = [list(map(int, archivo.readline().strip().split())) for _ in range(R)]
            casos.append({'R': R, 'C': C, 'matriz': matriz})
        
        return casos

# Función para procesar cada caso
def procesar_caso(caso):
    R, C, matriz = caso['R'], caso['C'], caso['matriz']
    return maximo_de_reliquias(matriz)

def main(): 
    opcion = int(input("Ingrese 1 para leer archivo o 2 para escribirlo en consola o 3 para la matriz por defecto: "))
    if opcion == 1:
        nombre_archivo_entrada = input("Ingrese el nombre del archivo de entrada: ")
        casos = leer_casos_desde_archivo(nombre_archivo_entrada)
        
        # Procesar cada caso
        resultados = [procesar_caso(caso) for caso in casos]
        contador = 1
        for resultado in resultados:
            print(f"Máximo de recursive_board_game: {resultado} , caso {contador}")
            contador += 1
        
    elif opcion == 2:
        R, C = map(int, input().strip().split())
        matriz = [list(map(int, input().strip().split())) for _ in range(R)]
        print(f"Procesando caso con matriz de tamaño {R}x{C}:")
        resultado = maximo_de_reliquias(matriz)
        print(f"Máximo de recursive_board_game: {resultado}")
        
    elif opcion == 3:
        print(maximo_de_reliquias(matriz))
    
if __name__ == "__main__":
    main()
    

