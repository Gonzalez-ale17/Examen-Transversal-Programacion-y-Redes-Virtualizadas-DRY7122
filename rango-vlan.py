try:
    vlan = int(input("Numero de VLAN: "))

    if 1 <= vlan <= 1005:
        print(f"VLAN {vlan} pertenece al rango normal (1-1005).")
    elif 1006 <= vlan <= 4094:
        print(f"VLAN {vlan} pertenece al rango extendido (1006-4094).")
    else:
        print("Numero de VLAN invalido. Debe estar entre 1 y 4094.")
except ValueError:
    print("Entrada invalida, ingrese un número entero.")
