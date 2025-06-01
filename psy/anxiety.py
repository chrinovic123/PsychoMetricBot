questions = [
    (
        "Sentiment de nervosité, d'anxiété ou de tension",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Incapacité à arrêter ou à contrôler les inquiétudes",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Inquiétude excessive à propos de différentes choses",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Difficulté à se détendre",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Agitation si intense qu'il est difficile de rester assis tranquillement",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Devenir facilement agacé ou irritable",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Sentiment de peur comme si quelque chose de terrible allait arriver",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    )
]

def calculate_result(responses):
    """Calcule le score GAD-7 et fournit une interprétation."""
    score = sum(responses)
    
    result = f"Votre score GAD-7 est: {score}/21\n\n"
    
    if score < 5:
        result += "Pas d'anxiété significative."
    elif 5 <= score <= 9:
        result += "Anxiété légère."
    elif 10 <= score <= 14:
        result += "Anxiété modérée."
    else:
        result += "Anxiété sévère."
    
    result += "\n\nCe test (GAD-7) est un outil de dépistage et ne remplace pas un diagnostic professionnel. "
    result += "Si vos résultats suggèrent une possible anxiété, veuillez consulter un professionnel de santé."
    
    return result