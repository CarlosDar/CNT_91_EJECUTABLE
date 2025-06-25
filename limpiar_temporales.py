#!/usr/bin/env python3
"""
Script para limpiar archivos temporales de openpyxl que pueden causar problemas
al abrir archivos Excel.

Uso: python limpiar_temporales.py
"""

import os
import tempfile
import glob

def limpiar_archivos_temporales():
    """
    Limpia los archivos temporales de openpyxl.
    """
    try:
        # Obtener el directorio temporal del sistema
        temp_dir = tempfile.gettempdir()
        print(f"Buscando archivos temporales en: {temp_dir}")
        
        # Buscar archivos temporales de openpyxl
        pattern = os.path.join(temp_dir, "openpyxl.*")
        temp_files = glob.glob(pattern)
        
        if not temp_files:
            print("✅ No se encontraron archivos temporales de openpyxl.")
            return
        
        print(f"Encontrados {len(temp_files)} archivos temporales:")
        
        # Eliminar archivos temporales
        eliminados = 0
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    eliminados += 1
                    print(f"  ✅ Eliminado: {os.path.basename(temp_file)}")
                else:
                    print(f"  ⚠️  No existe: {os.path.basename(temp_file)}")
            except Exception as e:
                print(f"  ❌ Error al eliminar {os.path.basename(temp_file)}: {e}")
        
        print(f"\n✅ Se eliminaron {eliminados} archivos temporales de openpyxl.")
        print("Ahora deberías poder abrir los archivos Excel sin problemas.")
        
    except Exception as e:
        print(f"❌ Error al limpiar archivos temporales: {e}")

def verificar_procesos_excel():
    """
    Verifica si hay procesos de Excel ejecutándose.
    """
    try:
        import psutil
        
        procesos_excel = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'excel' in proc.info['name'].lower():
                    procesos_excel.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if procesos_excel:
            print(f"\n⚠️  Se encontraron {len(procesos_excel)} procesos de Excel ejecutándose:")
            for proc in procesos_excel:
                print(f"  - PID {proc['pid']}: {proc['name']}")
            print("Considera cerrar Excel si tienes problemas para abrir archivos.")
        else:
            print("\n✅ No se encontraron procesos de Excel ejecutándose.")
            
    except ImportError:
        print("\n⚠️  Para verificar procesos de Excel, instala psutil: pip install psutil")
    except Exception as e:
        print(f"\n❌ Error al verificar procesos: {e}")

if __name__ == "__main__":
    print("🧹 Limpiador de archivos temporales de openpyxl")
    print("=" * 50)
    
    limpiar_archivos_temporales()
    verificar_procesos_excel()
    
    print("\n" + "=" * 50)
    print("✅ Limpieza completada.") 