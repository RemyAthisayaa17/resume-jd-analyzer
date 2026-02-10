from typing import List

def generate_recommendations(
    missing_requirements: List[str],
    max_new_tokens: int = 120
) -> List[str]:
    """
    Generate clean, deterministic, professional recommendations
    based strictly on missing competencies.
    """

    if not missing_requirements:
        return [
            "Strong alignment detected. Continue deepening expertise in matched areas."
        ]

    recommendations = []

    for req in missing_requirements:
        if "performance" in req or "optimize" in req:
            recommendations.append(
                "Demonstrate performance optimization by describing measurable improvements such as reduced load time, improved responsiveness, or optimized rendering."
            )
        elif "collaborate" in req:
            recommendations.append(
                "Highlight collaboration experience by explicitly mentioning cross-functional work with designers, backend engineers, or product teams."
            )
        elif "debug" in req:
            recommendations.append(
                "Add concrete examples of debugging front-end issues, including the type of problems resolved and the impact of the fixes."
            )
        else:
            recommendations.append(
                f"Strengthen evidence of experience related to: {req}."
            )

    return recommendations[:6]
