"""Карьерный советник. Атрошенко Б. С."""

from agents.base import BaseAgent
from models.career_advisor_resp import CareerAdvisorResponse


class CareerAdvisor(BaseAgent):

    def __init__(self):
        """Инициализатор."""
        super().__init__(CareerAdvisorResponse, name="CareerAdvisor")

    def build_prompt(self, input_data: str | dict) -> str:
        """
        Промпт задание.

        :param input_data: данные от Агента1.
        :return строка с заданием.
        """
        return (
            f"Role: {input_data.get("role")} \n"
            f"Skill Map: {input_data.get("skill_map")} \n"
            f"Salary Table: {input_data.get("salary_table")}"
            f"Create a development plan, a gap analysis, and an idea for a portfolio project."
        )

    def system_prompt(self) -> str:
        """Системный промпт c ролью и заданием для агента."""
        return """You are an experienced IT career consultant.
        
        Your task: based on the skill map and salary table, create the most realistic 
        3-month development plan for mastering the most in-demand skills that will 
        allow earning the maximum amount of money.
        
        Rules:
        - learning_path: exactly 3 phases of 30 days each — Foundation, Practice, Portfolio
        - Each phase contains a list of topics, each topic has at least 2 resources
          (course, book, website, or documentation with type specified)
          - Resources must be real (actual courses, books, documentation, websites, guides).
        - Each phase has a milestone — a specific measurable outcome
        - gap_analysis: a list of the most in-demand skills for maximum salary. Split into 
          quick_wins (things that can be covered in 2-4 weeks) and long_term (complex skills 
          requiring extended study of 3+ months). You can rely on skills with demand="critical" 
          and trend="growing".
        - portfolio_project: a concrete project idea with a title, description, 
          and a list of technologies (minimum 3 | maximum 6) from the skill_map
        
        Respond ONLY with valid JSON without markdown wrappers or explanations.
        
        Example JSON response:
        {
          "learning_path": [
            {
              "stage": "Foundation",
              "topics": [
                {
                  "theme": "RAG systems",
                  "resources": [
                    {
                      "name": "CS50",
                      "type": "course"
                    },
                    ...
                  ]
                },
                ...
              ],
              "milestone": "Learn to use RAG when building your own agents."
            },
            {
              "stage": "Practice",
              ...
            },
            ...
          ],
          "gap_analysis": {
            "quick_wins": [
              {
                "skill": "vLLM",
                "description": "Learn to deploy models on servers using vLLM Production Stack"
              },
              ...
            ],
            "long_term": [
              {
                "skill": "Machine learning algorithms",
                "description": "Understand and implement all core ML algorithms in PyTorch"
              },
              ...
            ]
          },
          "portfolio_project": {
            "title": "Multi-agent Telegram bot",
            "description": "Build a multi-agent system based on RAG with vector search",
            "skills_demonstrated": [
              "Qdrant", "RAG", "Agents", "Transformers"
            ]
          }
        }
        """