from typing import Dict, List


class SolutionAgent:
    def __init__(
        self,
        knowledge_base: Dict[str, Dict[str, List[str]]],
        llm_service=None
    ):
        """
        knowledge_base: Disease to solutions mapping
        llm_service: Optional Groq or LLM client
        """
        self.knowledge_base = knowledge_base
        self.llm_service = llm_service

    def recommend_solution(
        self,
        crop: str,
        disease: str,
        severity_info: Dict[str, str]
    ) -> Dict[str, List[str]]:
        """
        Always returns non-empty treatment & prevention.
        Knowledge base is the source of truth.
        LLM is used only as an enhancement.
        """

        # 1️⃣ Always start from knowledge base
        base_solution = self._recommend_from_kb(disease, severity_info)

        # 2️⃣ If no LLM, return KB solution
        if not self.llm_service:
            return base_solution

        # 3️⃣ Try enhancing with LLM (safe)
        llm_solution = self._recommend_with_llm(
            crop,
            disease,
            severity_info
        )

        # 4️⃣ Merge results safely (LLM never overwrites KB with empty)
        return {
            "treatment": (
                llm_solution.get("treatment")
                if llm_solution.get("treatment")
                else base_solution["treatment"]
            ),
            "prevention": (
                llm_solution.get("prevention")
                if llm_solution.get("prevention")
                else base_solution["prevention"]
            )
        }

    def _recommend_from_kb(
        self,
        disease: str,
        severity_info: Dict[str, str]
    ) -> Dict[str, List[str]]:

        severity = severity_info.get("risk_level", "Low")
        disease_data = self.knowledge_base.get(disease)

        # Fallback if disease not found
        if not disease_data:
            return {
                "treatment": ["Consult a local agriculture expert"],
                "prevention": ["Monitor crop health regularly"]
            }

        treatments = list(disease_data.get("treatment", []))
        prevention = list(disease_data.get("prevention", []))

        if severity in ["High", "Critical"]:
            treatments.extend(disease_data.get("advanced_treatment", []))

        return {
            "treatment": treatments,
            "prevention": prevention
        }

    def _recommend_with_llm(
        self,
        crop: str,
        disease: str,
        severity_info: Dict[str, str]
    ) -> Dict[str, List[str]]:

        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert agricultural advisor."
                },
                {
                    "role": "user",
                    "content": (
                        f"Crop: {crop}\n"
                        f"Disease: {disease}\n"
                        f"Severity: {severity_info}\n\n"
                        "Provide treatment and prevention steps as JSON with keys "
                        "'treatment' and 'prevention'."
                    )
                }
            ]

            response = self.llm_service.generate(messages)

            return {
                "treatment": response.get("treatment", []),
                "prevention": response.get("prevention", [])
            }

        except Exception:
            # Never fail solution generation
            return {
                "treatment": [],
                "prevention": []
            }
