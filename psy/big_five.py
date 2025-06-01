questions = [
    (
        "Je suis quelqu'un qui parle facilement aux autres.",
        ["Fortement en désaccord", "En désaccord", "Neutre", "D'accord", "Fortement d'accord"]
    ),
    (
        "Je suis quelqu'un qui a tendance à critiquer les autres.",
        ["Fortement en désaccord", "En désaccord", "Neutre", "D'accord", "Fortement d'accord"]
    ),
    (
        "Je fais mon travail de manière méthodique.",
        ["Fortement en désaccord", "En désaccord", "Neutre", "D'accord", "Fortement d'accord"]
    ),
    (
        "Je suis souvent stressé(e) ou anxieux(se).",
        ["Fortement en désaccord", "En désaccord", "Neutre", "D'accord", "Fortement d'accord"]
    ),
    (
        "J'ai une imagination active.",
        ["Fortement en désaccord", "En désaccord", "Neutre", "D'accord", "Fortement d'accord"]
    )
    # Ajouter plus de questions pour chaque trait (Extraversion, Agréabilité, Conscience, Névrosisme, Ouverture)
]

def calculate_result(responses: str) -> str:
    """Calcule les scores pour les 5 grands traits de personnalité."""
    # Dans une vraie implémentation, on calculerait les scores pour chaque trait
    # en fonction des réponses. Ceci est un exemple simplifié.
    
    traits = {
        "Extraversion": 0,
        "Agréabilité": 0,
        "Conscience": 0,
        "Névrosisme": 0,
        "Ouverture": 0
    }
    
    # Ici, on devrait avoir une logique pour calculer chaque trait
    # en fonction des réponses spécifiques qui s'y rapportent
    
    result = "📊 Résultats du Test Big Five (OCEAN):\n\n"
    for trait, score in traits.items():
        result += f"{trait}: {score}/20\n"
    
    result += "\nInterprétation:\n"
    result += "- Extraversion: Sociabilité et énergie\n"
    result += "- Agréabilité: Compassion et coopération\n"
    result += "- Conscience: Auto-discipline et organisation\n"
    result += "- Névrosisme: Tendance à éprouver des émotions négatives\n"
    result += "- Ouverture: Appréciation pour l'art, l'aventure, les idées\n"
    result += "\nCes résultats sont indicatifs et ne constituent pas un diagnostic."
    
    return result