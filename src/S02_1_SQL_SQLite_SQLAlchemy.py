import sqlite3
import pandas as pd

conn = sqlite3.connect(':memory:')
c = conn.cursor()

print("Base de datos SQLite en memoria creada exitosamente.")

c.execute('''
    CREATE TABLE auditorias (
        id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_auditoria TEXT NOT NULL,
        fecha_inicio DATE NOT NULL,
        fecha_fin DATE,
        estado TEXT NOT NULL
    );
''')

c.execute('''
    CREATE TABLE funcionarios (
        id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cargo TEXT NOT NULL,
        departamento TEXT NOT NULL
    );
''')

c.execute('''
    CREATE TABLE hallazgos (
        id_hallazgo INTEGER PRIMARY KEY AUTOINCREMENT,
        id_auditoria INTEGER NOT NULL,
        descripcion TEXT NOT NULL,
        severidad TEXT NOT NULL,
        monto_afectado REAL,
        fecha_identificacion DATE NOT NULL,
        FOREIGN KEY (id_auditoria) REFERENCES auditorias(id_auditoria)
    );
''')

print("Tablas 'auditorias', 'funcionarios' y 'hallazgos' creadas exitosamente.")

c.execute("ALTER TABLE funcionarios ADD COLUMN email TEXT;")
print("Columna 'email' añadida a la tabla 'funcionarios'.")

result = c.execute("PRAGMA table_info(funcionarios);").fetchall()
print("\nNueva estructura de la tabla 'funcionarios':")
for row in result:
    print(row)

c.execute('''
    CREATE TABLE tabla_temporal (
        id INTEGER PRIMARY KEY,
        dato TEXT
    );
''')
print("Tabla 'tabla_temporal' creada.")

c.execute("DROP TABLE tabla_temporal;")
print("Tabla 'tabla_temporal' eliminada.")

c.execute("""
    INSERT INTO auditorias (nombre_auditoria, fecha_inicio, fecha_fin, estado)
    VALUES
        ('Auditoría Financiera 2023 MinHacienda', '2023-01-15', '2023-06-30', 'Finalizada'),
        ('Auditoría de Cumplimiento Contratación Pública IDU', '2023-03-01', '2023-09-15', 'En Proceso'),
        ('Auditoría de Desempeño Gestión Ambiental CAR', '2023-05-10', NULL, 'Planeada'),
        ('Auditoría al Programa de Alimentación Escolar (PAE)', '2022-11-01', '2023-04-30', 'Finalizada');
""")
conn.commit()
print("Datos insertados en la tabla 'auditorias' exitosamente.")

c.execute("""
    INSERT INTO funcionarios (nombre, cargo, departamento, email)
    VALUES
        ('Ana María Gómez', 'Auditor Senior', 'Financiero', 'ana.gomez@contraloria.gov.co'),
        ('Carlos Pérez Rojas', 'Jefe de Equipo de Auditoría', 'Contratación', 'carlos.perez@contraloria.gov.co'),
        ('Laura Botero Vélez', 'Auditor Junior', 'Desempeño', 'laura.botero@contraloria.gov.co'),
        ('Miguel Ángel López', 'Coordinador de Proyectos', 'Financiero', 'miguel.lopez@contraloria.gov.co');
""")
conn.commit()
print("Datos insertados en la tabla 'funcionarios' exitosamente.")

c.execute("""
    INSERT INTO hallazgos (id_auditoria, descripcion, severidad, monto_afectado, fecha_identificacion)
    VALUES
        (1, 'Deficiencias en la conciliación de cuentas bancarias', 'Alta', 150000000.00, '2023-04-20'),
        (1, 'Incumplimiento de procedimientos internos para pagos', 'Media', 50000000.00, '2023-05-10'),
        (2, 'Adjudicación de contrato sin cumplir requisitos de publicidad', 'Alta', 5000000000.00, '2023-08-01'),
        (4, 'Alimentos entregados no cumplen con especificaciones técnicas', 'Grave', 750000000.00, '2023-03-15');
""")
conn.commit()
print("Datos insertados en la tabla 'hallazgos' exitosamente.")

