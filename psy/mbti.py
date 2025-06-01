questions = [
    (
        "En général, vous préférez:",
        ["Être entouré de gens", "Rester seul ou avec peu de gens"]
    ),
    (
        "Quand vous apprenez quelque chose de nouveau, vous préférez:",
        ["Comprendre la théorie d'abord", "Essayer directement"]
    ),
    (
        "Lorsque vous prenez une décision, vous comptez surtout sur:",
        ["Vos sentiments et valeurs", "La logique et l'objectivité"]
    ),
    (
        "Dans votre vie quotidienne, vous préférez:",
        ["Planifier à l'avance", "Improviser au fur et à mesure"]
    )
    # Ajouter plus de questions pour chaque dimension MBTI
]

def calculate_result(responses):
    """Détermine le type MBTI en fonction des réponses."""
    # Les réponses déterminent les préférences sur 4 dimensions:
    # E/I, S/N, T/F, J/P
    
    # Exemple simplifié - dans une vraie implémentation, on aurait plus de questions
    # et une logique plus complexe pour déterminer le type
    
    mbti_type = []
    
    # Extraversion (E) vs Introversion (I)
    mbti_type.append('E' if sum(responses[0::4]) < len(responses[0::4])/2 else 'I')
    
    # Sensation (S) vs Intuition (N)
    mbti_type.append('S' if sum(responses[1::4]) < len(responses[1::4])/2 else 'N')
    
    # Pensée (T) vs Sentiment (F)
    mbti_type.append('T' if sum(responses[2::4]) < len(responses[2::4])/2 else 'F')
    
    # Jugement (J) vs Perception (P)
    mbti_type.append('J' if sum(responses[3::4]) < len(responses[3::4])/2 else 'P')
    
    type_str = ''.join(mbti_type)
    
    descriptions = {
        "INTJ": "L'Architecte - Stratège créatif et original.",
        "INTP": "Le Logicien - Innovateur théorique assoiffé de connaissances.",
        "ENTJ": "Le Commandant - Leader charismatique et visionnaire.",
        "ENTP": "L'Innovateur - Inventeur curieux et astucieux.",
        # Ajouter les autres types...
    }
    
    result = f"Votre type MBTI est: {type_str}\n\n"
    result += descriptions.get(type_str, "Description non disponible pour ce type.")
    result += "\n\nLe MBTI est un indicateur de personnalité qui catégorise les individus en 16 types."
    
    return result