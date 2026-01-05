import re

# Leer database.py
with open('database.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar todas las funciones y agregar ph = self.get_placeholder() si usan ?
def process_functions(content):
    # Dividir en funciones
    lines = content.split('\n')
    result = []
    in_function = False
    function_has_placeholder = False
    function_start_indent = 0
    added_ph = False
    
    for i, line in enumerate(lines):
        # Detectar inicio de función
        if line.strip().startswith('def ') and '(self' in line:
            in_function = True
            function_has_placeholder = False
            added_ph = False
            # Obtener indentación de la función
            function_start_indent = len(line) - len(line.lstrip())
            result.append(line)
            continue
        
        # Si estamos en una función
        if in_function:
            # Verificar si la línea usa ?
            if '?' in line and ('execute' in line or 'VALUES' in line or 'WHERE' in line):
                function_has_placeholder = True
            
            # Si encontramos la docstring o el primer try/conn, agregar ph
            if function_has_placeholder and not added_ph:
                if ('"""' in line and i > 0 and '"""' in lines[i-1]) or \
                   ('try:' in line) or \
                   ('conn = self.get_connection()' in line):
                    # Agregar ph después de la docstring o antes del try
                    if 'conn = self.get_connection()' in line:
                        result.append(line)
                        result.append(' ' * (function_start_indent + 8) + 'ph = self.get_placeholder()')
                        added_ph = True
                        continue
            
            # Detectar fin de función (nueva función o fin de clase)
            if line.strip().startswith('def ') or (line.strip().startswith('class ') and in_function):
                in_function = False
        
        result.append(line)
    
    return '\n'.join(result)

# Procesar funciones
content = process_functions(content)

# Reemplazar ? con {ph} en queries SQL
# Hacer múltiples pasadas para diferentes patrones
patterns = [
    (r"VALUES \((\?(?:,\s*\?)*)\)", lambda m: f"VALUES ({', '.join(['{ph}'] * m.group(1).count('?'))})"),
    (r"WHERE\s+(\w+)\s*=\s*\?", r"WHERE \1 = {ph}"),
    (r"WHERE\s+(\w+)\s+BETWEEN\s+\?\s+AND\s+\?", r"WHERE \1 BETWEEN {ph} AND {ph}"),
    (r"AND\s+(\w+)\s*=\s*\?", r"AND \1 = {ph}"),
]

for pattern, replacement in patterns:
    content = re.sub(pattern, replacement, content)

# Agregar cursor.close() antes de conn.close() si no existe
lines = content.split('\n')
result = []
for i, line in enumerate(lines):
    if 'conn.close()' in line:
        # Verificar si las 3 líneas anteriores tienen cursor.close()
        has_cursor_close = False
        for j in range(max(0, i-3), i):
            if 'cursor.close()' in lines[j]:
                has_cursor_close = True
                break
        
        if not has_cursor_close:
            indent = len(line) - len(line.lstrip())
            result.append(' ' * indent + 'cursor.close()')
    
    result.append(line)

content = '\n'.join(result)

# Guardar
with open('database.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Archivo database.py actualizado")
print("Se agregaron:")
print("  - ph = self.get_placeholder() en funciones que lo necesitan")
print("  - Reemplazos de ? por {ph}")
print("  - cursor.close() antes de conn.close()")
