class DataExporter:
    def __init__(self, excel_manager):
        self.excel_manager = excel_manager
        
    def export_data(self, df, options):
        """
        Exporta datos a Excel con verificaciones y validación
        
        Args:
            df (DataFrame): DataFrame con los datos a exportar
            options (dict): Opciones de exportación
        """
        import pandas as pd
        from colorama import Fore, Style, init
        init()  # Inicializar colorama
        
        try:
            # Verificar que el DataFrame no esté vacío
            if df is None or df.empty:
                print(f"{Fore.RED}[ERROR] El DataFrame está vacío o es None{Style.RESET_ALL}")
                return False
                
            # Verificar columnas necesarias (ajustar según necesidades)
            expected_columns = ["display_id", "name", "asset_tag", "department_id", "user_id", "state"]
            existing_columns = df.columns.tolist()
            
            print(f"{Fore.CYAN}[INFO] Columnas en el DataFrame: {existing_columns}{Style.RESET_ALL}")
            
            # Verificar si hay columnas de criterios de búsqueda
            if not any(col in existing_columns for col in expected_columns):
                print(f"{Fore.YELLOW}[ADVERTENCIA] No se encontraron columnas esperadas en el DataFrame{Style.RESET_ALL}")
                # No interrumpir el proceso, seguir con las columnas existentes

            # Verificar opciones de salida
            if not options.get('output'):
                print(f"{Fore.RED}[ERROR] No se especificó archivo de salida{Style.RESET_ALL}")
                return False
                
            # Imprimir información detallada
            print(f"{Fore.CYAN}[INFO] Exportando {len(df)} filas a {options.get('output')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[INFO] Primeras filas del DataFrame:{Style.RESET_ALL}")
            print(df.head().to_string())
            
            # Exportar datos a Excel
            result = self.excel_manager.export_to_excel(df, options['output'])
            
            # Verificar resultado de exportación
            if result is False:
                print(f"{Fore.RED}[ERROR] La exportación a Excel falló{Style.RESET_ALL}")
                return False
                
            print(f"{Fore.GREEN}[ÉXITO] Exportación completada exitosamente a {options.get('output')}{Style.RESET_ALL}")
            
            # Mostrar en consola si es verbose
            if options.get('verbose'):
                print(df)
                
            return True
            
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Error al exportar datos: {str(e)}{Style.RESET_ALL}")
            import traceback
            print(f"{Fore.RED}[ERROR] Detalle del error:\n{traceback.format_exc()}{Style.RESET_ALL}")
            return False
