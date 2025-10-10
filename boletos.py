def menu():
    funciones = []
    ventas = []

    print("🔐 Iniciar sesión")
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    if contraseña != "1234":
        print("❌ Contraseña incorrecta. Acceso denegado.")
        return

    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Registrar función nueva")
        print("2. Listar funciones disponibles")
        print("3. Vender boletos")
        print("4. Ver resumen de ventas del día")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            codigo = input("Código de la función: ")
            pelicula = input("Nombre de la película: ")
            hora = input("Hora de la función: ")
            precio = 10000  # Precio fijo del boleto
            funciones.append({"codigo": codigo, "pelicula": pelicula, "hora": hora, "precio": precio, "disponibles": 200})
            print("✅ Función registrada con éxito (200 boletos disponibles, precio $10.000).")

        elif opcion == "2":
            print("\n--- Funciones disponibles ---")
            if not funciones:
                print("No hay funciones registradas.")
            else:
                for f in funciones:
                    print(f"Código: {f['codigo']} | Película: {f['pelicula']} | Hora: {f['hora']} | Precio: ${f['precio']} | Boletos disponibles: {f['disponibles']}")

        elif opcion == "3":
            if not funciones:
                print("No hay funciones registradas.")
                continue
            codigo = input("Ingrese el código de la función: ")
            funcion = next((f for f in funciones if f["codigo"] == codigo), None)
            if not funcion:
                print("❌ Error: la función no existe.")
                continue
            try:
                cantidad = int(input("Cantidad de boletos: "))
                if cantidad <= 0:
                    print("❌ Error: cantidad inválida.")
                    continue
                if cantidad > funcion["disponibles"]:
                    print(f"❌ Solo hay {funcion['disponibles']} boletos disponibles.")
                    continue
            except ValueError:
                print("❌ Error: debe ingresar un número válido.")
                continue

            total = funcion["precio"] * cantidad
            funcion["disponibles"] -= cantidad

            print(f"\nPelícula: {funcion['pelicula']}")
            print(f"Hora: {funcion['hora']}")
            print(f"Total a pagar: ${total}")
            ventas.append({"codigo": codigo, "cantidad": cantidad, "total": total})
            print("✅ Venta registrada (solo muestra en pantalla, no imprime recibo).\n")

        elif opcion == "4":
            if not ventas:
                print("No hay ventas registradas.")
                continue
            total_boletos = sum(v["cantidad"] for v in ventas)
            total_dinero = sum(v["total"] for v in ventas)
            print(f"\nBoletos vendidos: {total_boletos}")
            print(f"Dinero recaudado: ${total_dinero}")

        elif opcion == "5":
            print("👋 Saliendo del sistema...")
            break

        else:
            print("❌ Opción no válida, intente de nuevo.")

menu()