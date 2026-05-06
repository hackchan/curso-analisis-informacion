import pandas as pd
import numpy as np
import os

data_csv_simple = {
    'Nombre': ['Alice', 'Bob', 'Charlie'],
    'Edad': [24, 27, 22],
    'Ciudad': ['Nueva York', 'Londres', 'París']
}
df_simple = pd.DataFrame(data_csv_simple)
df_simple.to_csv('datos_simples.csv', index=False)

print('Archivo "datos_simples.csv" creado.')

df_leido_csv = pd.read_csv('datos_simples.csv')
print("Contenido del archivo CSV simple:")
print(df_leido_csv)

data_excel_simple = {
    'Producto': ['Laptop', 'Mouse', 'Teclado'],
    'Precio': [1200, 25, 75],
    'Cantidad': [10, 50, 30]
}
df_excel_simple = pd.DataFrame(data_excel_simple)
df_excel_simple.to_excel('productos_simples.xlsx', index=False)

print('Archivo "productos_simples.xlsx" creado.')

df_leido_excel = pd.read_excel('productos_simples.xlsx')
print("Contenido del archivo Excel simple:")
print(df_leido_excel)

contenido_csv_complejo = (
    "# Esto es un comentario\n"
    "Fecha;Ventas;Region\n"
    "2023-01-01;123,45;Norte\n"
    "2023-01-02;67,89;Sur\n"
    "2023-01-03;90,12;Este\n"
    "Final del reporte"
)
with open('ventas_complejas.csv', 'w', encoding='utf-8') as f:
    f.write(contenido_csv_complejo)

print('Archivo "ventas_complejas.csv" creado con estructura compleja.')

df_leido_complejo_csv = pd.read_csv(
    'ventas_complejas.csv',
    sep=';',
    skiprows=[0, 5],
    decimal=','
)
print("Contenido del archivo CSV complejo:")
print(df_leido_complejo_csv)
print("Tipos de datos después de la lectura:")
print(df_leido_complejo_csv.dtypes)

with pd.ExcelWriter('reporte_multih.xlsx') as writer:
    df_resumen = pd.DataFrame({
        'Mes': ['Enero', 'Febrero', 'Marzo'],
        'Ingresos': [10000, 12000, 11500]
    })
    df_resumen.to_excel(writer, sheet_name='Resumen Mensual', index=False)

    df_detalle = pd.DataFrame({
        'ID Transacción': [1, 2, 3],
        'Producto': ['A', 'B', 'C'],
        'Cantidad': [5, 2, 8]
    })
    metadata_rows = pd.DataFrame([['Reporte de Ventas', np.nan, np.nan], ['Generado el:', '2023-01-01', np.nan], [np.nan, np.nan, np.nan]])
    df_final_detalle = pd.concat([metadata_rows, df_detalle], ignore_index=True)
    df_final_detalle.to_excel(writer, sheet_name='Detalle Ventas', index=False, header=False)

print('Archivo "reporte_multih.xlsx" creado.')

df_resumen_mensual = pd.read_excel('reporte_multih.xlsx', sheet_name='Resumen Mensual')
print("Datos de la hoja 'Resumen Mensual':")
print(df_resumen_mensual)

df_detalle_ventas = pd.read_excel(
    'reporte_multih.xlsx',
    sheet_name='Detalle Ventas',
    skiprows=3,
    header=None,
    names=['ID Transacción', 'Producto', 'Cantidad']
)
print("Datos de la hoja 'Detalle Ventas' (con skiprows y nombres de columna):")
print(df_detalle_ventas)

contenido_latin1 = (
    "ID;Descripción;Valor\n"
    "1;Pequeño negocio;100\n"
    "2;Grandes áreas;250\n"
    "3;Fenómenos atmosféricos;50\n"
)
with open('datos_latin1.csv', 'w', encoding='latin1') as f:
    f.write(contenido_latin1)

print('Archivo "datos_latin1.csv" creado con codificación latin1.')

print("Intento de lectura sin encoding (esperando error o caracteres incorrectos):")
try:
    df_error_encoding = pd.read_csv('datos_latin1.csv', sep=';')
    print(df_error_encoding)
except UnicodeDecodeError as e:
    print(f"¡Error de decodificación esperado! {e}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")

df_latin1_correcto = pd.read_csv('datos_latin1.csv', sep=';', encoding='latin1')
print("Lectura correcta con encoding='latin1':")
print(df_latin1_correcto)

"""
for f in ['datos_simples.csv', 'productos_simples.xlsx', 'ventas_complejas.csv', 'reporte_multih.xlsx', 'datos_latin1.csv']:
    if os.path.exists(f):
        os.remove(f)
        print(f'Archivo {f} eliminado.')
"""