c.execute("""
    UPDATE auditorias
    SET estado = 'En Proceso', fecha_fin = '2024-03-31'
    WHERE nombre_auditoria = 'Auditoría de Desempeño Gestión Ambiental CAR';
""")
conn.commit()
print("Estado de auditoría y fecha de fin actualizados.")

c.execute("""
    UPDATE hallazgos
    SET monto_afectado = 180000000.00
    WHERE id_hallazgo = 1;
""")
conn.commit()
print("Monto afectado del hallazgo 1 actualizado.")

print("\nVerificando cambios en auditorias (ID 3):")
result_auditoria = c.execute("SELECT * FROM auditorias WHERE id_auditoria = 3;").fetchone()
print(result_auditoria)

print("\nVerificando cambios en hallazgos (ID 1):")
result_hallazgo = c.execute("SELECT * FROM hallazgos WHERE id_hallazgo = 1;").fetchone()
print(result_hallazgo)

c.execute("""
    DELETE FROM hallazgos
    WHERE id_hallazgo = 2;
""")
conn.commit()
print("Hallazgo con ID 2 eliminado exitosamente.")

print("\nVerificando hallazgos restantes:")
result_hallazgos = c.execute("SELECT * FROM hallazgos;").fetchall()
for row in result_hallazgos:
    print(row)

c.execute("""
    INSERT OR REPLACE INTO funcionarios (id_funcionario, nombre, cargo, departamento, email)
    VALUES
        (1, 'Ana María Gómez', 'Auditor Principal', 'Financiero', 'ana.gomez@contraloria.gov.co');
""")
conn.commit()
print("Funcionario 1 actualizado (o insertado si no existía).")

c.execute("""
    INSERT OR REPLACE INTO funcionarios (id_funcionario, nombre, cargo, departamento, email)
    VALUES
        (5, 'Elena Castro', 'Analista de Datos', 'Tecnología', 'elena.castro@contraloria.gov.co');
""")
conn.commit()
print("Funcionario 5 insertado.")

print("\nLista de funcionarios actualizada:")
result_funcionarios = c.execute("SELECT * FROM funcionarios;").fetchall()
for row in result_funcionarios:
    print(row)

print("\nTodas las auditorías:")
result = c.execute("SELECT * FROM auditorias;").fetchall()
for row in result:
    print(row)

df_auditorias = pd.read_sql_query("SELECT * FROM auditorias;", conn)
print("\nAuditorías (DataFrame):")
print(df_auditorias)

print("\nNombres y cargos de los funcionarios:")
result = c.execute("SELECT nombre, cargo FROM funcionarios;").fetchall()
for row in result:
    print(row)

df_funcionarios_resumen = pd.read_sql_query("SELECT nombre, cargo FROM funcionarios;", conn)
print("\nNombres y Cargos de Funcionarios (DataFrame):")
print(df_funcionarios_resumen)

print("\nDepartamentos únicos de funcionarios:")
result = c.execute("SELECT DISTINCT departamento FROM funcionarios;").fetchall()
for row in result:
    print(row)

df_departamentos = pd.read_sql_query("SELECT DISTINCT departamento FROM funcionarios;", conn)
print("\nDepartamentos Únicos (DataFrame):")
print(df_departamentos)

print("\nAuditorías Finalizadas:")
result = c.execute("SELECT * FROM auditorias WHERE estado = 'Finalizada';").fetchall()
for row in result:
    print(row)

df_finalizadas = pd.read_sql_query("SELECT * FROM auditorias WHERE estado = 'Finalizada';", conn)
print("\nAuditorías Finalizadas (DataFrame):")
print(df_finalizadas)

print("\nHallazgos con monto afectado > 100,000,000:")
result = c.execute("SELECT * FROM hallazgos WHERE monto_afectado > 100000000;").fetchall()
for row in result:
    print(row)

df_hallazgos_grandes = pd.read_sql_query("SELECT * FROM hallazgos WHERE monto_afectado > 100000000;", conn)
print("\nHallazgos con Monto Afectado Alto (DataFrame):")
print(df_hallazgos_grandes)

