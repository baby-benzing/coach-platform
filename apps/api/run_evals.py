#!/usr/bin/env python
"""
Run evaluation suite for the workout planning agent.

Usage:
    python run_evals.py [--quick] [--verbose]

Options:
    --quick     Run only quick test cases
    --verbose   Print detailed output
"""

import asyncio
import argparse
import json
import sys
from datetime import datetime

from agents import WorkoutPlanningAgent
from agents.evals import (
    run_evaluation_suite,
    EVALUATION_TEST_CASES,
    PlanEvaluator,
)
from agents.evals.test_cases import QUICK_TEST_CASES


async def main():
    parser = argparse.ArgumentParser(description="Run agent evaluation suite")
    parser.add_argument("--quick", action="store_true", help="Run quick tests only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--output", "-o", help="Output file for results (JSON)")
    parser.add_argument("--test", "-t", help="Run specific test by name")
    args = parser.parse_args()

    print("=" * 60)
    print("WORKOUT PLANNING AGENT EVALUATION")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    # Select test cases
    if args.test:
        # Run specific test
        all_tests = EVALUATION_TEST_CASES + QUICK_TEST_CASES
        test_cases = [t for t in all_tests if args.test.lower() in t["name"].lower()]
        if not test_cases:
            print(f"No test found matching: {args.test}")
            sys.exit(1)
    elif args.quick:
        test_cases = QUICK_TEST_CASES
        print("Running QUICK test suite...")
    else:
        test_cases = EVALUATION_TEST_CASES
        print(f"Running FULL test suite ({len(test_cases)} tests)...")

    print()

    # Initialize agent
    agent = WorkoutPlanningAgent(
        coach_philosophy="Focus on movement quality and progressive overload."
    )

    # Run evaluation
    results = await run_evaluation_suite(
        agent=agent,
        test_cases=test_cases,
        verbose=args.verbose
    )

    # Print summary
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Average Score: {results['average_score']:.1%}")
    print()

    # Print individual results
    print("Test Results:")
    for r in results["results"]:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {r['name']}: {r['score']:.1%}")

    # Save to file if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    # Exit with appropriate code
    if results["passed"] == results["total_tests"]:
        print("\n All tests passed!")
        sys.exit(0)
    else:
        print(f"\n {results['failed']} test(s) failed")
        sys.exit(1)


async def run_single_test():
    """Run a single test for debugging."""
    test_case = QUICK_TEST_CASES[0]

    print(f"Running single test: {test_case['name']}")

    agent = WorkoutPlanningAgent()

    plan = await agent.generate_plan(
        assessment=test_case["assessment"],
        coach_preferences=test_case.get("coach_preferences", {})
    )

    print("\nGenerated Plan:")
    print(json.dumps(plan, indent=2)[:2000])

    evaluator = PlanEvaluator()
    result = evaluator.evaluate(plan, test_case)

    print(f"\nEvaluation: {result.summary}")
    if result.recommendations:
        print("Recommendations:")
        for rec in result.recommendations:
            print(f"  - {rec}")


if __name__ == "__main__":
    # Check for dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    asyncio.run(main())
