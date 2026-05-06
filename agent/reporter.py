import os

def generate_report(results, analyses):
    report_lines = [
        "===== TRANSACTION FAILURE REPORT =====\n",
        f"Total Transactions Analyzed: {len(results)}\n",
        "=" * 50 + "\n"
    ]

    for item, analysis in zip(results, analyses):
        report_lines.append(f"--- Transaction ({item['correlationId']}) ---")
        systems = list(set(e["system"] for e in item["events"]))
        report_lines.append(f"Systems Involved: {systems}")

        if item["failures"]:
            report_lines.append("Failures:")
            for f in item["failures"]:
                report_lines.append(f"{f.get('system', '')} - {f.get('eventType', '')} - {f.get('details', '')}")
        else:
            report_lines.append("Failures: None")

        report_lines.append("\nAI Analysis:")
        report_lines.append(analysis)
        report_lines.append("-" * 50 + "\n")

    return "\n".join(report_lines)

def save_report(report, file_path="output/final_report.txt"):
    os.makedirs(os.path.dirname(file_path) or "output", exist_ok=True)
    with open(file_path, "w") as f:
        f.write(report)
    print("Report saved to", file_path)