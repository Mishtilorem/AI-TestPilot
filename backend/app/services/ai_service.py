import json
from sqlalchemy.orm import Session
from app.ai.factory import get_ai_provider
from app.ai.utils import parse_json, sanitize_selenium_script
from app.ai.prompts.test_case_prompt import TEST_CASE_SYSTEM_PROMPT, build_test_case_prompt
from app.ai.prompts.selenium_script_prompt import SCRIPT_SYSTEM_PROMPT, build_script_prompt
from app.ai.prompts.failure_analysis_prompt import ANALYSIS_SYSTEM_PROMPT, build_analysis_prompt
from app.models.test_case import TestCase
from app.models.test_result import TestResult
from app.repositories.test_case_repository import TestCaseRepository
from app.repositories.test_result_repository import TestResultRepository

test_case_repo = TestCaseRepository()
test_result_repo = TestResultRepository()


class AIService:
    async def generate_test_cases(
        self,
        db: Session,
        project_id: str,
        requirement_id: str,
        requirement_content: str,
        target_url: str,
    ) -> list[TestCase]:
        """Ask the AI to turn a requirement into test cases, then store them."""
        provider = get_ai_provider()
        raw = await provider.generate_json(
            TEST_CASE_SYSTEM_PROMPT,
            build_test_case_prompt(requirement_content, target_url),
        )
        data = parse_json(raw)

        created: list[TestCase] = []
        for item in data.get("test_cases", []):
            test_case = TestCase(
                project_id=project_id,
                requirement_id=requirement_id,
                title=item.get("title", "Untitled test case")[:500],
                description=item.get("description", ""),
                expected_result=item.get("expected_result", ""),
                generated_by_ai=True,
            )
            created.append(test_case_repo.create(db, test_case))
        return created

    async def generate_selenium_script(
        self, db: Session, test_case: TestCase, target_url: str
    ) -> TestCase:
        """Ask the AI to write a Selenium script for a test case and store it."""
        provider = get_ai_provider()
        raw = await provider.generate(
            SCRIPT_SYSTEM_PROMPT,
            build_script_prompt(
                test_case.title,
                test_case.description,
                test_case.expected_result,
                target_url,
            ),
        )
        test_case.selenium_script = sanitize_selenium_script(raw)
        return test_case_repo.update(db, test_case)

    async def analyze_failure(
        self, db: Session, result: TestResult, test_case: TestCase
    ) -> TestResult:
        """Ask the AI to explain a failed test, then store the analysis on the result."""
        provider = get_ai_provider()
        raw = await provider.generate_json(
            ANALYSIS_SYSTEM_PROMPT,
            build_analysis_prompt(
                test_case.title,
                test_case.selenium_script or "",
                result.logs or "",
            ),
        )
        data = parse_json(raw)
        # Store the human-readable parts as JSON text; keep confidence numeric.
        result.ai_analysis = json.dumps(
            {
                "root_cause": data.get("root_cause", ""),
                "explanation": data.get("explanation", ""),
                "possible_fixes": data.get("possible_fixes", []),
            }
        )
        try:
            result.ai_confidence = float(data.get("confidence", 0.0))
        except (TypeError, ValueError):
            result.ai_confidence = 0.0
        return test_result_repo.update(db, result)


ai_service = AIService()
