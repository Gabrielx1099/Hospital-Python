"""
Dataset simulado de síntomas -> especialidad para el Hospital Carlos Lanfranco La Hoz.
Este dataset es simulado con fines académicos y no proviene de historiales clínicos reales.
"""

import os
import csv
import random

# Definir especialidades tal como están en la base de datos (sin tildes)
ESPECIALIDADES = [
    'Cardiologia',
    'Pediatria',
    'Ginecologia',
    'Traumatologia',
    'Medicina General',
    'Oftalmologia',
    'Neurologia',
    'Dermatologia'
]

# Síntomas base por especialidad
SINTOMAS_BASE = {
    'Cardiologia': [
        "dolor en el pecho", "presion en el pecho", "palpitaciones en el corazon",
        "arritmia", "taquicardia", "dolor que se va al brazo izquierdo",
        "falta de aire al hacer esfuerzo", "agitacion al caminar", "presion arterial alta",
        "dolor punzante en el pecho", "siento que el corazon late muy rapido", "soplo en el corazon",
        "insuficiencia cardiaca", "angina de pecho", "siento latidos desordenados",
        "dolor de pecho al respirar", "sensacion de ahogo en el pecho", "cansancio por presion alta",
        "dolor en la zona del corazon", "palpitaciones fuertes durmiendo"
    ],
    'Pediatria': [
        "mi hijo tiene fiebre", "mi bebe llora mucho y no duerme", "mi hijito esta con tos",
        "mi nena tiene sarpullido", "el bebe no quiere tomar teta", "mi niño tiene dolor de estomago",
        "mi bebe vomito la leche", "fiebre alta en mi hijo", "gripe de mi recien nacido",
        "mi nene tiene moquito y estornuda", "el niño tiene diarrea", "vacunas para mi bebe",
        "mi hijito no quiere comer", "ronchas en la piel de mi bebe", "infeccion al oido de mi niño",
        "mi hijita se ha caido y llora", "tos con flema en mi nene", "bebe con colicos de gases",
        "control de crecimiento de mi hijo", "mi bebe tiene el ojo con lagaña"
    ],
    'Ginecologia': [
        "retraso en mi menstruacion", "dolor pelvico fuerte", "flujo vaginal con mal olor",
        "control de embarazo", "sangrado fuera de mi periodo", "dolor en los ovarios",
        "indigestión y nauseas de gestante", "flujo vaginal blanco y picazón", "infeccion vaginal",
        "mi periodo no llega hace un mes", "quistes en el ovario", "menopausia y calores",
        "control prenatal", "dolor en las mamas", "ecografia de embarazo",
        "menstruacion muy abundante", "colicos menstruales insoportables", "metodo anticonceptivo",
        "sangrado vaginal anormal", "descarte de cancer de cuello uterino"
    ],
    'Traumatologia': [
        "me doble el tobillo", "dolor fuerte de rodilla", "posible fractura de muñeca",
        "me duele la columna baja", "luxacion de hombro", "me cai de la bicicleta y me duele la cadera",
        "dolor de espalda que no me deja pararme", "esguince de tobillo", "lesion en el codo jugando futbol",
        "me duele la articulacion", "inflamacion en la muñeca por golpe", "hueso roto",
        "desgarro muscular en el muslo", "dolor de cuello por caida", "me duele el talon al pisar",
        "no puedo mover el brazo despues de un golpe", "me golpee el codo y se hincho", "tengo reumatismo en las rodillas",
        "tiron en la espalda baja", "fractura de dedo"
    ],
    'Medicina General': [
        "resfriado comun", "dolor de cabeza leve", "malestar general y cuerpo pesado",
        "indigestión estomacal", "tengo dolor de garganta", "fiebre leve de un dia",
        "gripe con estornudos", "necesito chequeo general medico", "infeccion urinaria leve",
        "tengo tos seca", "dolor de estomago leve", "me siento debil y cansado",
        "tengo nauseas", "estreñimiento de hace dias", "dolor de oido leve",
        "necesito orden para analisis de sangre", "presion baja y mareo leve", "dolor de cuerpo por gripe",
        "acidez estomacal despues de comer", "tengo una picadura de insecto"
    ],
    'Oftalmologia': [
        "veo borroso", "me arden los ojos", "tengo enrojecimiento en el ojo",
        "siento arenilla en la vista", "mi vision ha disminuido", "dolor en el ojo derecho",
        "veo doble", "tengo catarata", "medida de vista para lentes",
        "picazon en los ojos por alergia", "tengo conjuntivitis", "veo destellos de luz",
        "ojo seco y cansado", "se me nubla la vista al leer", "infeccion en el parpado",
        "tengo un orzuelo en el ojo", "presion alta en los ojos", "glaucoma control",
        "sensibilidad fuerte a la luz", "veo manchas negras flotando"
    ],
    'Neurologia': [
        "dolor de cabeza migraña fuerte", "migrañas constantes", "adormecimiento de la mitad del cuerpo",
        "hormigueo en las manos y pies", "mareos y desmayo de la nada", "convulsiones repentinas",
        "perdida de memoria y desorientacion", "paralisis facial temporal", "tengo tics nerviosos",
        "dolor de cabeza cronico con nauseas", "siento zumbido de oidos y mareo", "falta de equilibrio al caminar",
        "demencia y confusion", "temblor involuntario en las manos", "siento electricidad en la cabeza",
        "dificultad para hablar de pronto", "derrame cerebral secuelas", "insomnio severo de origen nervioso",
        "dolor de cabeza que no calma con pastillas", "desvanecimiento sin causa"
    ],
    'Dermatologia': [
        "ronchas rojas en la piel", "mancha extraña que pica", "lunar que cambio de tamaño",
        "picazon extrema y resequedad", "acne severo en la cara", "alergia en la piel con ampollas",
        "caida de cabello excesiva", "hongos en las uñas del pie", "sarpullido en el cuerpo",
        "quemadura de sol con ampollas", "manchas blancas en la cara", "verruga en el cuello",
        "caspa extrema", "picadura infectada con pus en la piel", "tengo psoriasis",
        "piel muy roja e inflamada", "costras en el cuero cabelludo", "manchas oscuras en la piel",
        "urticaria por comida", "eccema seco en los brazos"
    ]
}