print("\nFuncionarios del departamento Financiero y Auditor Senior:")
result = c.execute("SELECT * FROM funcionarios WHERE departamento = 'Financiero' AND cargo = 'Auditor Senior';").fetchall()
for row in result:
    print(row)

df_fin_senior = pd.read_sql_query("SELECT * FROM funcionarios WHERE departamento = 'Financiero' AND cargo = 'Auditor Senior';", conn)
print("\nFuncionarios Financieros Senior (DataFrame):")
print(df_fin_senior)

print("\nHallazgos de severidad Alta o Grave:")
result = c.execute("SELECT * FROM hallazgos WHERE severidad = 'Alta' OR severidad = 'Grave';").fetchall()
for row in result:
    print(row)

df_severidad_alta_grave = pd.read_sql_query("SELECT * FROM hallazgos WHERE severidad = 'Alta' OR severidad = 'Grave';", conn)
print("\nHallazgos de Severidad Alta o Grave (DataFrame):")
print(df_severidad_alta_grave)

print("\nAuditorías ordenadas por fecha de inicio (ASC):")
result = c.execute("SELECT * FROM auditorias ORDER BY fecha_inicio ASC;").fetchall()
for row in result:
    print(row)

df_auditorias_fecha = pd.read_sql_query("SELECT * FROM auditorias ORDER BY fecha_inicio ASC;", conn)
print("\nAuditorías por Fecha de Inicio (DataFrame):")
print(df_auditorias_fecha)

print("\nHallazgos ordenados por monto afectado (DESC):")
result = c.execute("SELECT * FROM hallazgos ORDER BY monto_afectado DESC;").fetchall()
for row in result:
    print(row)

df_hallazgos_monto_desc = pd.read_sql_query("SELECT * FROM hallazgos ORDER BY monto_afectado DESC;", conn)
print("\nHallazgos por Monto Afectado (Descendente, DataFrame):")
print(df_hallazgos_monto_desc)

print("\nLos 2 primeros funcionarios:")
result = c.execute("SELECT * FROM funcionarios LIMIT 2;").fetchall()
for row in result:
    print(row)

df_top_funcionarios = pd.read_sql_query("SELECT * FROM funcionarios LIMIT 2;", conn)
print("\nTop 2 Funcionarios (DataFrame):")
print(df_top_funcionarios)

print("\nNúmero total de auditorías:")
result = c.execute("SELECT COUNT(*) FROM auditorias;").fetchone()[0]
print(f"Total de auditorías: {result}")

print("\nSuma total de montos afectados:")
result = c.execute("SELECT SUM(monto_afectado) FROM hallazgos;").fetchone()[0]
print(f"Suma total de montos afectados: {result:,.2f}")

print("\nMonto promedio afectado por severidad:")
result = c.execute("SELECT severidad, AVG(monto_afectado) FROM hallazgos GROUP BY severidad;").fetchall()
for row in result:
    print(f"Severidad: {row[0]}, Promedio: {row[1]:,.2f}")

df_avg_monto_severidad = pd.read_sql_query("SELECT severidad, AVG(monto_afectado) as monto_promedio FROM hallazgos GROUP BY severidad;", conn)
print("\nMonto Promedio por Severidad (DataFrame):")
print(df_avg_monto_severidad)

print("\nNúmero de funcionarios por departamento:")
result = c.execute("SELECT departamento, COUNT(*) FROM funcionarios GROUP BY departamento;").fetchall()
for row in result:
    print(f"Departamento: {row[0]}, Cantidad: {row[1]}")

df_funcionarios_depto = pd.read_sql_query("SELECT departamento, COUNT(*) as cantidad_funcionarios FROM funcionarios GROUP BY departamento;", conn)
print("\nFuncionarios por Departamento (DataFrame):")
print(df_funcionarios_depto)

print("\nDepartamentos con más de un funcionario:")
result = c.execute("SELECT departamento, COUNT(*) FROM funcionarios GROUP BY departamento HAVING COUNT(*) > 1;").fetchall()
for row in result:
    print(f"Departamento: {row[0]}, Cantidad: {row[1]}")

