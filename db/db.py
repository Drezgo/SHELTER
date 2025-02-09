# Функції для взаємодії з SQLite

import sqlite3

from config import DB_PATH, STEPS_SELECT_RESULTS

def store_coeficients_attenuation_coefficients():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # завантажуємо вибір користувача
    cursor.execute("SELECT Material, Thickness FROM Uses_choice_G1")
    user_data = cursor.fetchall()

    coefficients = []
    for row in user_data:
        material, thickness = row

        cursor.execute(
            f"""
            SELECT 
            neutron_dose_coefficient as kn,
            gamma_dose_coefficient as ky

            FROM attenuation_coefficients
            WHERE material_name = '{material}' AND material_thickness = '{thickness}'
            """
        )
        data = cursor.fetchone()

        coefficients.append(
            {"material": material, "thickness": thickness, "kn": data[0], "ky": data[1]}
        )

    STEPS_SELECT_RESULTS["coefficients"] = coefficients
    connection.close()

def load_materials():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT 
        name
        
        FROM materials
        ORDER BY name
        """
    )
    data = cursor.fetchall()
    connection.close()
    return data

def load_shelter_classes():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT 
        protection_class, 
        description, 
        overpressure_air_blast_wave,
        radiation_protection_level
        
        FROM storage_classes
        ORDER BY protection_class
        """
    )
    data = cursor.fetchall()
    connection.close()
    return data

def load_building_types():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT 
        name
        
        FROM building_types
        ORDER BY name
        """
    )
    data = cursor.fetchall()
    connection.close()
    return data

def load_building_height_by_type(building_type: str):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT 
        distinct building_height 
        
        FROM location_condition_coefficients 
        WHERE building_type_name = '{building_type}'
        """
    )
    data = cursor.fetchall()
    connection.close()
    return data

def load_building_density_by_type(building_type: str):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT 
        distinct building_density 
        
        FROM location_condition_coefficients 
        WHERE building_type_name = '{building_type}'
        """
    )
    data = cursor.fetchall()
    connection.close()
    return data

def load_wall_thickness_by_material(material: str):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT
        distinct wall_thickness

        FROM building_coefficients
        WHERE wall_material_name = '{material}'
        """
    )
    data = cursor.fetchall()
    connection.close()
    return data

def load_wall_materials():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT 
        name
        
        FROM wall_materials
        ORDER BY name
        """
    )
    data = cursor.fetchall()
    connection.close()
    return data

def get_shelter_class(protection_class: str):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT 
        protection_class, 
        description, 
        overpressure_air_blast_wave,
        radiation_protection_level
        
        FROM storage_classes
        WHERE protection_class = '{protection_class}'
        """
    )
    result = cursor.fetchone()
    connection.close()
    return result

def get_coefficient_zab(
    building_type_name: str, building_height: str, building_density: int
):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT 
        coefficient
        
        FROM location_condition_coefficients
        WHERE building_type_name = '{building_type_name}' AND
                building_height = '{building_height}' AND
                building_density = {building_density}
        """
    )
    result = cursor.fetchone()
    connection.close()
    return result

def get_coefficient_bud(
    wall_material_name: str,
    building_type_name: str,
    wall_thickness: int,
    area_relation_percent: int,
):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT 
        coefficient
        
        FROM building_coefficients
        WHERE building_type_name = '{building_type_name}' AND
                wall_material_name = '{wall_material_name}' AND
                wall_thickness = {wall_thickness} AND
                area_relation_percent = {area_relation_percent}
        """
    )
    result = cursor.fetchone()
    connection.close()
    return result



