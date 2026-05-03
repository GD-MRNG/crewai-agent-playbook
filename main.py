import sys
from datetime import date
from dotenv import load_dotenv

load_dotenv()

from src.crews.debate.crew import Debate
from src.crews.financial_researcher.crew import FinancialResearcher
from src.crews.stock_picker.crew import StockPicker


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <crew>")
        print("Available crews: debate, financial_researcher, stock_picker")
        sys.exit(1)

    crew_name = sys.argv[1]

    if crew_name == "debate":
        inputs = {"motion": "AI will do more harm than good"}
        Debate().crew().kickoff(inputs=inputs)
    elif crew_name == "financial_researcher":
        inputs = {
            "company": "Apple",
            "current_date": date.today().strftime("%B %d, %Y"),
        }
        FinancialResearcher().crew().kickoff(inputs=inputs)
    elif crew_name == "stock_picker":
        inputs = {
            "sector": "Technology",
            "current_date": date.today().strftime("%B %d, %Y"),
        }
        StockPicker().crew().kickoff(inputs=inputs)
    else:
        print(f"Unknown crew: {crew_name}")
        print("Available crews: debate, financial_researcher, stock_picker")
        sys.exit(1)


if __name__ == "__main__":
    main()
