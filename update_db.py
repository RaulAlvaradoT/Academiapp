import re

# Leer el archivo
with open('database.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazar todos los ? con placeholders dinámicos
# Buscar patrones como VALUES (?, ?, ?) o WHERE x = ?
def replace_placeholders(match):
    full_match = match.group(0)
    # Contar cuántos ? hay
    count = full_match.count('?')
    # Crear reemplazo con {ph}
    result = full_match
    for i in range(count):
        result = result.replace('?', '{ph}', 1)
    return result

# Patrón para encontrar queries con ?
pattern = r"(VALUES\s*\([?,'\" \w]*\)|WHERE\s+[^'\"]*\?[^'\"]*|=\s*\?)"
content = re.sub(pattern, replace_placeholders, content, flags=re.IGNORECASE)

# Agregar cursor.close() antes de cada conn.close() que no lo tenga
lines = content.split('\n')
new_lines = []
for i, line in enumerate(lines):
    if 'conn.close()' in line and i > 0:
        # Verificar si la línea anterior ya tiene cursor.close()
        if 'cursor.close()' not in lines[i-1]:
            # Obtener la indentación
            indent = len(line) - len(line.lstrip())
            new_lines.append(' ' * indent + 'cursor.close()')
    new_lines.append(line)

content = '\n'.join(new_lines)

# Agregar ph = self.get_placeholder() al inicio de cada función que use {ph}
# Este paso es complejo, lo haremos manualmente

# Guardar el archivo
with open('database_updated.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Archivo actualizado guardado como database_updated.py")
print("Revisa el archivo y si está correcto, renómbralo a database.py")
