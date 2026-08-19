from datetime import date, timedelta
import re
from math import ceil

class RequirementAgent:
    def run(self, description):
        text = description.lower()

        modules = []
        keyword_modules = {
            "login": "Authentication",
            "user": "User Management",
            "student": "Student Management",
            "admin": "Admin Management",
            "exam": "Examination Module",
            "question": "Question Management",
            "quiz": "Quiz Module",
            "payment": "Payment Module",
            "course": "Course Management",
            "result": "Result Management",
            "report": "Reporting",
            "notification": "Notification System",
            "chat": "Chat System",
            "database": "Database Management",
            "security": "Security",
            "attendance": "Attendance Management",
            "library": "Library Management",
            "inventory": "Inventory Management",
        }

        for key, module in keyword_modules.items():
            if key in text and module not in modules:
                modules.append(module)

        # Useful defaults when the description is broad.
        if not modules:
            modules = [
                "User Management",
                "Core Application Module",
                "Database Management",
                "Testing & Quality",
                "Reporting"
            ]

        functional = [
            f"The system shall provide {m.lower()} functionality."
            for m in modules
        ]

        non_functional = [
            "The system should provide secure authentication and authorization.",
            "The system should validate user input.",
            "The system should maintain reliable data storage.",
            "The system should provide a responsive user interface.",
            "The system should handle errors gracefully."
        ]

        return {
            "project": description[:100],
            "modules": modules,
            "functional_requirements": functional,
            "non_functional_requirements": non_functional
        }


class PlanningAgent:
    def run(self, requirements):
        tasks = []
        base_tasks = [
            ("Project setup", 1, "High"),
            ("Requirements validation", 1, "High"),
            ("System architecture", 2, "High"),
            ("Database design", 2, "High"),
        ]

        for name, days, priority in base_tasks:
            tasks.append({
                "task": name,
                "duration": days,
                "priority": priority,
                "status": "Pending"
            })

        for module in requirements["modules"]:
            duration = 2
            if "Examination" in module or "Payment" in module:
                duration = 4
            elif "Management" in module:
                duration = 3

            tasks.append({
                "task": f"Develop {module}",
                "duration": duration,
                "priority": "High" if module in ["Authentication", "Security"] else "Medium",
                "status": "Pending"
            })

        tasks += [
            {"task": "Integration", "duration": 2, "priority": "High", "status": "Pending"},
            {"task": "User acceptance review", "duration": 1, "priority": "Medium", "status": "Pending"},
            {"task": "Deployment preparation", "duration": 1, "priority": "Medium", "status": "Pending"},
        ]
        return tasks


class SchedulingAgent:
    def run(self, tasks):
        current = date.today()
        schedule = []
        for i, task in enumerate(tasks):
            start = current
            end = current + timedelta(days=max(task["duration"] - 1, 0))
            schedule.append({
                "task": task["task"],
                "start": start.isoformat(),
                "end": end.isoformat(),
                "duration": task["duration"],
                "priority": task["priority"]
            })
            current = end + timedelta(days=1)

        total_days = sum(t["duration"] for t in tasks)
        return {
            "schedule": schedule,
            "total_days": total_days,
            "estimated_completion": (date.today() + timedelta(days=max(total_days - 1, 0))).isoformat()
        }


class TestingAgent:
    def run(self, requirements, tasks):
        tests = [
            ("Authentication", "Verify valid and invalid login"),
            ("Input Validation", "Verify empty, invalid and boundary inputs"),
            ("Authorization", "Verify users cannot access unauthorized features"),
            ("Database", "Verify create, read, update and delete operations"),
            ("Error Handling", "Verify the application handles invalid operations"),
            ("Integration", "Verify modules communicate correctly"),
            ("Performance", "Verify important pages/functions respond acceptably"),
        ]

        # Add module-specific tests.
        for module in requirements["modules"]:
            tests.append((module, f"Verify core functionality of {module.lower()}"))

        return [
            {"module": m, "test_case": t, "status": "Not Run"}
            for m, t in tests
        ]


class RiskAgent:
    def run(self, requirements, tasks):
        risks = [
            {
                "risk": "Requirement changes",
                "probability": "Medium",
                "impact": "High",
                "score": 6,
                "mitigation": "Validate requirements before development and track changes."
            },
            {
                "risk": "Schedule delay",
                "probability": "High",
                "impact": "Medium",
                "score": 6,
                "mitigation": "Prioritize high-value tasks and review progress regularly."
            },
            {
                "risk": "Security vulnerabilities",
                "probability": "Medium",
                "impact": "High",
                "score": 6,
                "mitigation": "Use authentication, authorization, input validation and security testing."
            },
            {
                "risk": "Integration failures",
                "probability": "Medium",
                "impact": "Medium",
                "score": 4,
                "mitigation": "Integrate modules incrementally and run integration tests."
            }
        ]

        if len(tasks) > 15:
            risks.append({
                "risk": "Large project scope",
                "probability": "High",
                "impact": "High",
                "score": 9,
                "mitigation": "Break the project into milestones and deliver an MVP first."
            })

        return sorted(risks, key=lambda x: x["score"], reverse=True)


class ProgressAgent:
    def run(self, tasks, risks):
        total = len(tasks)
        # Initial demo state: everything is pending.
        completed = sum(1 for t in tasks if t["status"] == "Completed")
        percentage = round((completed / total) * 100, 1) if total else 0

        high_risk = sum(1 for r in risks if r["score"] >= 7)

        if high_risk:
            health = "Needs Attention"
        elif percentage >= 70:
            health = "Good"
        else:
            health = "On Track"

        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": total - completed,
            "percentage": percentage,
            "high_risk_count": high_risk,
            "health": health
        }


class ProjectManager:
    def __init__(self):
        self.requirement_agent = RequirementAgent()
        self.planning_agent = PlanningAgent()
        self.scheduling_agent = SchedulingAgent()
        self.testing_agent = TestingAgent()
        self.risk_agent = RiskAgent()
        self.progress_agent = ProgressAgent()

    def run(self, description):
        requirements = self.requirement_agent.run(description)
        tasks = self.planning_agent.run(requirements)
        scheduling = self.scheduling_agent.run(tasks)
        tests = self.testing_agent.run(requirements, tasks)
        risks = self.risk_agent.run(requirements, tasks)
        progress = self.progress_agent.run(tasks, risks)

        return {
            "requirements": requirements,
            "tasks": tasks,
            "scheduling": scheduling,
            "tests": tests,
            "risks": risks,
            "progress": progress,
            "agents": [
                "Requirement Agent",
                "Planning Agent",
                "Scheduling Agent",
                "Development Agent",
                "Testing Agent",
                "Risk Agent",
                "Progress Agent"
            ]
        }
