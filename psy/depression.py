questions = [
    (
        "Peu d'intérêt ou de plaisir à faire les choses",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Sentiment de tristesse, dépression ou désespoir",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Problèmes de sommeil (difficulté à dormir, sommeil agité ou excessif)",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Sensation de fatigue ou manque d'énergie",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Perte d'appétit ou excès alimentaire",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Sentiment d'échec ou déception envers soi-même",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Difficulté à se concentrer (lecture, télévision, etc.)",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Mouvements ou parole si lents que les autres pourraient le remarquer, ou au contraire agitation",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    ),
    (
        "Pensées que vous seriez mieux mort ou de vous faire du mal d'une certaine manière",
        ["Pas du tout", "Plusieurs jours", "Plus de la moitié des jours", "Presque tous les jours"]
    )
]

def calculate_result(responses):
    """Calcule le score PHQ-9 et fournit une interprétation."""
    score = sum(responses)
    
    result = f"Votre score PHQ-9 est: {score}/27\n\n"
    
    if score < 5:
        result += "Pas de dépression significative."
    elif 5 <= score <= 9:
        result += "Symptômes dépressifs légers."
    elif 10 <= score <= 14:
        result += "Symptômes dépressifs modérés."
    elif 15 <= score <= 19:
        result += "Symptômes dépressifs modérément sévères."
    else:
        result += "Symptômes dépressifs sévères."
    
    result += "\n\nCe test (PHQ-9) est un outil de dépistage et ne remplace pas un diagnostic professionnel. "
    result += "Si vos résultats suggèrent une possible dépression, veuillez consulter un professionnel de santé."
    
    return result