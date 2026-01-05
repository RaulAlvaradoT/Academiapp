import re

# Leer archivo
with open('database.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Patrón para encontrar cursor.execute(''' ... ''', (...)) que contiene {ph}
# y agregarle la f antes de las comillas si no la tiene
def fix_execute_statements(content):
    # Buscar execute(''' ... ''') que contiene {ph}
    pattern = r"cursor\.execute\(('''[\s\S]*?''')\s*,?\s*(\([^)]*\))?\)"
    
    def replacer(match):
        query = match.group(1)
        params = match.group(2) if match.group(2) else ''
        
        # Si contiene {ph} y no tiene f antes de las comillas
        if '{ph}' in query and not query.startswith("f'''"):
            query = 'f' + query
        
        if params:
            return f"cursor.execute({query}, {params})"
        else:
            return f"cursor.execute({query})"
    
    content = re.sub(pattern, replacer, content)
    return content

# Aplicar corrección
content = fix_execute_statements(content)

# Buscar funciones que usan {ph} y agregar ph = self.get_placeholder()
# si no lo tienen ya
lines = content.split('\n')
result = []
i = 0

while i < len(lines):
    line = lines[i]
    result.append(line)
    
    # Si es una definición de función
    if line.strip().startswith('def ') and '(self' in line:
        # Buscar si usa {ph} en las siguientes líneas
        uses_ph = False
        has_ph_declaration = False
        func_end = i + 1
        
        # Buscar hasta el final de la función
        while func_end < len(lines) and not (lines[func_end].strip().startswith('def ') and func_end > i + 3):
            if '{ph}' in lines[func_end]:
                uses_ph = True
            if 'ph = self.get_placeholder()' in lines[func_end]:
                has_ph_declaration = True
            func_end += 1
        
        # Si usa {ph} pero no tiene la declaración
        if uses_ph and not has_ph_declaration:
            # Encontrar dónde insertar (después de la docstring o al inicio)
            insert_pos = i + 1
            
            # Saltar docstring si existe
            if insert_pos < len(lines) and '"""' in lines[insert_pos]:
                insert_pos += 1
                while insert_pos < len(lines) and '"""' not in lines[insert_pos]:
                    insert_pos += 1
                insert_pos += 1
            
            # Saltar líneas en blanco
            while insert_pos < len(lines) and lines[insert_pos].strip() == '':
                insert_pos += 1
            
            # Obtener indentación
            if insert_pos < len(lines):
                indent = len(lines[insert_pos]) - len(lines[insert_pos].lstrip())
                # Insertar ph declaration
                ph_line = ' ' * indent + 'ph = self.get_placeholder()'
                lines.insert(insert_pos, ph_line)
    
    i += 1

content = '\n'.join(lines)

# Guardar
with open('database.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Archivo database.py corregido")
print("  - Se agregó 'f' antes de strings con {ph}")
print("  - Se agregó ph = self.get_placeholder() donde faltaba")