# Modificadores coloquiales peruanos y variaciones
PREFIXES = [
    "", "doctor ", "buenas tardes doctor ", "buenos dias ", "hola ", "ayuda por favor ",
    "tengo ", "siento ", "presento ", "ultimamente tengo ", "desde hace dias tengo ",
    "me ha dado ", "de la nada tengo ", "tengo un ", "siento un ", "me salio "
]

SUFFIXES = [
    "", " bien fuerte", " y me duele bastante", " constante", " que no se me pasa",
    " por ratos", " feo", " que me asusta", " hace tres dias", " y me da miedo",
    " urgente", " y no puedo mas", " y necesito cita", " y malestar", " de un momento a otro"
]

def generar_dataset():
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    filepath = os.path.join(data_dir, 'sintomas_especialidad.csv')
    
    registros = []
    
    for especialidad, sintomas in SINTOMAS_BASE.items():
        frases_generadas = set()
        
        # 1. Agregar los síntomas base tal cual
        for s in sintomas:
            frases_generadas.add(s)
            
        # 2. Generar variaciones hasta tener al menos 100 frases únicas por especialidad
        intentos = 0
        while len(frases_generadas) < 100 and intentos < 2000:
            sintoma = random.choice(sintomas)
            prefijo = random.choice(PREFIXES)
            sufijo = random.choice(SUFFIXES)
            
            # Combinar
            if prefijo:
                # Si el sintoma ya empieza con "tengo" o "siento" y el prefijo es "tengo"/"siento", evitar redundancia
                if (prefijo.strip() in ["tengo", "siento", "tengo un", "siento un"]) and (sintoma.startswith("tengo") or sintoma.startswith("siento") or sintoma.startswith("me ") or sintoma.startswith("mi ")):
                    phrase = sintoma
                elif sintoma.startswith("mi ") or sintoma.startswith("el "):
                    phrase = f"{prefijo.strip()} {sintoma}"
                else:
                    phrase = f"{prefijo.strip()} {sintoma}"
            else:
                phrase = sintoma
                
            if sufijo:
                phrase = f"{phrase} {sufijo.strip()}"
                
            # Limpieza básica
            phrase = phrase.replace("  ", " ").strip()
            
            # Asegurar longitud razonable y unicidad
            if len(phrase) > 10 and phrase not in frases_generadas:
                frases_generadas.add(phrase)
            
            intentos += 1
            
        # Si por alguna razón no se llega a 100, rellenamos duplicando con pequeñas variaciones
        for f in list(frases_generadas)[:100]:
            registros.append({'texto': f, 'especialidad': especialidad})
            
    # Guardar en CSV
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['texto', 'especialidad'])
        writer.writeheader()
        writer.writerows(registros)
        
    print(f"✅ Dataset generado exitosamente en '{filepath}' con {len(registros)} registros ({len(registros)//len(ESPECIALIDADES)} por especialidad).")

if __name__ == '__main__':
    generar_dataset()
