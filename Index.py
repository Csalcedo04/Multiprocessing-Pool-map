import time
import re
import os
import multiprocessing as mp
import filecmp




class Route:
    def __init__(self, ruta) -> None:
        self.ruta = ruta
        pass


class Serial(Route):
    def __init__(self,ruta) -> None:
        super().__init__(ruta)
        pass

    def shoelace_formula(self, coordinates: list)->str:
        n:int = len(coordinates)
        if n < 3:
            return 0

        # Initialize variables for the calculations
        area:float = 0.0
        j:int = n - 1

        # Apply the Shoelace formula
        for i in range(n):
            xi, yi = coordinates[i]
            xj, yj = coordinates[j]
            area += (xi + xj) * (yj - yi)
            j = i

        return str(abs(area) / 2)

    def run(self)->float:
        t1:float = time.perf_counter()
        pattern = r"\((\d+),(\d+)\)"
        with open(self.ruta, "r") as f, open('Carlos_serial_output.txt', 'w') as outfile:
            lines:list[str] = [line for line in f]
            for line in lines:
                points:list[str] = re.findall(pattern, line)
                float_points: list[tuple[float, float]] = [(float(x), float(y)) for x, y in points]
                outfile.write(f'{self.shoelace_formula(float_points)}\n')

            t2:float = time.perf_counter()
            print(f"Time taken, serial method: \t{t2 - t1}")
        return t2 - t1


class Parallel(Route):
    def __init__(self, ruta) -> None:
        super().__init__(ruta)
        pass

    def shoelace_formula(self, coordinates:list)->float:
        n:int = len(coordinates)
        if n < 3:
            return 0
        area:float = 0.0
        j:float = n - 1
        for i in range(n):
            xi, yi = coordinates[i]
            xj, yj = coordinates[j]
            area += (xi + xj) * (yj - yi)
            j = i
        return abs(area) / 2

    def process_line(self, line)-> list[tuple[float, float]]:
        pattern = re.compile(r"\((\d+),(\d+)\)")
        points:list[str] = pattern.findall(line)
        float_points:list[tuple[float, float]] = [(float(x), float(y)) for x, y in points]
        return float_points



    def wrapper(self, args:list)-> list[list[tuple[float, float]]]:
        return [self.shoelace_formula(self.process_line(line)) for line in args]

    def run(self)->float:
        cpu:int = os.cpu_count()
        t1:float = time.perf_counter()
        with open(self.ruta, "r") as f:
            lines:list[str] = [line for line in f]
        list_points:list = list(chunks(lines, len(lines) // cpu))
        try:
            res = list_points.pop()
            list_points[-1].extend(res)

            with mp.Pool(processes=cpu) as pool:
                results = pool.map(self.wrapper, list_points)

            with open("Carlos_parallelized_output.txt", "w") as f:
                for result in results:
                    for area in result:
                        f.write(f'{area}\n')
            t2:float = time.perf_counter()
            print(f"Time taken, parallel method: \t{t2-t1}")
            return t2-t1
        except IndexError:
            pass

def chunks(lst:list, n:int):
    try:
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    except ValueError:
        print("El archivo digitado no posee la estructura requerida para el programa")


def has_txt_extension(file_path:str)->bool:
    _ , extension = os.path.splitext(file_path)
    return extension.lower() == ".txt"


if __name__ =="__main__":

    folder_path = input("Digite la ruta con el archivo de poligonos.txt: ")
    while True:
        try:
            if has_txt_extension(folder_path):
                s = Serial(folder_path).run()
                p = Parallel(folder_path).run()
                if s is False or p is False:
                    print("El archivo ingresado no corresponde a una serie de listas con los puntos de varios poligonos, Por favor digite un archivo valido. ")
                else:
                    try:
                        print(f"relacion {s/p}")
                    except TypeError:
                        pass
                    result = filecmp.cmp('Carlos_serial_output.txt', 'Carlos_parallelized_output.txt', shallow=False)
                    if result:
                        print("Las respuestas en los archivos Carlos_parallelized_output.txt y Carlos_serial_output.txt son iguales.")
                    else:
                        print("Las respuestas en los archivos Carlos_parallelized.txt y Carlos_serial_output.txt son differentes.")
                break
            else:
                print("\nPor favor digite correctamente la ruta del rachivo\n")
                folder_path = input("Digite la ruta con el archivo de poligonos.txt: ")
                pass
            break
        except FileNotFoundError:
            print("El archivo digitado no existe")
            break