df_depto_mas_uno = pd.read_sql_query("SELECT departamento, COUNT(*) as cantidad_funcionarios FROM funcionarios GROUP BY departamento HAVING COUNT(*) > 1;", conn)
print("\nDepartamentos con más de un Funcionario (DataFrame):")
print(df_depto_mas_uno)

print("\nHallazgos con el nombre de su auditoría (INNER JOIN):")
result = c.execute("""
    SELECT
        h.descripcion,
        h.severidad,
        a.nombre_auditoria,
        a.estado
    FROM
        hallazgos h
    INNER JOIN
        auditorias a ON h.id_auditoria = a.id_auditoria;
""").fetchall()
for row in result:
    print(row)

df_hallazgos_auditorias = pd.read_sql_query("""
    SELECT
        h.descripcion,
        h.severidad,
        a.nombre_auditoria,
        a.estado
    FROM
        hallazgos h
    INNER JOIN
        auditorias a ON h.id_auditoria = a.id_auditoria;
""", conn)
print("\nHallazgos y Auditorías (INNER JOIN, DataFrame):")
print(df_hallazgos_auditorias)

print("\nTodas las auditorías y sus hallazgos (LEFT JOIN):")
result = c.execute("""
    SELECT
        a.nombre_auditoria,
        a.estado,
        h.descripcion,
        h.severidad
    FROM
        auditorias a
    LEFT JOIN
        hallazgos h ON a.id_auditoria = h.id_auditoria;
""").fetchall()
for row in result:
    print(row)

df_auditorias_left_hallazgos = pd.read_sql_query("""
    SELECT
        a.nombre_auditoria,
        a.estado,
        h.descripcion,
        h.severidad
    FROM
        auditorias a
    LEFT JOIN
        hallazgos h ON a.id_auditoria = h.id_auditoria;
""", conn)
print("\nAuditorías y Hallazgos (LEFT JOIN, DataFrame):")
print(df_auditorias_left_hallazgos)

print("\nEjemplo de CROSS JOIN (limitado a 5 filas para no saturar):")
result = c.execute("""
    SELECT
        f.nombre, a.nombre_auditoria
    FROM
        funcionarios f
    CROSS JOIN
        auditorias a
    LIMIT 5;
""").fetchall()
for row in result:
    print(row)

df_cross_join_example = pd.read_sql_query("""
    SELECT
        f.nombre, a.nombre_auditoria
    FROM
        funcionarios f
    CROSS JOIN
        auditorias a
    LIMIT 5;
""", conn)
print("\nCROSS JOIN (Ejemplo limitado, DataFrame):")
print(df_cross_join_example)

print("\nAuditorías con al menos un hallazgo de severidad 'Grave' (usando subconsulta):")
result = c.execute("""
    SELECT
        nombre_auditoria,
        estado
    FROM
        auditorias
    WHERE
        id_auditoria IN (SELECT id_auditoria FROM hallazgos WHERE severidad = 'Grave');
""").fetchall()
for row in result:
    print(row)

df_auditorias_graves = pd.read_sql_query("""
    SELECT
        nombre_auditoria,
        estado
    FROM
        auditorias
    WHERE
        id_auditoria IN (SELECT id_auditoria FROM hallazgos WHERE severidad = 'Grave');
""", conn)
print("\nAuditorías con Hallazgos Graves (DataFrame):")
print(df_auditorias_graves)

print("\nFuncionarios que no son 'Auditor Principal' (usando subconsulta con NOT IN):")
result = c.execute("""
    SELECT
        nombre, cargo
    FROM
        funcionarios
    WHERE
        cargo NOT IN ('Auditor Principal');
""").fetchall()
for row in result:
    print(row)

df_no_auditor_principal = pd.read_sql_query("""
    SELECT
        nombre, cargo
    FROM
        funcionarios
    WHERE
        cargo NOT IN ('Auditor Principal');
""", conn)
print("\nFuncionarios que no son Auditor Principal (DataFrame):")
print(df_no_auditor_principal)

conn.close()